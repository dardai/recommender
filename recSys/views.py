import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from django.http import JsonResponse

# Create your views here.

def test_index(request):
    blogs = '欢迎来到智能推荐系统'
    print (request.GET)
    #if 'q' in request.GET:
    #    message = 'search ' + request.GET['q']
    #else:
    #    message = '空表单'
    return JsonResponse({'res':1,'name':'推荐系统'},json_dumps_params={'ensure_ascii':False})
    #return HttpResponse(message)
   # return  render(request,"recommend/testIndex.html",{"rec":blogs})

