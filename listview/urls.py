from django.urls import path, include
from . import views
from .views import Delete, Update


urlpatterns = [
    path('', views.index, name = "Home"),
    path('example/', views.example, name = "example"),
    # path('login/', views.login, name = "Login"),
    path('signup/', views.signup, name = "Signup"),
    path('delete_record/', Delete.as_view(), name='delete-record'),
    path('delete_user/', views.delete_user, name='delete-user'),
    path('<int:id/', Update.as_view(), name = 'update-record'),
    path('update_record', views.editRecord, name = "Update"),
    path('autocomplete/', views.autocomplete, name="autocomplete"),
    path('autocomplete_user/', views.autocomplete_user, name="autocomplete-user"),
    path('autofill', views.autofill, name = 'autofill'),
    path('massmail', views.massmail, name = 'massmail'),
    path('filter', views.filter, name="filter"),
    path('create_user', views.createUser, name="create_user"),
    path('users/', views.users, name = "Users"),
    path('exportcsv', views.exportcsv, name = "export-csv"),
    path('update_linkedin_data/', views.update_linkedin_data, name = "export-csv"),
]