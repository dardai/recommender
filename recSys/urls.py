
from django.conf.urls import url
from .import views
urlpatterns = [
    url(r'^$',views.test_index,name="test_index")
]
