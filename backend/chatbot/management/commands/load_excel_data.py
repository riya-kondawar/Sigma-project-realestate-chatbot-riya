import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings
from chatbot.models import RealEstateData

class Command(BaseCommand):
    help = 'Load real estate data from Excel file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            help='Path to Excel file',
            default='sample_data.xlsx'
        )

    def handle(self, *args, **options):
        file_path = options['file']
        
        # If relative path, look in project root
        if not os.path.isabs(file_path):
            project_root = settings.BASE_DIR
            file_path = os.path.join(project_root, file_path)
        
        self.stdout.write(f"Loading data from: {file_path}")
        
        if not os.path.exists(file_path):
            self.stderr.write(f"Error: File not found at {file_path}")
            # List files in directory to help debug
            dir_path = os.path.dirname(file_path)
            if os.path.exists(dir_path):
                files = os.listdir(dir_path)
                self.stdout.write(f"Files in directory: {', '.join(files)}")
            return
        
        try:
            # Try different Excel engines
            try:
                df = pd.read_excel(file_path, engine='openpyxl')
            except Exception as e:
                self.stdout.write(f"openpyxl failed, trying default engine: {e}")
                df = pd.read_excel(file_path)  # Try without specifying engine
            
            self.stdout.write(f"Successfully read Excel file with {len(df)} rows")
            self.stdout.write(f"Columns: {', '.join(df.columns.tolist())}")
            
            # Clear existing data
            count_before = RealEstateData.objects.count()
            RealEstateData.objects.all().delete()
            self.stdout.write(f"Cleared {count_before} existing records")
            
            # Process each row
            processed_count = 0
            for index, row in df.iterrows():
                try:
                    self.create_real_estate_record(row)
                    processed_count += 1
                    if processed_count % 10 == 0:  # Progress indicator
                        self.stdout.write(f"Processed {processed_count} rows...")
                except Exception as e:
                    self.stderr.write(f"Error processing row {index}: {e}")
                    continue
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully loaded {processed_count} records from Excel file')
            )
            
        except Exception as e:
            self.stderr.write(f"Error loading Excel file: {e}")
            self.stdout.write("Make sure openpyxl is installed: pip install openpyxl")

    def create_real_estate_record(self, row):
        """Create a RealEstateData record from a pandas row"""
        
        # Helper function to safely get values
        def get_value(key, default=0):
            value = row.get(key)
            if pd.isna(value) or value is None:
                return default
            try:
                return float(value) if isinstance(value, (int, float)) else value
            except (ValueError, TypeError):
                return default
        
        # Handle column name variations
        column_mapping = {
            'final_location': 'final location',
            'total_sales_igr': 'total_sales - igr',
            'total_sold_igr': 'total sold - igr',
            'flat_sold_igr': 'flat_sold - igr',
            'office_sold_igr': 'office_sold - igr',
            'others_sold_igr': 'others_sold - igr',
            'shop_sold_igr': 'shop_sold - igr',
            'commercial_sold_igr': 'commercial_sold - igr',
            'other_sold_igr': 'other_sold - igr',
            'residential_sold_igr': 'residential_sold - igr',
            'flat_weighted_avg_rate': 'flat - weighted average rate',
            'office_weighted_avg_rate': 'office - weighted average rate',
            'others_weighted_avg_rate': 'others - weighted average rate',
            'shop_weighted_avg_rate': 'shop - weighted average rate',
            'total_carpet_area': 'total carpet area supplied (sqft)'
        }
        
        def get_mapped_value(field_name, default=0):
            # Try direct mapping first
            if field_name in row:
                value = row[field_name]
            else:
                # Try mapped column name
                mapped_name = column_mapping.get(field_name, field_name)
                value = row.get(mapped_name, default)
            
            if pd.isna(value) or value is None:
                return default
            return value

        RealEstateData.objects.create(
            final_location=str(get_mapped_value('final_location', 'Unknown')),
            year=int(get_mapped_value('year', 2020)),
            city=str(get_mapped_value('city', 'Pune')),
            loc_lat=float(get_mapped_value('loc_lat', 0)),
            loc_lng=float(get_mapped_value('loc_lng', 0)),
            total_sales_igr=float(get_mapped_value('total_sales_igr', 0)),
            total_sold_igr=int(get_mapped_value('total_sold_igr', 0)),
            flat_sold_igr=int(get_mapped_value('flat_sold_igr', 0)),
            office_sold_igr=int(get_mapped_value('office_sold_igr', 0)),
            others_sold_igr=int(get_mapped_value('others_sold_igr', 0)),
            shop_sold_igr=int(get_mapped_value('shop_sold_igr', 0)),
            commercial_sold_igr=int(get_mapped_value('commercial_sold_igr', 0)),
            other_sold_igr=int(get_mapped_value('other_sold_igr', 0)),
            residential_sold_igr=int(get_mapped_value('residential_sold_igr', 0)),
            flat_weighted_avg_rate=float(get_mapped_value('flat_weighted_avg_rate', 0)),
            office_weighted_avg_rate=float(get_mapped_value('office_weighted_avg_rate', 0)),
            others_weighted_avg_rate=float(get_mapped_value('others_weighted_avg_rate', 0)),
            shop_weighted_avg_rate=float(get_mapped_value('shop_weighted_avg_rate', 0)),
            total_units=int(get_mapped_value('total_units', 0)),
            total_carpet_area=float(get_mapped_value('total_carpet_area', 0)),
            flat_total=int(get_mapped_value('flat_total', 0)),
            shop_total=int(get_mapped_value('shop_total', 0)),
            office_total=int(get_mapped_value('office_total', 0)),
            others_total=int(get_mapped_value('others_total', 0))
        )