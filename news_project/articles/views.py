from rest_framework import generics, viewsets, permissions
from .models import Article, User
from rest_framework.exceptions import PermissionDenied
from .serializers import ArticleSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import AuthTokenSerializer


class CustomAuthToken(ObtainAuthToken):
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token_data = serializer.create(serializer.validated_data)
        return Response(token_data)


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ArticleListCreateView(generics.CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != 'author':
            raise PermissionDenied("Вы не можете создавать посты.")
        serializer.save(author=self.request.user)


class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.author:
            raise PermissionDenied("Вы не можете редактировать этот пост.")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise PermissionDenied("Вы не можете удалить этот пост.")
        instance.delete()


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_queryset(self):
        user = self.request.user
        if self.request.user.is_authenticated and user.role == 'subscriber':
            return Article.objects.all()
        return Article.objects.filter(is_published=True)
