from .views import MenuView
from django.urls import re_path, path

app_name = 'app'

urlpatterns = [
    path('', MenuView.as_view(), name='menu'),
    re_path(r'^(?P<menu>[^/]+)/(?P<path>[a-zA-Z\/ 0-9]*)?/$', MenuView.as_view(), name='menu'),

]
