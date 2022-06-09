import io
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from .models import Article, Category


class ArticleSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault)
    category = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Article
        fields = ('title', 'content', 'time_create', 'category', 'source', 'user')
