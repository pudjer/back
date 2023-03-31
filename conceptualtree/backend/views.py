
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .serializers import *

class MyPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100



class NodeViewSet(viewsets.ModelViewSet):
    pagination_class = MyPagination
    serializer_class = NodeSerializer
    queryset = Branch.objects.all()
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

    def get_queryset(self):
        queryset = super().get_queryset()
        # Set up eager loading to avoid N+1 selects
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset

    @action(methods=['GET'], detail=True)
    def show_branch_as_obj(self, request, slug):
        branch = Branch.objects.get(slug=slug)
        serializer = BranchSerializer(instance=branch)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True)
    def show_branch(self, request, slug):
        branch = Branch.objects.get(slug=slug)
        relations = branch.get_relations()
        unique_branches = {relation.child_id for relation in relations}
        unique_branches.add(branch.pk)
        unique_branches = Branch.objects.filter(pk__in=unique_branches)

        queryset = NodeSerializer.setup_eager_loading(unique_branches)
        serializer = NodeSerializer(queryset, many=True)

        rel_serializer = RelationsSerializer(relations, many=True)
        return Response({'nodes':serializer.data, 'links':rel_serializer.data})


