from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.db.models import Avg
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import  AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login, logout

from .models import Movie, Category, Review, Rating, Genre
from .forms import MovieForm

def index(request):
    movies = Movie.objects.all()
    return render(request, 'index.html', {'movies': movies})



def register(request):
    if request.method=='POST':
        username=request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['password1']
        if password==cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request,'username taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'email taken')
                return redirect('register')
            else:
                user=User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
                user.save();
                return redirect('login')

        else:
            messages.info(request,'password not matching')

            return redirect('index')
    return render(request,'register.html')

def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)  # Bind form data
        if form.is_valid():  # Validate form data
            movie = form.save(commit=False)  # Save movie object without committing to the database
            movie.added_by = request.user  # Set the user who added the movie
            movie.save()  # Save the movie object to the database
            return redirect('index')  # Redirect to index page after saving the movie
    else:
        form = MovieForm()  # Create a new instance of the MovieForm
    categories = Category.objects.all()  # Fetch all categories
    return render(request, 'add_movie.html', {'form': form, 'categories': categories})

def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Category.objects.create(name=name)
        return redirect('index')
    return render(request, 'add_movie.html')

def movie_details(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    movie = Movie.objects.get(pk=movie_id)
    average_rating = Rating.objects.filter(movie=movie).aggregate(Avg('value'))['value__avg']
    return render(request, 'movie_details.html', {'movie': movie, 'average_rating': average_rating})

def genre_list(request):
    genres = Genre.objects.all()
    return render(request, 'genre_list.html', {'genres': genres})

def movies_genre(request, genre_id):
    genre = get_object_or_404(Genre, pk=genre_id)
    movies = Movie.objects.filter(genres=genre)
    return render(request, 'movies_genre.html', {'genre': genre, 'movies': movies})

def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        if request.user == movie.added_by:
            movie.delete()
            return redirect('index')  # Redirect after deletion
    return render(request, 'delete_movie.html', {'movie': movie})

def submit_review(request, movie_id):
    if request.method == 'POST':
        movie = Movie.objects.get(pk=movie_id)
        rating_value = int(request.POST.get('rating'))
        review_text = request.POST.get('review_text')
        review = Review.objects.create(user=request.user, movie=movie, text=review_text)
        rating = Rating.objects.create(user=request.user, movie=movie, value=rating_value)
        return redirect('movie_details', movie_id=movie_id)
    else:
        return redirect('index')  # Redirect if not a POST request or if the user is not logged in

def movie_list(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')

    movies = Movie.objects.all()

    if query:
        movies = movies.filter(title__icontains=query)

    if category_id:
        # Get the category object based on the category_id
        category = Category.objects.filter(id=category_id).first()
        if category:
            # Filter movies by the selected category
            movies = movies.filter(category=category)

    categories = Category.objects.all()  # Fetch all categories for the dropdown

    return render(request, 'movie_list.html', {'movies': movies, 'query': query, 'categories': categories})
def delete_user(request, user_id):
    User.objects.get(id=user_id).delete()
    return redirect('index')

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)  # Correct usage of login function
                return redirect('index')  # Redirect authenticated users to index page
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    auth.logout(request)
    return redirect('index')