from rest_framework.decorators import api_view  # [GET, POST, PUT, DELETE]
from rest_framework.response import Response  # Return Result
from main.serializers import NewsSerializer
from main.models import News


@api_view(['GET', 'POST'])
def news_list_api_view(request):
    if request.method == 'GET':
        search = request.query_params.get('search', '')
        # 1. Get list of news
        news = News.objects.select_related('category') \
            .prefetch_related('tags', 'news_comments').filter(title__icontains=search)

        # 2. Convert list of news to list of Dictionary
        data = NewsSerializer(instance=news, many=True).data

        # 3. Return Dictionary as JSON
        return Response(data=data)
    elif request.method == 'POST':
        # Step 1. Get data from BODY
        title = request.data.get('title')
        text = request.data.get('text')
        amount = request.data.get('amount')
        is_active = request.data.get('is_active')
        category_id = request.data.get('category_id')
        tags = request.data.get('tags')
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
