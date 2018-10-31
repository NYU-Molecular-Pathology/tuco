from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('run/', views.runs, name='runs'),
    path('run/<int:id>', views.run, name='run'),
    path('sample/', views.samples, name='samples'),
    path('sample/<int:id>', views.sample, name='sample'),
    path('samplesheet/', views.samplesheets, name='samplesheets'),
    path('samplesheet/<int:id>', views.samplesheet, name='samplesheet'),
]
