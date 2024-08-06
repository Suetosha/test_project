from .views import MenuView
from django.urls import path

app_name = 'app'

urlpatterns = [
    path('', MenuView.as_view(), name='menu'),

]
