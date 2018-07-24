from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.urls import reverse, reverse_lazy
from dyno.forms import ContactForm, ImageForm, CrispyModelForm
from django.views.generic.edit import FormView
from PIL import Image
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from dyno.models import Well_Profile, Card_Info, Dysfunction_Profile
from dyno.predict.predict_model import load_keras_model, predict_img
from djangoproject.settings import *
import jwt

#load keras model:
load_keras_model()

# Create your views here.

class home(View):

    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'dyno/home.html')

class dashboard(View):
    @method_decorator(login_required)
    def get(self, request):


        METABASE_SITE_URL = "http://localhost:3000"
        METABASE_SECRET_KEY = "c50834df91e9bcd1e94f8d3626fa4672ed31e33107e3ec592dcc0a85522c6ae5"

        payload = {
          "resource": {"dashboard": 1},
          "params": {

          }
        }
        token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")

        iframeUrl = METABASE_SITE_URL + "/embed/dashboard/" + token.decode("utf8") + "#bordered=true&titled=true"

        return render(request, 'dyno/dashboard.html', {'iframeUrl': iframeUrl})

    @method_decorator(login_required)
    def post(self, request):
        pass #to be added later

class success(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'dyno/success.html')


class diagnose(FormView):

    @method_decorator(login_required)
    def get(self, request):
        form = ImageForm()
        return render(request, 'dyno/diagnose.html', {
            'form': form
            })

    @method_decorator(login_required)
    def post(self, request):
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            predict_img()

            return HttpResponseRedirect(reverse_lazy('dyno:predict_results'))


class well_information(View):
    @method_decorator(login_required)
    def get(self, request):
        form = CrispyModelForm()
        return render(request, 'dyno/well_information.html', {
        'form': form
        })
    @method_decorator(login_required)
    def post(self, request):
        form = CrispyModelForm(request.POST)
        if form.is_valid():
            form.save()

        return HttpResponseRedirect(reverse('dyno:success'))

class predict_results(FormView):

    @method_decorator(login_required)
    def get(self, request):

        img = Card_Info.objects.latest('id')
        img_file = str(img.img_file)           # this section is ghetto
        img_path = os.path.join(MEDIA_URL, img_file)
        return render(request, 'dyno/predict_results.html', {'img':img, 'img_path':img_path})

    @method_decorator(login_required)
    def post(self, request):
        pass
