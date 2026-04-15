# from django.shortcuts import render

# from django.http import HttpResponse
# def index(request):
#     return HttpResponse("Hello, world!")

# from django.http import HttpResponse

from django.shortcuts import render
from django.http import HttpResponse
from .models import Book
from django.db.models import Q, Count, Sum, Avg, Max, Min
from .models import Book, Student, Address


# #Use the constructor function
# mybook = Book(title = 'Continuous Delivery', author = 'J.Humble and D. Farley', edition = 1)
# mybook.save()
# #Use the create function
# mybook1 = Book.objects.create(title = 'Continuous Delivery11', author = 'J.Humble and D. Farley11', edition = 5)
# mybook1.save()

# def index(request):
#     name = request.GET.get("name") or "world!"  #add this line
#     return HttpResponse("Hello, "+name) #replace the word “world!” with the variable name

# def index(request): 
#     name = request.GET.get("name") or "world!"
#     return render(request, "bookmodule/index.html")    #Change HttpResponse  to render function

def index(request):
    name = request.GET.get("name") or "world!"
    
    return render(request, "bookmodule/index.html" , {"name": name})  #your render line

def index2(request, val1 = 0):   #add the view function (index2)
    return HttpResponse("value1 = "+str(val1))

def viewbook(request, bookId):
    # assume that we have the following books somewhere (e.g. database)
    book1 = {'id':123, 'title':'Continuous Delivery', 'author':'J. Humble and D. Farley'}
    book2 = {'id':456, 'title':'Secrets of Reverse Engineering', 'author':'E. Eilam'}
    targetBook = None
    if book1['id'] == bookId: targetBook = book1
    if book2['id'] == bookId: targetBook = book2
    context = {'book':targetBook} # book is the variable name accessible by the template
    return render(request, 'bookmodule/show.html', context)

# def index(request):
#     return render(request, "bookmodule/index.html")
 
def list_books(request):
    return render(request, 'bookmodule/list_books.html')
 
# def viewbook(request, bookId):
#     return render(request, 'bookmodule/one_book.html')
 
def aboutus(request):
    return render(request, 'bookmodule/aboutus.html')

def links(request):
    return render(request,"bookmodule/links.html")

def formatting(request):
    return render(request,"bookmodule/formatting.html")

def listing(request):
    return render(request,"bookmodule/listing.html")

def tables(request):
    return render(request,"bookmodule/tables.html")

# --------- Lab 6 ---------

# Task 1

# def search_books(request):
#     return render(request, 'bookmodule/search.html')

# Task 2

def __getBooksList():
    book1 = {'id':12344321, 'title':'Continuous Delivery', 'author':'J.Humble and D. Farley'}
    book2 = {'id':56788765,'title':'Reversing: Secrets of Reverse Engineering', 'author':'E. Eilam'}
    book3 = {'id':43211234, 'title':'The Hundred-Page Machine Learning Book', 'author':'Andriy Burkov'}
    return [book1, book2, book3]

def search_books(request):
    if request.method == "POST":
        string = request.POST.get('keyword').lower()
        isTitle = request.POST.get('option1')
        isAuthor = request.POST.get('option2')

        books = __getBooksList()
        newBooks = []

        for item in books:
            contained = False

            if isTitle and string in item['title'].lower():
                contained = True

            if not contained and isAuthor and string in item['author'].lower():
                contained = True

            if contained:
                newBooks.append(item)

        return render(request, 'bookmodule/bookList.html', {'books': newBooks})

    return render(request, 'bookmodule/search.html')

# Lab 7

def simple_query(request):
    mybooks=Book.objects.filter(title__icontains='Continuous') # <- multiple objects
    return render(request, 'bookmodule/bookList.html', {'books':mybooks})

def complex_query(request):
    mybooks=books=Book.objects.filter(author__isnull = False).filter(title__icontains='Continuous').filter(edition__gte = 2).exclude(price__lte = 100)[:10]
    if len(mybooks)>=1:
        return render(request, 'bookmodule/bookList.html', {'books':mybooks})
    else:
        return render(request, 'bookmodule/index.html')

# Lab 8

# Task 1
def task1(request):
    books = Book.objects.filter(Q(price__lte=80))
    return render(request, 'bookmodule/task1.html', {'books': books})

# Task 2
def task2(request):
    books = Book.objects.filter(
        Q(edition__gt=3) & (Q(title__icontains='qu') | Q(author__icontains='qu'))
    )
    return render(request, 'bookmodule/task2.html', {'books': books})

# Task 3
def task3(request):
    books = Book.objects.filter(
        Q(edition__lte=3) & ~(Q(title__icontains='qu') | Q(author__icontains='qu'))
    )
    return render(request, 'bookmodule/task3.html', {'books': books})

# Task 4
def task4(request):
    books = Book.objects.all().order_by('title')
    return render(request, 'bookmodule/task4.html', {'books': books})

# Task 5
def task5(request):
    stats = Book.objects.aggregate(
        total_books=Count('id'),
        total_price=Sum('price'),
        avg_price=Avg('price'),
        max_price=Max('price'),
        min_price=Min('price')
    )
    return render(request, 'bookmodule/task5.html', {'stats': stats})

# Task 7
def task7(request):
    data = Student.objects.values('address__city').annotate(count=Count('id'))
    return render(request, 'bookmodule/task7.html', {'data': data})


# http://127.0.0.1:8000/books/lab8/task1
# http://127.0.0.1:8000/books/lab8/task2
# http://127.0.0.1:8000/books/lab8/task3
# http://127.0.0.1:8000/books/lab8/task4
# http://127.0.0.1:8000/books/lab8/task5
# http://127.0.0.1:8000/books/lab8/task7