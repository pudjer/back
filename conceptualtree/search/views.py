from rest_framework import viewsets

from backend.serializers import NodeSerializer
from search.documents import NodeDocument



class SearchNodeViewSet(viewsets.ModelViewSet):
    serializer_class = NodeSerializer
    def get_queryset(self):
        queryset = NodeDocument.search().query('match', content=str(self.kwargs['query'])).to_queryset()
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset
