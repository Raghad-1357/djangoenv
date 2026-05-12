from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Book, Student2, Profile
from django.db.models import Q, Count, Sum, Avg, Max, Min
from .models import *
from .forms import *

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required


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


# ------------- LAB 9 ------------- 

# Task 1: Books with percentage availability (Transient Field)
def lab9_task1(request):
    books = Book.objects.all()
    total_books_count = books.count()
    
    for book in books:
        if total_books_count > 0:
            book.availability_pct = (book.quantity / total_books_count) * 100 
        else:
            book.availability_pct = 0
            
    return render(request, 'bookmodule/lab9_task1.html', {'books': books})


# Task 2: Publishers with total book stock (Annotate)
def lab9_task2(request):
    publishers = Publisher.objects.annotate(total_stock=Count('book')) 
    return render(request, 'bookmodule/lab9_task2.html', {'publishers': publishers})


# Task 3: Oldest book for each publisher
def lab9_task3(request):
    publishers = Publisher.objects.annotate(oldest_book_date=Min('book__pubdate')) 
    return render(request, 'bookmodule/lab9_task3.html', {'publishers': publishers})


# Task 4: Average, Min, and Max price per publisher
def lab9_task4(request):
    publishers = Publisher.objects.annotate(
        avg_price=Avg('book__price'),
        min_price=Min('book__price'),
        max_price=Max('book__price')
    ) 
    return render(request, 'bookmodule/lab9_task4.html', {'publishers': publishers})


# Task 5: Publishers with count of highly rated books
def lab9_task5(request):
    publishers = Publisher.objects.annotate(
        highly_rated_count=Count('book', filter=Q(book__rating__gte=4))
    ) 
    return render(request, 'bookmodule/lab9_task5.html', {'publishers': publishers})


# Task 6: Complex filtering with annotations
def lab9_task6(request):
    publishers = Publisher.objects.annotate(
        filtered_book_count=Count('book', filter=Q(
            book__price__gt=50, 
            book__quantity__lt=5, 
            book__quantity__gte=1
        ))
    ) 
    return render(request, 'bookmodule/lab9_task6.html', {'publishers': publishers})


# -----------------LAB 10-----------------

# Task 1: قائمة الكتب
def list_books_v1(request):
    books = Book.objects.all()
    return render(request, 'bookmodule/lab10_list_books.html', {'books': books})

# Task 2: إضافة كتاب جديد
def add_book_v1(request):
    if request.method == "POST":
        title = request.POST.get('title')
        author = request.POST.get('author')
        price = request.POST.get('price')
        Book.objects.create(title=title, author=author, price=price)
        return redirect('list_books_v1')
    return render(request, 'bookmodule/lab10_add_book.html')

# Task 3: تعديل كتاب
def edit_book_v1(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == "POST":
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.price = request.POST.get('price')
        book.save()
        return redirect('list_books_v1')
    return render(request, 'bookmodule/lab10_edit_book.html', {'book': book})

# Task 4: حذف كتاب
def delete_book_v1(request, id):
    book = get_object_or_404(Book, id=id)
    book.delete()
    return redirect('list_books_v1')

# ------------------Part 2------------------

# Task 1 (Part 2): القائمة
def list_books_v2(request):
    books = Book.objects.all()
    return render(request, 'bookmodule/list_books_v2.html', {'books': books})

# Task 2 (Part 2): إضافة باستخدام Form
def add_book_v2(request):
    form = BookForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('list_books_v2')
    return render(request, 'bookmodule/form_book.html', {'form': form, 'title': 'إضافة كتاب جديد'})

# Task 3 (Part 2): تعديل باستخدام Form
def edit_book_v2(request, id):
    book = get_object_or_404(Book, id=id)
    form = BookForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        return redirect('list_books_v2')
    return render(request, 'bookmodule/form_book.html', {'form': form, 'title': 'تعديل الكتاب'})

# Task 3 (Part 2): حذف باستخدام Form
def delete_book_v2(request, id):
    book = get_object_or_404(Book, id=id)
    book.delete()
    return redirect('list_books_v2')



# -----------------LAB 11-----------------
# ----------- Task 1 -----------

@login_required(login_url='login')
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'bookmodule/lab11/form_student.html', {'form': form})


@login_required(login_url='login')
def student_list_view(request):
    students = Student.objects.all()
    return render(request, 'bookmodule/lab11/student_list.html', {'students': students})


@login_required(login_url='login')
def edit_student(request, id):
    students = get_object_or_404(Student, id=id)
    form = StudentForm(request.POST or None, instance=students)
    if form.is_valid():
        form.save()
        return redirect('student_list')
    return render(request, 'bookmodule/lab11/form_student.html', {'form': form, 'title': 'تعديل الطالب'})

@login_required(login_url='login')
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    return redirect('student_list')

# ----------- Task 2 -----------

@login_required(login_url='login')
def add_student2(request):
    if request.method == 'POST':
        form = Student2Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list2')
    else:
        form = Student2Form()
    return render(request, 'bookmodule/lab11/form_student_task2.html', {'form': form})

@login_required(login_url='login')
def student_list_view2(request):
    students = Student2.objects.all()
    return render(request, 'bookmodule/lab11/student_list_task2.html', {'students': students})

@login_required(login_url='login')
def edit_student2(request, id):
    student = get_object_or_404(Student2, id=id)
    form = Student2Form(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        return redirect('student_list2')
    return render(request, 'bookmodule/lab11/form_student_task2.html', {'form': form, 'title': 'تعديل الطالب'})

@login_required(login_url='login')
def delete_student2(request, id):
    student = get_object_or_404(Student2, id=id)
    student.delete()
    return redirect('student_list2')

# ----------- Task 3 -----------

@login_required(login_url='login')
def profile_list_view(request):
    profiles = Profile.objects.all()
    return render(request, 'bookmodule/lab11/profile_list.html', {'profiles': profiles})

# دالة إضافة بروفايل مع صورة (File Handling)
@login_required(login_url='login') 
def add_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('profile_list')
    else:
        form = ProfileForm()
    return render(request, 'bookmodule/lab11/add_profile.html', {'form': form})


# -----------------LAB 12-----------------

# Task 1: التسجيل
def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم التسجيل بنجاح! يمكنك الآن تسجيل الدخول.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'bookmodule/lab12/register.html', {'form': form})

# Task 2: تسجيل الدخول
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.info(request, f'مرحباً بك، {user.username}!')
            return redirect('student_list') 
        else:
            messages.error(request, 'خطأ في اسم المستخدم أو كلمة المرور.')
    else:
        form = AuthenticationForm()
    return render(request, 'bookmodule/lab12/login.html', {'form': form})

# Task 4: تسجيل الخروج
def logout_user(request):
    logout(request)
    messages.warning(request, 'لقد سجلت الخروج.')
    return redirect('login')

