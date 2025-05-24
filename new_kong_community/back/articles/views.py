from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Comment
from rest_framework import status
from django.shortcuts import render
from .serializers import ArticleListSerializer, ArticleSerializer, ArticleDetailSerializer, CommentSerializer
from .models import Article
from django.shortcuts import get_object_or_404


#전체 글 목록

@api_view(['GET', 'POST'])
def article_list_create(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializers = ArticleListSerializer(articles, many=True)
        return Response(serializers.data)    
    
    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

# 단일 게시글 조회/수정/삭제
@api_view(['GET', 'PUT', 'DELETE'])
def article_detail(request, article_pk):
    try:
        article = Article.objects.get(pk=article_pk)
    except article.DoesNotExist:
        return Response({'error': 'article not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            article = serializer.save()
            response_serializer = ArticleDetailSerializer(article)
            return Response(response_serializer.data)
        # print('들어왔니?')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        article.delete()
        
        return Response({'message': f'article {article_pk} is deleted'}, status=status.HTTP_204_NO_CONTENT)

# 글 생성
@api_view(['POST'])
def create_aritcle(request, aritcle_pk):
    try:
        movie = Article.objects.get(pk=article_pk)
    except Article.DoesNotExist:
        return Response({'error': 'Article not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ArticleSerializer(data=request.data)
    if serializer.is_valid():
        article = serializer.save(movie=movie)
        # 응답은 상세 serializer로 반환
        response_serializer = ArticleDetailSerializer(article)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#댓글작성
@api_view(['GET', 'POST'])
def comment_create(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)  # ✅ 게시글 가져오기

    if request.method == 'GET':
        comments = article.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = CommentSerializer(
            data=request.data,
            context={'request': request, 'article': article}
        )
        if serializer.is_valid():
            serializer.save()  # 👈 user, article은 context로 전달
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

