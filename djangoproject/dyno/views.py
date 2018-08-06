from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.urls import reverse, reverse_lazy
from dyno.forms import ContactForm, ImageForm, CrispyModelForm, DirectoryForm, CrispyDysfunctionModelForm
from django.views.generic.edit import FormView
from PIL import Image
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from dyno.models import Well_Profile, Card_Info, Dysfunction_Profile
from dyno.predict.predict_model import load_keras_model, predict_img, analyze_directory, predict_from_directory
from django.views.decorators.csrf import csrf_exempt
from djangoproject.settings import *
import jwt

#load keras model:
#load_keras_model()

# Create your views here.

class home(View):

    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'dyno/home.html')

class dashboard(View):
    @method_decorator(login_required)
    def get(self, request):

        METABASE_SITE_URL = "https://dyno-metabase.herokuapp.com"
        METABASE_SECRET_KEY = "e357b3b54f5c59de60d890b532b5556049f7ef19e445beb0abfee57afd8782d1"

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
        dys_1 = Dysfunction_Profile.objects.get(dys_name="Good")
        dys_2 = Dysfunction_Profile.objects.get(dys_name="Bad")
        METABASE_SITE_URL = "http://localhost:3000"
        METABASE_SECRET_KEY = "c50834df91e9bcd1e94f8d3626fa4672ed31e33107e3ec592dcc0a85522c6ae5"

        payload = {
          "resource": {"dashboard": 2},
          "params": {

          }
        }
        token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")

        iframeUrl = METABASE_SITE_URL + "/embed/dashboard/" + token.decode("utf8") + "#bordered=true&titled=true"

        return render(request, 'dyno/predict_results.html', {'img':img, 'img_path':img_path, 'iframeUrl':iframeUrl, 'dys_1': dys_1, 'dys_2': dys_2})

    @method_decorator(login_required)
    def post(self, request):
        pass

class command_center(View):

    @method_decorator(login_required)
    def get(self, request):
        form = DirectoryForm()

        METABASE_SITE_URL = "http://dyno-metabase.herokuapp.com"
        METABASE_SECRET_KEY = "e357b3b54f5c59de60d890b532b5556049f7ef19e445beb0abfee57afd8782d1"

        payload = {
          "resource": {"question": 3},
          "params": {
            
          }
        }
        token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")

        iframeUrl = METABASE_SITE_URL + "/embed/question/" + token.decode("utf8") + "#bordered=true&titled=true"

        return render(request, 'dyno/command_center.html', {'form':form, 'iframeUrl':iframeUrl})

    @method_decorator(login_required)
    def post(self, request):
        form = DirectoryForm(request.POST)
        if form.is_valid():

            input_directory = (form.cleaned_data['input_dir'])
            well_name = (form.cleaned_data['well_name'])
            request.session['input_directory'] = input_directory
            request.session['analyze_results'] = analyze_directory(
                                                input_directory,
                                                well_name
                                                )

            return HttpResponseRedirect(reverse_lazy('dyno:checkpoint'))

class checkpoint(View):

    @method_decorator(login_required)
    def get(self, request):
        num_files, well_name, SAVE_DIR = request.session['analyze_results']

        return render(request, 'dyno/checkpoint.html', {
                                                        'num_files':num_files,
                                                        'well_name':well_name,
                                                        'SAVE_DIR':SAVE_DIR})

    @method_decorator(login_required)
    def post(self, request):
        input_directory = request.session['input_directory']
        num_files, well_name, SAVE_DIR = request.session['analyze_results']

        predict_from_directory(input_directory, well_name)

        # del request.session['input_directory','analyze_resukts','well'] should we delete session??

        return HttpResponseRedirect(reverse_lazy('dyno:predict_results'))

class dysfunction(View):
    @method_decorator(login_required)
    def get(self, request):
        form = CrispyDysfunctionModelForm()
        return render(request, 'dyno/dysfunction_profile.html', {
        'form': form
        })

    @method_decorator(login_required)
    def post(self, request):
        form = CrispyDysfunctionModelForm(request.POST)
        if form.is_valid():
            form.save()

        return HttpResponseRedirect(reverse('dyno:success'))
