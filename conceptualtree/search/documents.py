from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import analyzer

from backend.models import *


html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)

@registry.register_document
class NodeDocument(Document):
    title = fields.TextField(
        analyzer=html_strip)
    content = fields.TextField(
        analyzer=html_strip)
    tags = fields.NestedField(
        properties={
            'name': fields.KeywordField()
        })
    language = fields.NestedField(
        properties={
            'name': fields.KeywordField()
        })
    author = fields.NestedField(
        properties={
            'username': fields.KeywordField()
        })
    suggest = fields.CompletionField()
    class Index:
        name = 'nodes'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}
    class Django:
        model = Branch

    related_models = [Language, User]

    def get_queryset(self):
        return super().get_queryset().select_related(
            'language',
            'author',
        )

    def get_instances_from_related(self, related_instance):
            return related_instance.branch_set.all()

# recursivefield, raw,