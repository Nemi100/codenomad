from django.shortcuts import render

def index(request):
    """"A view to retun the index page"""
    
    return render(request, 'home/index.html')