from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('index2/<int:val1>/', views.index2),
    path('<int:bookId>', views.viewbook),
    path('', views.index, name= "books.index"),
    path('list_books/', views.list_books, name= "books.list_books"),
    path('<int:bookId>/', views.viewbook, name="books.view_one_book"),
    path('aboutus/', views.aboutus, name="books.aboutus"),
    path('html5/links/', views.links, name="books.links"),
    path('html5/text/formatting/', views.formatting, name="books.formatting"),
    path('html5/listing/', views.listing, name="books.listing"),
    path('search', views.search_books),
    path('simple/query', views.simple_query, name='simple_query'),
    path('complex/query', views.complex_query, name='complex_query'),
    
    path('lab8/task1', views.task1),  
    path('lab8/task2', views.task2),
    path('lab8/task3', views.task3),
    path('lab8/task4', views.task4),
    path('lab8/task5', views.task5),
    path('lab8/task7', views.task7),

    path('lab9/Lab9_task1', views.lab9_task1),
    path('lab9/Lab9_task2', views.lab9_task2),
    path('lab9/Lab9_task3', views.lab9_task3),
    path('lab9/Lab9_task4', views.lab9_task4),
    path('lab9/Lab9_task5', views.lab9_task5),
    path('lab9/Lab9_task6', views.lab9_task6),

# ----------LAB 10-----------
    path('lab10_part1/list_books', views.list_books_v1, name='list_books_v1'),
    path('lab10_part1/add_book', views.add_book_v1, name='add_book_v1'),
    path('lab10_part1/edit_book/<int:id>', views.edit_book_v1, name='edit_book_v1'),
    path('lab10_part1/delete_book/<int:id>', views.delete_book_v1, name='delete_book_v1'),

    path('lab10_part2/listbooks', views.list_books_v2, name='list_books_v2'),
    path('lab10_part2/addbook', views.add_book_v2, name='add_book_v2'),
    path('lab10_part2/editbook/<int:id>', views.edit_book_v2, name='edit_book_v2'),
    path('lab10_part2/deletebook/<int:id>', views.delete_book_v2, name='delete_book_v2'),


# ----------LAB 11-----------

    path('lab11/addStudent', views.add_student, name='add_student'),
    path('lab11/addStudent2', views.add_student2, name='add_student2'),
    path('lab11/addProfile', views.add_profile, name='add_profile'),
    path('lab11/students', views.student_list_view, name='student_list'),
    path('lab11/students2', views.student_list_view2, name='student_list2'),
    path('lab11/profiles', views.profile_list_view, name='profile_list'),
    path('lab11/editStudent/<int:id>', views.edit_student, name='edit_student'),
    path('lab11/editStudent2/<int:id>', views.edit_student2, name='edit_student2'),
    path('lab11/deleteStudent/<int:id>', views.delete_student, name='delete_student'),
    path('lab11/deleteStudent2/<int:id>', views.delete_student2, name='delete_student2'),

# ----------LAB 12-----------

    path('users/register/', views.register_user, name='register'),
    path('users/login/', views.login_user, name='login'),
    path('users/logout/', views.logout_user, name='logout'),

]
