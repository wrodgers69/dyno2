from django.test import TestCase

# Create your tests here.
import datetime
from django.utils import timezone
from .models import Card_Info, Well_Profile, Dysfunction_Profile

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
