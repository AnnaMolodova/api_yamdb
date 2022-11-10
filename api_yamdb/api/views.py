from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework import filters, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings
from django.db.models import Avg
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
                                   DestroyModelMixin)

from .filters import TitleFilter
from reviews.models import Category, Genre, Title, User
from .serializers import (
    RegistrationSerializer,
    UserMeSerializer,
    UserSerializer,
    TokenCodeSerializer,
    CategorySerializer,
    GenreSerializer,
    TitleReadSerializer,
    TitleSerializer,
    ReviewSerializer,
    CommentSerializer
)
from api.permissions import (AuthorAdminReadOnly,
                             CommentReviewPermission,
                             IsAdminOrSuperuser, AdminUserOrReadOnly)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrSuperuser, ]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, )
    search_fields = ('username', )
    lookup_field = 'username'

    @action(
        detail=False, methods=['GET', 'PATCH'], url_path='me',
        permission_classes=(AuthorAdminReadOnly, )
    )
    def me(self, request):
        serializer = UserMeSerializer(request.user)
        userself = User.objects.get(username=self.request.user)
        if request.method == 'PATCH':
            serializer = UserMeSerializer(
                userself,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'GET':
            serializer = self.get_serializer(userself)
            return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def sign_up(request):
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']
    user = User.objects.get_or_create(username=username, email=email)
    user.confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Ваш код',
        user.username,
        user.confirmation_code,
        settings.ADMIN_EMAIL,
        [user.email]
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    serializer_class = TokenCodeSerializer
    serializer = serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.data['username']
    )
    confirmation_code = serializer.validated_data['confirmation_code']
    if user.confirmation_code != confirmation_code:
        return Response('Код подтверждения неверный',
                        status=status.HTTP_400_BAD_REQUEST)
    token = RefreshToken.for_user(user)
    return Response({
        'token': str(token),
        'access': str(token.access_token),
    },
        status=status.HTTP_200_OK)


class CategoryViewSet(CreateModelMixin, ListModelMixin,
                      DestroyModelMixin, GenericViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [AuthorAdminReadOnly, ]
    filter_backends = (SearchFilter, )
    search_fields = ('name', 'slug')
    lookup_field = 'slug'


class GenreViewSet(CreateModelMixin, ListModelMixin,
                   DestroyModelMixin, GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AdminUserOrReadOnly, ]
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all()
    serializer_class = TitleSerializer
    permission_classes = [AdminUserOrReadOnly, ]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return TitleReadSerializer
        return TitleSerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [CommentReviewPermission, ]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [CommentReviewPermission, ]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = get_object_or_404(
            title.reviews, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = get_object_or_404(
            title.reviews, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
