from django.contrib import admin
from .models import RealEstateData

@admin.register(RealEstateData)
class RealEstateDataAdmin(admin.ModelAdmin):
    list_display = ['final_location', 'year', 'city', 'total_sold_igr', 'flat_weighted_avg_rate']
    list_filter = ['final_location', 'year', 'city']
    search_fields = ['final_location', 'city']