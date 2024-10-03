# -*- coding: utf-8 -*-
from django.views.generic import RedirectView
from . import views
from django.conf.urls import url


urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/admin/', permanent=True), name='admin'),
]
