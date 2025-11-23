import pandas as pd
import json
import openai
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework import status
from django.conf import settings
from .models import RealEstateData
from .serializers import RealEstateDataSerializer

class ChatAnalysisView(APIView):
    parser_classes = [JSONParser]

    def __init__(self):
        super().__init__()
        # Initialize OpenAI client only if API key is available
        if getattr(settings, 'OPENAI_API_KEY', None) and settings.OPENAI_API_KEY != 'your_openai_api_key_here':
            openai.api_key = settings.OPENAI_API_KEY
            self.openai_available = True
        else:
            self.openai_available = False

    def post(self, request):
        query = request.data.get('query', '')
        
        if not query:
            return Response({'error': 'Query is required'}, status=400)

        # Process query and get data
        analysis_data = self.process_query(query)
        
        if not analysis_data:
            return Response({'error': 'No data found for the given query'}, status=404)

        # Generate AI summary
        summary = self.generate_ai_summary(query, analysis_data)
        
        # Prepare chart data
        chart_data = self.prepare_chart_data(analysis_data)
        
        return Response({
            'summary': summary,
            'chart_data': chart_data,
            'table_data': analysis_data,
            'query': query
        })

    def process_query(self, query):
        locations = self.extract_locations(query)
        years = self.extract_years(query)
        
        queryset = RealEstateData.objects.all()
        
        if locations:
            queryset = queryset.filter(final_location__in=locations)
        
        if years:
            queryset = queryset.filter(year__in=years)
        
        serializer = RealEstateDataSerializer(queryset, many=True)
        return serializer.data

    def extract_locations(self, query):
        locations = ['Akurdi', 'Ambegaon Budruk', 'Aundh', 'Wakad']
        found_locations = []
        
        query_lower = query.lower()
        for location in locations:
            if location.lower() in query_lower:
                found_locations.append(location)
        
        # If no specific location found, return all for general queries
        if not found_locations and any(word in query_lower for word in ['pune', 'all', 'every', 'overview']):
            return locations
        
        return found_locations if found_locations else locations  # Return all if none specified

    def extract_years(self, query):
        years = []
        words = query.split()
        for word in words:
            if word.isdigit() and len(word) == 4:
                year = int(word)
                if 2020 <= year <= 2024:
                    years.append(year)
        
        # Check for "last X years" pattern
        query_lower = query.lower()
        if 'last 3 years' in query_lower:
            return [2022, 2023, 2024]
        elif 'last 2 years' in query_lower:
            return [2023, 2024]
        elif 'last year' in query_lower:
            return [2024]
            
        return years  # Return empty list for all years

    def generate_ai_summary(self, query, data):
        try:
            if not self.openai_available:
                return self.generate_mock_summary(query, data)

            prompt = f"""
            Analyze this real estate data and provide a concise, insightful summary in 2-3 paragraphs.
            
            User Query: {query}
            
            Data: {json.dumps(data, indent=2)}
            
            Focus on:
            1. Key trends in prices and demand
            2. Comparison between locations if multiple are present
            3. Notable changes over years
            4. Market insights and recommendations
            
            Write in a professional but accessible tone for real estate analysis.
            """

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a real estate market analyst providing insightful analysis of property data."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI error: {e}")
            return self.generate_mock_summary(query, data)

    def generate_mock_summary(self, query, data):
        if not data:
            return "No data available for analysis."
            
        locations = list(set([item['final_location'] for item in data]))
        years = list(set([item['year'] for item in data]))
        
        # Calculate basic statistics
        avg_prices = [item['flat_weighted_avg_rate'] for item in data if item['flat_weighted_avg_rate']]
        total_sales = [item['total_sales_igr'] for item in data if item['total_sales_igr']]
        total_units = [item['total_sold_igr'] for item in data if item['total_sold_igr']]
        
        avg_price = sum(avg_prices) / len(avg_prices) if avg_prices else 0
        total_sales_sum = sum(total_sales) if total_sales else 0
        total_units_sum = sum(total_units) if total_units else 0
        
        return f"""
## Real Estate Analysis Report

**Analysis for**: {', '.join(locations) if locations else 'All locations'}  
**Period**: {min(years) if years else 'N/A'}-{max(years) if years else 'N/A'}  
**Total Transactions**: {len(data)} records

### Market Overview
The analyzed real estate market shows {'growth' if len(years) > 1 else 'stable'} trends during the period. 
Average property prices are around ₹{avg_price:,.0f} per sqft, with total sales volume of ₹{total_sales_sum:,.0f} 
across {total_units_sum} units sold.

### Key Insights
- **Price Trends**: Properties have maintained consistent valuation across the analyzed period
- **Demand Patterns**: Market shows healthy transaction volumes
- **Location Analysis**: {locations[0] if len(locations) == 1 else 'Multiple locations'} demonstrate unique market characteristics

### Recommendations
Based on the data analysis, this market presents opportunities for both investors and homebuyers. 
Consider monitoring price fluctuations and demand patterns for optimal decision-making.
        """

    def prepare_chart_data(self, data):
        if not data:
            return None

        # Group by year and location
        chart_data = {}
        
        for item in data:
            location = item['final_location']
            year = item['year']
            
            if location not in chart_data:
                chart_data[location] = {
                    'years': [],
                    'prices': [],
                    'demand': [],
                    'sales': []
                }
            
            # Avoid duplicates and ensure data exists
            if year not in chart_data[location]['years']:
                chart_data[location]['years'].append(year)
                chart_data[location]['prices'].append(item.get('flat_weighted_avg_rate', 0))
                chart_data[location]['demand'].append(item.get('total_sold_igr', 0))
                chart_data[location]['sales'].append(item.get('total_sales_igr', 0) / 1000000)  # In millions
        
        return chart_data

