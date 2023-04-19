
from elasticsearch_dsl.query import Q
from backend.serializers import NodeSerializer
from search.documents import NodeDocument



from rest_framework import viewsets

class SearchNodeViewSet(viewsets.ModelViewSet):
    serializer_class = NodeSerializer

    def get_queryset(self):
        search_query = self.request.query_params.get('query', '')
        query = Q("multi_match", query=search_query, fields=['title', 'content']) | \
                Q("nested", path="tags", query=Q("term", tags__name=search_query)) | \
                Q("nested", path="author", query=Q("term", author__username=search_query))
        queryset = NodeDocument.search().query(query).to_queryset()
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset



