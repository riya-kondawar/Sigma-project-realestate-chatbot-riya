from django.urls import path
from .views import ChatAnalysisView, UploadExcelView, DownloadDataView

urlpatterns = [
    path('analyze/', ChatAnalysisView.as_view(), name='analyze'),
    path('upload/', UploadExcelView.as_view(), name='upload'),
    path('download/', DownloadDataView.as_view(), name='download'),
]