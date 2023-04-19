from rest_framework import serializers

from common.models import *
from common.serializers import *
from .models import *





class NodeSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255)
    tags = TagField(queryset=Tag.objects.all(), many=True)
    language = TagField(queryset=Language.objects.all())
    links = serializers.SlugRelatedField(queryset=Branch.objects.all(), many=True, slug_field="slug")
    author = OtherUserSerializer(read_only=True)

    def get_author_instance(self, username):
        try:
            return User.objects.get(username=username)
        except Exception:
            raise serializers.ValidationError(f"User with username '{username}' does not exist.")

    def create(self, validated_data):
        data = self.initial_data
        if 'username' in data["author"]:
            validated_data['author'] = self.get_author_instance(data['author']['username'])

        links = validated_data.pop('links')
        tags = validated_data.pop('tags')
        instance = Branch.objects.create(**validated_data)
        instance.links.set(links)
        instance.tags.set(tags)
        return instance




    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related('links', 'tags').select_related('language', 'author')
        return queryset


    class Meta:
        exclude = ('users_liked','users_learned','users_wanted',)
        model = Branch


class BranchSerializer(NodeSerializer):
    links = serializers.SerializerMethodField()

    def get_links(self, obj):
        if obj in self.context.get('seen_branches', []):
            return 'Уже есть'
        else:
            seen_branches = self.context.get('seen_branches', []) + [obj]
            queryset = super().setup_eager_loading(obj.links.all())
            serializer = BranchSerializer(
                queryset,
                many=True, context={'seen_branches': seen_branches}
            )
            return serializer.data

    # add other fields as needed


class RelationsSerializer(serializers.ModelSerializer):
    child = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all())
    parent = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all())

    class Meta:
        fields = '__all__'
        model = Relations