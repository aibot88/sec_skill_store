---
name: django-codegen
description: |
  트리거: "django 코드 생성", "django rest", "drf 만들어줘", "django 모델 생성", "django viewset 만들어줘"
  수행: Python Django REST Framework 기반 Model·Serializer·ViewSet·URL패턴·Permission을 일괄 생성한다.
  DRF ModelSerializer, ModelViewSet, DefaultRouter, IsAuthenticated/커스텀 Permission 클래스 적용.
  출력: 앱 디렉토리 구조 + 각 파일 코드 블록 + urls.py 등록 안내.
---

# Django REST Framework 코드 생성기

## 목적

Django 앱 이름과 모델 필드만 입력하면 DRF 기반 REST API 전체(Model → Serializer → ViewSet → URL)를
즉시 생성한다. 인증·권한 설정, 필터링, 페이지네이션까지 실용적인 기본값을 포함한다.

## 실행 절차

1. **입력 파악**: 앱 이름, 모델 이름, 필드 목록, 인증 요구사항 확인
2. **models.py 생성**: Django ORM 모델, Meta 클래스(ordering, verbose_name), `__str__` 메서드
3. **serializers.py 생성**: ModelSerializer(List/Detail/Create 분리), `validate_*` 메서드, 중첩 직렬화
4. **views.py 생성**: ModelViewSet, 커스텀 액션(`@action`), `get_queryset` 오버라이드
5. **permissions.py 생성**: 커스텀 Permission 클래스 (IsOwner 등)
6. **urls.py 생성**: DefaultRouter 등록, urlpatterns 정의
7. **admin.py 생성**: ModelAdmin 기본 설정
8. **migrations 안내**: `python manage.py makemigrations && migrate` 명령 안내

## 출력 형식

### 앱 디렉토리 구조
```
{app_name}/
├── __init__.py
├── models.py
├── serializers.py
├── views.py
├── permissions.py
├── urls.py
├── admin.py
└── tests.py
```

### 각 파일 코드 블록 + urls.py 프로젝트 등록 안내
```python
# config/urls.py에 추가
path('api/v1/', include('{app_name}.urls')),
```

## 사용 예시

### 입력
```
Article 앱 django rest framework로 만들어줘.
모델: id(AutoField), title(CharField, max=200), content(TextField), author(ForeignKey User), status(choices: draft/published), created_at(auto_now_add)
인증: 로그인한 사용자만 작성, 작성자만 수정/삭제 가능
```

### 출력 (models.py)
```python
# articles/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Article(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'draft', '초안'
        PUBLISHED = 'published', '게시됨'

    title = models.CharField(max_length=200, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='articles',
        verbose_name='작성자'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name='상태'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        ordering = ['-created_at']
        verbose_name = '게시글'
        verbose_name_plural = '게시글 목록'
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['author']),
        ]

    def __str__(self):
        return f"[{self.get_status_display()}] {self.title}"
```

### 출력 (serializers.py)
```python
# articles/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Article

User = get_user_model()


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = fields


class ArticleListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'author', 'status', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']


class ArticleDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'author', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']


class ArticleCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'content', 'status']

    def validate_title(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("제목은 최소 2자 이상이어야 합니다.")
        return value.strip()

    def validate_content(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("내용은 최소 10자 이상이어야 합니다.")
        return value

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
```

### 출력 (permissions.py)
```python
# articles/permissions.py
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    객체의 소유자만 수정/삭제 가능. 나머지는 읽기만 허용.
    """
    message = "이 작업은 작성자만 수행할 수 있습니다."

    def has_object_permission(self, request, view, obj):
        # 읽기 권한은 모든 요청에 허용
        if request.method in permissions.SAFE_METHODS:
            return True
        # 쓰기 권한은 소유자에게만 허용
        return obj.author == request.user
```

### 출력 (views.py)
```python
# articles/views.py
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Article
from .serializers import (
    ArticleListSerializer,
    ArticleDetailSerializer,
    ArticleCreateUpdateSerializer,
)
from .permissions import IsOwnerOrReadOnly


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.select_related('author').all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'author']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return ArticleCreateUpdateSerializer
        return ArticleDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        # 비로그인 사용자는 published 게시글만 조회
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(status=Article.Status.PUBLISHED)
        return queryset

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_articles(self, request):
        """현재 로그인한 사용자의 게시글 목록"""
        queryset = self.get_queryset().filter(author=request.user)
        serializer = ArticleListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsOwnerOrReadOnly])
    def publish(self, request, pk=None):
        """게시글 발행"""
        article = self.get_object()
        article.status = Article.Status.PUBLISHED
        article.save(update_fields=['status', 'updated_at'])
        return Response({'status': 'published'}, status=status.HTTP_200_OK)
```

### 출력 (urls.py)
```python
# articles/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'articles', views.ArticleViewSet, basename='article')

urlpatterns = [
    path('', include(router.urls)),
]

# 생성되는 URL 패턴:
# GET    /api/v1/articles/           - 목록 조회
# POST   /api/v1/articles/           - 생성
# GET    /api/v1/articles/{id}/      - 상세 조회
# PUT    /api/v1/articles/{id}/      - 전체 수정
# PATCH  /api/v1/articles/{id}/      - 부분 수정
# DELETE /api/v1/articles/{id}/      - 삭제
# GET    /api/v1/articles/my_articles/ - 내 게시글
# POST   /api/v1/articles/{id}/publish/ - 발행
```

### 출력 (admin.py)
```python
# articles/admin.py
from django.contrib import admin
from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'content', 'author__username']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['author']
```

## 주의사항

- **`get_user_model()`**: `AUTH_USER_MODEL`이 커스텀인 경우에도 안전. `from django.contrib.auth.models import User` 직접 임포트 금지.
- **`select_related` / `prefetch_related`**: ForeignKey는 `select_related`, ManyToMany/역참조는 `prefetch_related`로 N+1 방지.
- **직렬화 분리**: List/Detail/CreateUpdate 직렬화 클래스 분리로 오버페치 방지.
- **`update_fields`**: 부분 필드만 업데이트 시 `save(update_fields=[...])` 사용으로 불필요한 UPDATE 방지.
- **`auto_now_add` vs `default`**: `auto_now_add=True`는 수정 불가. 테스트에서 값 제어가 필요하면 `default=timezone.now` 사용.
- **DjangoFilterBackend**: `django-filter` 패키지 별도 설치 필요 (`pip install django-filter`).
- **INSTALLED_APPS**: 생성한 앱과 `'rest_framework'`, `'django_filters'`를 `settings.py`에 등록해야 함.
