from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ValidationError
from rest_framework import generics, viewsets, filters
from rest_framework.pagination import PageNumberPagination


from api.serializers import ReviewSerializer, CommentSerializer
from api.permissions import IsAuthorModeratorOrReadOnly
from reviews.models import Review, Comment, Title

def index(request):
    pass


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorModeratorOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Title, iid=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = Title.objects.get(id=title_id)
        if self.request.user.reviews.filter(title=title_id).exists():
            raise ValidationError("К этому произведению уже оставлен отзыв.")
        
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorModeratorOrReadOnly,)
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)