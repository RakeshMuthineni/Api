# from django.shortcuts import render
# from django.views.generic import TemplateView
#
# from .models import Movie
# from django.http import JsonResponse
#
# # Create your views here.
#
# 
# def Movie_list(request):
#     movie = Movie.objects.all()
#     data ={
#         'movies':list(movie.values())
#     }
#     return JsonResponse(data)
#
# def Movie_details(request,pk):
#     movie = Movie.objects.get(pk=pk)
#
#     data = {
#         'movie' : movie.name,
#         'description':movie.description,
#         'active':movie.active
#     }
#     return JsonResponse(data)