from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('add_movie/', views.add_movie, name='add_movie'),
    path('add_category/', views.add_category, name='add_category'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('movies/<int:movie_id>/', views.movie_details, name='movie_details'),
    path('movies/<int:movie_id>/delete/', views.delete_movie, name='delete_movie'),
    path('movies/<int:movie_id>/submit_review/', views.submit_review, name='submit_review'),
    path('genres/', views.genre_list, name='genre_list'),
    path('genres/<int:genre_id>/', views.movies_genre, name='movies_genre'),
    path('movies/', views.movie_list, name='movie_list'),

]