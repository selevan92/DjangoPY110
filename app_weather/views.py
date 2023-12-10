from django.shortcuts import render
from django.http import JsonResponse
from weather_api import current_weather


# Create your views here.
def my_view(request):
    if request.method == "GET":
        return JsonResponse(current_weather(59.93, 30.31),
                            json_dumps_params={'indent': 4, 'ensure_ascii': False})
