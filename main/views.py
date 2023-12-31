from rest_framework.decorators import api_view  # [GET, POST, PUT, DELETE]
from rest_framework.response import Response  # Return Result
from main.serializers import NewsSerializer, CategorySerializer, TagSerializer
from main.models import News, Category, Tag
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.views import APIView


class NewsListCreateAPIView(ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def create(self, request, *args, **kwargs):
        serializer = NewsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=400, data=serializer.errors)

        # Step 1. Get data from BODY
        title = serializer.validated_data.get('title') # None
        text = serializer.validated_data.get('text') # None
        amount = serializer.validated_data.get('amount')
        is_active = serializer.validated_data.get('is_active') # T
        category_id = serializer.validated_data.get('category_id')
        tags = serializer.validated_data.get('tags')

        # Step 2. Create news by this data
        news = News.objects.create(
            title=title, text=text,
            view_amount=amount, is_active=is_active,
            category_id=category_id
        )
        news.tags.set(tags)
        news.save()

        # Step 3. Return created news
        return Response(data=NewsSerializer(news).data)



class TagModelViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'


class CategoryListAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination


class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'



@api_view(['GET', 'POST'])
def news_list_api_view(request):
    if request.method == 'GET':
        print(request.user)
        search = request.query_params.get('search', '')
        # 1. Get list of news
        news = News.objects.select_related('category') \
            .prefetch_related('tags', 'news_comments').filter(title__icontains=search)

        # 2. Convert list of news to list of Dictionary
        data = NewsSerializer(instance=news, many=True).data

        # 3. Return Dictionary as JSO
        return Response(data=data)
    elif request.method == 'POST':
        # Step 0. Validation
        serializer = NewsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=400, data=serializer.errors)
        # Step 1. Get data from BODY
        title = serializer.validated_data.get('title') # None
        text = serializer.validated_data.get('text') # None
        amount = serializer.validated_data.get('amount')
        is_active = serializer.validated_data.get('is_active') # T
        category_id = serializer.validated_data.get('category_id')
        tags = serializer.validated_data.get('tags')
        # Step 2. Create news by this data
        news = News.objects.create(
            title=title, text=text,
            view_amount=amount, is_active=is_active,
            category_id=category_id
        )
        news.tags.set(tags)
        news.save()

        # Step 3. Return created news
        return Response(data=NewsSerializer(news).data)


@api_view(['GET', 'PUT', 'DELETE'])
def news_detail_api_view(request, news_id):  # 4
    try:
        news = News.objects.get(id=news_id)
    except News.DoesNotExist:
        return Response(data={'message': 'News object does not exists!'},
                        status=404)
    if request.method == 'GET':
        data = NewsSerializer(instance=news, many=False).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = NewsSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            news.title = request.data.get('title')
            news.category_id = request.data.get('category_id')
            news.text = request.data.get('text')
            news.view_amount = request.data.get('amount')
            news.is_active = request.data.get('is_active')
            news.tags.set(request.data.get('tags'))
            news.save()
            return Response(data=NewsSerializer(news).data)
    else:
        news.delete()
        return Response(status=204)


@api_view(['GET'])
def test_api_view(request):
    dict_ = {
        'text': 'Hello World',
        'int': 1000,
        'float': 9.99,
        'bool': True,
        'list': [1, 2, 3],
        'dict': {
            'key': 'value'
        }
    }
    return Response(data=dict_)
