
from django.contrib import admin

from django.urls import path

from django.conf import settings

from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('pages/dashboard.html', views.dashboard, name='dashboard'),
    path('pages/ecozlounge.html', views.ecozlounge, name='ecozlounge'),
    path('pages/dem.html', views.dem, name='dem'),
    # path('generate-plot-data/', views.generate_plot_data, name='generate_plot_data'),
    path('pages/partials/plot.html', views.render_plot, name='render_plot'),
    path('pages/youtube.html', views.youtube_stats_view, name='youtube'),    

]