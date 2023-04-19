from django.urls import path

from search.views import SearchNodeViewSet

urlpatterns = [
    #path('', index , name='home' )
    path('node/', SearchNodeViewSet.as_view({'get': 'list'}), name='searchnode'),
]