from django.urls import path

from . import views

from dyno.views import home, success
from dyno.views import dashboard, diagnose, well_information, predict_results
from django.conf import settings
from django.conf.urls.static import static


app_name = 'dyno'
urlpatterns = [
    # starting view, has list of all other links
    path('home', home.as_view(), name='home'),
    path('success', success.as_view(), name = 'success'),
    path('dashboard', dashboard.as_view(), name = 'dashboard'),
    path('diagnose', diagnose.as_view(), name = 'diagnose'),
    path('well_information', well_information.as_view(), name = 'well_information'),
    path('predict_results', predict_results.as_view(), name = 'predict_results'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
