from django.contrib import admin
from .models import Movie, Category, Review

admin.site.register(Movie)
admin.site.register(Category)
admin.site.register(Review)