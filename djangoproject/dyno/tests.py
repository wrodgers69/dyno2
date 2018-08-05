from django.test import TestCase

# Create your tests here.
import datetime
from django.utils import timezone
from .models import Card_Info, Well_Profile, Dysfunction_Profile
from django.test import Client
from django.contrib.auth.models import User
import unittest
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy


#class ModelReturnTests(TestCase):

#    def create_well_profile(self, well_name="test well"):
#        return Well_Profile.objects.create(well_name=well_name)

#    def create_card_info(self, title="only a test", associated_well_profile="test well"):
#        return Card_Info.objects.create(title=title, associated_well_profile=associated_well_profile)

#    def test_card_info_Creation(self):
#        w = self.create_card_info()
#        self.assertTrue(isinstance(w, Card_Info))
#        self.assertEqual(w.__unicode__(), w.title)


class ModelTests(TestCase):

    #test if date outside of "recent" window passes (future)
    def test_date_created_in_future(self):
        time = timezone.now() + datetime.timedelta(days=1)
        future_date = Well_Profile(date_created=time)
        self.assertIs(future_date.was_created_recently(), False)

    #test date inside of "recent" time window
    def test_date_creatd_recently(self):
        time = timezone.now() + datetime.timedelta(days=-0.5)
        createdate = Well_Profile(date_created=time)
        self.assertIs(createdate.was_created_recently(), True)

    #test date outside of "recent" time window (older)
    def test_date_created_in_past(self):
        time = timezone.now() + datetime.timedelta(days=-5)
        past_date = Well_Profile(date_created=time)
        self.assertIs(past_date.was_created_recently(), False)




    def test_date_created_in_future2(self):
        time = timezone.now() + datetime.timedelta(days=1)
        future_date = Card_Info(date_upload=time)
        self.assertIs(future_date.was_created_recently(), False)

    #test date inside of "recent" time window
    def test_date_creatd_recently2(self):
        time = timezone.now() + datetime.timedelta(days=-0.5)
        createdate = Card_Info(date_upload=time)
        self.assertIs(createdate.was_created_recently(), True)

    #test date outside of "recent" time window (older)
    def test_date_created_in_past2(self):
        time = timezone.now() + datetime.timedelta(days=-5)
        past_date = Card_Info(date_upload=time)
        self.assertIs(past_date.was_created_recently(), False)





    #model = Card_Info
    #test date inside of "recent" time window
    def test_date_mod_recently(self):
        time = timezone.now() + datetime.timedelta(days=-0.1)
        recent_mod = Card_Info(date_updated=time)
        self.assertIs(recent_mod.was_updated_recently(), True)

    #model = Card_Info
    #test if date outside of "recent" window passes (future)
    def test_date_mod_future(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_date = Card_Info(date_updated=time)
        self.assertIs(future_date.was_updated_recently(), False)

    #model = Card_Info
    #test date outside of "recent" time window (older)
    def test_mod_past(self):
        time = timezone.now() + datetime.timedelta(days=-5)
        past_date = Card_Info(date_updated=time)
        self.assertIs(past_date.was_updated_recently(), False)




    #Test last_well_test value cannot be greater than designed total
    def test_production_out_of_range(self):
        design = 1
        actual= 1.1
        prod = Well_Profile(designed_total_prod=design, last_well_test=actual)
        self.assertIs(prod.production_check(), False)

    #Test last_well_test value is okay < designed total.
    def test_prod_in_range(self):
        prod = Well_Profile(designed_total_prod=100, last_well_test=50)
        self.assertIs(prod.production_check(), True)

    #test values cannot be negative
    def test_negative_values(self):
        prod = Well_Profile(last_well_test=-1, designed_total_prod=100)
        self.assertIs(prod.production_check(), False)


    #Test saving date function, in range.
#    def test_date_save_fn(self):
#        now = timezone.now()
#        previously = timezone.now() + datetime.timedelta(days=-.5)
#        new = Well_Profile(well_name="test 1h", date_created=previously, date_updated=now)
#        new.save()
#        self.assertIs(new.save(), True)

class Test_Well_Information(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        #creating client instance
        self.client = Client()
        self.user = User.objects.create_user('wade','wade@wade.com','p@ssword')

    def test_well_information_view_login(self):
        self.client.login(username='wade', password='p@ssword')
        response = self.client.get(reverse_lazy('dyno:well_information'))
        #check for reponse is 200 okself.
        self.assertEqual(response.status_code, 200)

class Test_Home_View(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.client = Client()
        self.user = User.objects.create_user('lee', 'wade@wade.com', 'p@ssword')

    def test_home_view_login(self):
        self.client.login(username='lee', password='p@ssword')
        response = self.client.get(reverse_lazy('dyno:home'))
        self.assertEqual(response.status_code, 200)

class Test_Home_View_Fails(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.client = Client()
        #self.user = User.objects.create_user('lee', 'wade@wade.com', 'p@ssword')

    def test_home_view_login(self):
        #self.client.login(username='lee', password='p@ssword')
        response = self.client.get(reverse_lazy('dyno:home'))
        self.assertEqual(response.status_code, 302)

class Test_Well_Information_View_Fails(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.client = Client()
        #self.user = User.objects.create_user('lee', 'wade@wade.com', 'p@ssword')

    def test_home_view_login(self):
        #self.client.login(username='lee', password='p@ssword')
        response = self.client.get(reverse_lazy('dyno:well_information'))
        self.assertEqual(response.status_code, 302)

class Test_Success_View(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.client = Client()
        self.user = User.objects.create_user('james', 'wade@wade.com', 'p@ssword')

    def test_home_view_login(self):
        self.client.login(username='james', password='p@ssword')
        response = self.client.get(reverse_lazy('dyno:success'))
        self.assertEqual(response.status_code, 200)

class Test_Success_View_Fails(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.client = Client()
        #self.user = User.objects.create_user('lee', 'wade@wade.com', 'p@ssword')

    def test_home_view_login(self):
        #self.client.login(username='lee', password='p@ssword')
        response = self.client.get(reverse_lazy('dyno:success'))
        self.assertEqual(response.status_code, 302)

class Test_Diagnose_View(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.client = Client()
        self.user = User.objects.create_user('wade2', 'wade@wade.com', 'p@ssword')

    def test_home_view_login(self):
        self.client.login(username='wade2', password='p@ssword')
        response = self.client.get(reverse_lazy('dyno:diagnose'))
        self.assertEqual(response.status_code, 200)

class Test_Diagnose_View_Fails(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.client = Client()
        #self.user = User.objects.create_user('lee', 'wade@wade.com', 'p@ssword')

    def test_home_view_login(self):
        #self.client.login(username='lee', password='p@ssword')
        response = self.client.get(reverse_lazy('dyno:diagnose'))
        self.assertEqual(response.status_code, 302)

class Test_PredictResults_View(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.client = Client()
        self.user = User.objects.create_user('wade3', 'wade@wade.com', 'p@ssword')
        well = Well_Profile.objects.create(well_name='test well 1')
        card = Card_Info.objects.create(associated_well_profile=well, title='test card', img_file='test image', prediction='good')

    def test_home_view_login(self):
        self.client.login(username='wade3', password='p@ssword')
        response = self.client.get(reverse_lazy('dyno:predict_results'))
        self.assertEqual(response.status_code, 200)

class Test_PredictResults_View_Fails(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.client = Client()
        #self.user = User.objects.create_user('lee', 'wade@wade.com', 'p@ssword')

    def test_home_view_login(self):
        #self.client.login(username='lee', password='p@ssword')
        response = self.client.get(reverse_lazy('dyno:predict_results'))
        self.assertEqual(response.status_code, 302)


class Test_Dashboard_View(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.client = Client()
        self.user = User.objects.create_user('wade4', 'wade@wade.com', 'p@ssword')
        well = Well_Profile.objects.create(well_name='test well 1')
        card = Card_Info.objects.create(associated_well_profile=well, title='test card', img_file='test image', prediction='good')

    def test_home_view_login(self):
        self.client.login(username='wade4', password='p@ssword')
        response = self.client.get(reverse_lazy('dyno:dashboard'))
        self.assertEqual(response.status_code, 200)

class Test_Dashboard_View_Fails(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.client = Client()
        #self.user = User.objects.create_user('lee', 'wade@wade.com', 'p@ssword')

    def test_home_view_login(self):
        #self.client.login(username='lee', password='p@ssword')
        response = self.client.get(reverse_lazy('dyno:dashboard'))
        self.assertEqual(response.status_code, 302)


class Test_CommandCenter_View(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.client = Client()
        self.user = User.objects.create_user('wade5', 'wade@wade.com', 'p@ssword')
        well = Well_Profile.objects.create(well_name='test well 1')
        card = Card_Info.objects.create(associated_well_profile=well, title='test card', img_file='test image', prediction='good')

    def test_home_view_login(self):
        self.client.login(username='wade5', password='p@ssword')
        response = self.client.get(reverse_lazy('dyno:command_center'))
        self.assertEqual(response.status_code, 200)

class Test_CommandCenter_View_Fails(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.client = Client()
        #self.user = User.objects.create_user('lee', 'wade@wade.com', 'p@ssword')

    def test_home_view_login(self):
        #self.client.login(username='lee', password='p@ssword')
        response = self.client.get(reverse_lazy('dyno:command_center'))
        self.assertEqual(response.status_code, 302)

#class Test_Checkpoint_View(unittest.TestCase):

#    @classmethod
#    def setUpClass(self):
#        self.client = Client()
#        self.user = User.objects.create_user('wade6', 'wade@wade.com', 'p@ssword')

#    def test_home_view_login(self):
#        self.client.login(username='wade6', password='p@ssword')
#        response = self.client.get(reverse_lazy('dyno:checkpoint'))
#        self.assertEqual(response.status_code, 200)

class Test_Checkpoint_View_Fails(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.client = Client()
        #self.user = User.objects.create_user('lee', 'wade@wade.com', 'p@ssword')

    def test_home_view_login(self):
        #self.client.login(username='lee', password='p@ssword')
        response = self.client.get(reverse_lazy('dyno:checkpoint'))
        self.assertEqual(response.status_code, 302)

#class TestMustLogin(unittest.TestCase):

#    @classmethod
#    def setUpClass(self):
        #self.
