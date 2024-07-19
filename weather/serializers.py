from rest_framework import serializers

from weather.models import CitySearch


class AllHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CitySearch
        fields = ('city_name', 'search_count')


class HistorySerializer(serializers.Serializer):
    city_name = serializers.CharField(write_only=True, help_text='Название города')
    count = serializers.IntegerField(help_text='Количество запросов')
