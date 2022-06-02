from django.shortcuts import get_object_or_404, render
from rest_framework import generics, viewsets, filters
from rest_framework.pagination import PageNumberPagination

from api.serializers import ReviewSerializer, CommentSerializer
from api.permissions import IsAuthorOrReadOnly
from reviews.models import Review, Comment

def index(request):
    pass


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)