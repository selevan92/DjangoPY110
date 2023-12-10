from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render
from .models import DATABASE
# Create your views here.

def product_view(request):
    if request.method == 'GET':
        return JsonResponse(DATABASE, json_dumps_params={'indent': 4, 'ensure_ascii': False})

def show_view(request):
    if request.method == 'GET':
        with open('store/shop.html', 'r', encoding='utf-8') as f:
            return HttpResponse(f)
