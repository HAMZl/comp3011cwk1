import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Story
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date

@csrf_exempt
def Login(request):
    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse("Welcome!", content_type="text/plain", status=status.HTTP_200_OK)
        else:
            return HttpResponse("Login failed: Invalid username or password!", content_type="text/plain", status=status.HTTP_401_UNAUTHORIZED)
    return HttpResponse("Login failed!", content_type="text/plain", status=status.HTTP_401_UNAUTHORIZED)

@csrf_exempt
def Logout(request):
    if request.method == "POST":
        logout(request)
        return HttpResponse("Logged Out Successfully!", content_type="text/plain", status=status.HTTP_200_OK)
    return HttpResponse("Logged Out FAILED!", content_type="text/plain", status=503)

@csrf_exempt
def Stories(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            data = json.loads(request.body)
            headline = data.get('headline') 
            category = data.get('category') 
            region = data.get('region') 
            details = data.get('details')
            if category not in ["pol", "art", "tech", "trivia"] and region not in ["uk", "eu", "w"]:
                return HttpResponse("Invalid category or region parameter.", content_type="text/plain", status=503)
            story = Story(headline=headline,category=category,region=region,details=details,author=request.user)
            story.save()
            return HttpResponse("Story Posted Successfully!", content_type="text/plain", status=status.HTTP_201_CREATED) 
        else:
            return HttpResponse("Service Unavailable", content_type="text/plain", status=503)
    elif request.method == "GET":
        story_cat = request.GET.get('story_cat','*')
        story_region = request.GET.get('story_region','*')
        story_date = request.GET.get('story_date', '*')
        
        stories_queryset = Story.objects.all()
        if story_cat != '*':
            if story_cat in ["pol", "art", "tech", "trivia"]:
                stories_queryset = stories_queryset.filter(category=story_cat)
            else:
                return HttpResponse("Invalid story_cat parameter.", content_type="text/plain", status=503)

        if story_region != '*':
            if story_region in ["uk", "eu", "w"]:
                stories_queryset = stories_queryset.filter(region=story_region)
            else:
                return HttpResponse("Invalid story_region parameter.", content_type="text/plain", status=503)

        if story_date != '*':
            parsed_date = parse_date(story_date)
            if parsed_date:
                stories_queryset = stories_queryset.filter(date__gte=parsed_date)
            else:
                return HttpResponse("Invalid date parameter.", content_type="text/plain", status=503)
                
        response_data = [{'key':obj.pk, 'headline':obj.headline,'story_cat':obj.category,'story_region':obj.region, 'author': obj.author.username, 'story_date':obj.date.isoformat(),'story_details': obj.details} for obj in stories_queryset]
        return JsonResponse({"stories": response_data}, status=status.HTTP_200_OK)
    else:
        return HttpResponse("Service Unavailable", content_type="text/plain", status=503)

def Delete(request, pk):
    pass
    if request.user.is_authenticated:
        try:
            story = Story.objects.get(pk=pk, author=request.user)
            story.delete()
            return HttpResponse("Story Deleted Successfully!", content_type="text/plain", status=status.HTTP_200_OK)
        except Story.DoesNotExist:
            return HttpResponse("Service Does Not Exist", content_type="text/plain", status=503)
    else:
        return HttpResponse("Service Unavailable", content_type="text/plain", status=503)
