from .views import MenuView
from django.urls import re_path

app_name = 'app'

urlpatterns = [
    re_path(r'^menu/(?P<path>[a-zA-Z\/]*)/$', MenuView.as_view(), name='menu'),

]
