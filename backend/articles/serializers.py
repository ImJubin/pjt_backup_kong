from rest_framework import serializers
from .models import Article
from .models import Comment

class ArticleTitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ['title']

class ArticleListSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Article
        fields = ('id', 'title', 'content')


class ArticleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Article
        fields = '__all__'


class ArticleDetailSerializer(serializers.ModelSerializer):
    movie = ArticleTitleSerializer(read_only=True) 

    class Meta:
        model = Article
        fields = ['id', 'movie', 'title', 'content']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'article', 'created_at')  # ✅ 클라이언트가 이 값 보내지 않아도 됨!

    def create(self, validated_data):
        request = self.context.get('request')
        article = self.context.get('article')
        return Comment.objects.create(
            user=request.user,
            article=article,
            **validated_data
        ) 