class UploadExcelView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file provided'}, status=400)

        try:
            # Read the Excel file
            df = pd.read_excel(file)
            
            # Print column names for debugging
            print("Excel columns:", df.columns.tolist())
            
            # Process the data
            result = self.process_excel_data(df)
            return Response({'message': 'Data uploaded successfully', 'processed_rows': result})
        except Exception as e:
            print(f"Upload error: {e}")
            return Response({'error': f'Upload failed: {str(e)}'}, status=400)

    def process_excel_data(self, df):
        # Clear existing data
        RealEstateData.objects.all().delete()
        
        processed_count = 0
        
        for index, row in df.iterrows():
            try:
                # Create a new record with proper error handling
                RealEstateData.objects.create(
                    final_location=row.get('final location', ''),
                    year=int(row.get('year', 2020)),
                    city=row.get('city', 'Pune'),
                    loc_lat=float(row.get('loc_lat', 0)),
                    loc_lng=float(row.get('loc_lng', 0)),
                    total_sales_igr=float(row.get('total_sales - igr', 0)),
                    total_sold_igr=int(row.get('total sold - igr', 0)),
                    flat_sold_igr=int(row.get('flat_sold - igr', 0)),
                    office_sold_igr=int(row.get('office_sold - igr', 0)),
                    others_sold_igr=int(row.get('others_sold - igr', 0)),
                    shop_sold_igr=int(row.get('shop_sold - igr', 0)),
                    commercial_sold_igr=int(row.get('commercial_sold - igr', 0)),
                    other_sold_igr=int(row.get('other_sold - igr', 0)),
                    residential_sold_igr=int(row.get('residential_sold - igr', 0)),
                    flat_weighted_avg_rate=float(row.get('flat - weighted average rate', 0)),
                    office_weighted_avg_rate=float(row.get('office - weighted average rate', 0)),
                    others_weighted_avg_rate=float(row.get('others - weighted average rate', 0)),
                    shop_weighted_avg_rate=float(row.get('shop - weighted average rate', 0)),
                    total_units=int(row.get('total units', 0)),
                    total_carpet_area=float(row.get('total carpet area supplied (sqft)', 0)),
                    flat_total=int(row.get('flat total', 0)),
                    shop_total=int(row.get('shop total', 0)),
                    office_total=int(row.get('office total', 0)),
                    others_total=int(row.get('others total', 0))
                )
                processed_count += 1
            except Exception as e:
                print(f"Error processing row {index}: {e}")
                continue
        
        return processed_count

class DownloadDataView(APIView):
    def get(self, request):
        location = request.GET.get('location')
        year = request.GET.get('year')
        
        queryset = RealEstateData.objects.all()
        
        if location and location != 'all':
            queryset = queryset.filter(final_location=location)
        if year and year != 'all':
            queryset = queryset.filter(year=int(year))
        
        serializer = RealEstateDataSerializer(queryset, many=True)
        return Response(serializer.data)

class InitializeDataView(APIView):
    def post(self, request):
        """Initialize with sample data if no data exists"""
        if RealEstateData.objects.exists():
            return Response({'message': 'Data already exists'})
        
        # You can add sample data initialization here if needed
        return Response({'message': 'Initialize data endpoint ready'})