from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination
from reviews.models import Category, Genre, Title
from .serializers import TitleSerializer, CategorySerializer, GenreSerializer
from .permissions import IsAdmin, IsAdminOrReadOnly, IsAuthorOrAdminOrModerator
from django_filters.rest_framework import DjangoFilterBackend


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'title', 'year')
    permission_classes = (
        IsAdminOrReadOnly,
    )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title',)
    permission_classes = (
        IsAdminOrReadOnly,
    )

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title',) 
    permission_classes = (
        IsAdminOrReadOnly,
    )