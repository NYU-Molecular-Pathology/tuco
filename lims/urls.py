from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'lims'

urlpatterns = [
    path('', views.index, name='index'),
    path('run/', views.RunsList.as_view(), name='runs'), # all runs
    path('run/<int:id>', views.RunDetail.as_view(), name='run'), # one run
    path('sample/', views.SamplesList.as_view(), name='samples'), # all samples
    path('sample/<int:id>', views.SampleDetail.as_view(), name='sample'), # one sample
    path('samplesheet/', views.SampleSheetList.as_view(), name='samplesheets'), # all samplesheets
    path('samplesheet/<int:id>', views.SampleSheetDetail.as_view(), name='samplesheet'),  #one samplesheet
    path('samplesheet/upload', views.samplesheet_upload, name='samplesheet_upload') # all samplesheets
]
