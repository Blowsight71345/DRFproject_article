from django.urls import path, include
from .views import (ArticleDetailView, ArticleListCreateView,
                    CustomAuthToken, UserRegistrationView)
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="News_project API",
      default_version='v1',
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contacts@example.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register('articles', ArticleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationView.as_view(),
         name='user-registration'),
    path('articles/', ArticleListCreateView.as_view(),
         name='article-list-create'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(),
         name='article-detail'),
    path('articles/<int:pk>/update/',
         ArticleViewSet.as_view({'put': 'partial_update'}),
         name='article-update'),
    path('articles/<int:pk>/delete/',
         ArticleViewSet.as_view({'delete': 'destroy'}),
         name='article-delete'),
    path('articles/create', ArticleListCreateView.as_view(),
         name='article-create'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
    path('api/token/auth/', CustomAuthToken.as_view(),
         name='api_token_auth'),
]
