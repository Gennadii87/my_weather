from django.db import models


class CitySearch(models.Model):

    session_key = models.CharField(max_length=40)
    city_name = models.CharField(max_length=255)
    search_count = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Город {self.city_name} - искали {self.search_count} раз"
