from django.urls import path
from . import views

app_name = "polls"
urlpatterns = [
    #ex: /polls
    path("", views.IndexView.as_view(), name="index"),
    # ex: /polls/5/
    path("<int:pk>/",views.DetailView.as_view(),name = "detail"),
    #ex:/polls/5/results/
    path("<int:pk>/results/",views.ResultsView.as_view(),name = 'results'),
     #ex:/polls/5/votes/
    path("<int:question_id>/vote/",views.vote,name = "vote"),
    path('add_question/', views.add_question, name='add_question'),
    path('add_question/polls/success_page/', views.success_page, name='success_page'),
    path('<int:question_id>/update/',views.update_question,name='update_question'),
    path('<int:question_id>/', views.success_page, name='detail'),
    path('<int:question_id>/delete',views.delete_question,name ='delete_question'),
    path('<int:question_id>/delete_choice/<int:choice_id>/',views.delete_choice,name = 'delete_choice')
]