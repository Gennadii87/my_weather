from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from .models import CitySearch
from .serializers import HistorySerializer, AllHistorySerializer


@extend_schema(tags=['History'])
class CityAllSearchViewSet(viewsets.ViewSet):
    serializer_class = AllHistorySerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                'order',
                location=OpenApiParameter.QUERY,
                type=str,
                enum=['max', 'min'],
                description='Опциональный параметр для сортировки'
            )
        ],
        summary='Получить статистику по всем городам',
        description='Можно получить статистику запросов по всем городам которые участвовали в поиске',
    )
    @csrf_exempt
    @action(detail=False, methods=['get'], url_path='all-city')
    def all_city_request_counts(self, request):
        order = request.GET.get('order')
        city_searches = CitySearch.objects.all()
        counts = city_searches.values('city_name').annotate(search_count=Sum('search_count'))

        if order == 'max':
            counts = counts.order_by('-search_count')

        elif order == 'min':
            counts = counts.order_by('search_count')

        return Response(list(counts), status=status.HTTP_200_OK)


@extend_schema(tags=['History'])
class CitySearchViewSet(viewsets.ViewSet):
    serializer_class = HistorySerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                'city_name',
                location=OpenApiParameter.QUERY,
                type=str,
                many=False,
                required=True,
            )
        ],
        summary='Получить количество запросов по конкретному городу',
        description='Необходимо указать название города',
    )
    @csrf_exempt
    @action(detail=False, methods=['get'], url_path='city')
    def city_request_count(self, request):
        city_name = request.GET.get('city_name')
        if city_name:
            city_search = CitySearch.objects.filter(city_name=city_name).aggregate(search_count=Sum('search_count'))
            count = city_search['search_count'] if city_search['search_count'] is not None else 0
            return Response({'city_name': city_name, 'count': count}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'city_name parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
