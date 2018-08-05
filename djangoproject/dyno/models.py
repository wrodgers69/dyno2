from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

# Create your models here.

class Well_Profile(models.Model):
    #well_id = models.AutoField(primary_key=True, blank = True, null = True)
    well_name = models.CharField(max_length=50, blank = True, null = True)
    #well_API
    pumping_unit =models.CharField(max_length=50, blank = True, null = True)
    engineer = models.ManyToManyField(User)

    team_choices = (
    ('1', 'Wolfbone RMT'),
    ('2', 'Lockridge RMT'),
    ('3', 'Cedar Canyon RMT'),
    ('4', 'Mentone RMT'),
    ('5', 'FDP'),
    ('6', 'Well Analysis and Design'),
    )
    team = models.CharField(max_length=100, choices=team_choices, default='Wolfbone RMT')

    asset_choices = (
    ('WOLFBONE', 'Wolfbone'),
    ('REDBULLSOUTH', 'RedBull South'),
    ('LOCKRIDGE', 'Lockridge'),
    ('MENTONE', 'Mentone'),
    ('HELLSCANYON', 'Hells Canyon'),
    ('REDBULLNORTH', 'RedBull North'),
    )
    asset = models.CharField(max_length=100, choices=asset_choices, default='Wolfbone')

    region_choices = (
    ('TXDELAWARE', 'Tx Delaware Basin'),
    ('MIDLAND', 'Midland Basin'),
    ('NMDEL', 'NM Delaware Basin')
    )
    region = models.CharField(max_length=100, choices=region_choices, default='Tx Delaware Basin')

    welltype_choices = (
    ('WCA10k', 'WCA_10k'),
    ('WCA7.5k', 'WCA_7500'),
    ('1BS10k', '1BS_10k'),
    ('WCB10k', 'WCB_10k'),
    ('WCC10k', 'WCC_10k'),
    ('2BS10k', '2BS_10k'),
    ('3BS10k', '3BS_10k'),
    ('HOBAN10k', 'Hoban_10k'),
    ('HOBAN5k', 'Hoban_5k'),
    )
    subwelltype = models.CharField(max_length=50, choices=welltype_choices, default='WCA_10k')

    designed_total_prod = models.IntegerField(default=0, null = True)
    #Eventually "last_well_test" will be a query into a company's DB and auto-populate
    last_well_test = models.IntegerField(default=0, null = True)
    date_created = models.DateTimeField(editable=False)
    date_updated = models.DateTimeField(null = True)
    def save(self, *args, **kwargs):
        #''' On save, update timestamps '''
        if not self.well_name:
            self.date_updated = timezone.now()
        else:
            self.date_created = timezone.now()
        return super(Well_Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.well_name

    #"recently" is being defined as within 1 day of "now"
    def was_updated_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date_updated <= now

    def was_created_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date_created <= now

    def production_check(self):
        min = 0
        return min <= self.last_well_test <= self.designed_total_prod

    pass

class Card_Info(models.Model):
    #card_id = models.AutoField(primary_key=True, blank = True, null = True)
    associated_well_profile = models.ForeignKey(Well_Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    img_file = models.ImageField(upload_to='images')
    card_description = models.CharField(max_length=200, blank = True)
    prediction = models.CharField(max_length=50, blank = True)#    date_upload = models.DateTimeField(editable=False)
    date_updated = models.DateTimeField(auto_now=True, null = True)
    date_upload = models.DateTimeField(auto_now_add=True, editable=False)
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''

        if not self.img_file:
            self.date_updated = timezone.now()
        else:
            self.date_upload = timezone.now()


        return super(Card_Info, self).save(*args, **kwargs)

    actual_total_prod = models.IntegerField(default=0, null = True)
    #placeholder for string to return... function of other inputs (like title + date)
    #    def __str__(self):
    #       return self.well_name
    #       return str(self.title)
    def __str__(self):
        return self.title

    def was_updated_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date_updated <= now

    def was_created_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date_upload <= now

class Dysfunction_Profile(models.Model):
    #dys_id = models.AutoField(primary_key=True, blank = True, null = True)
    dys_name = models.CharField(max_length=50, blank = True, null = True)
    #dys_name = models.ForeignKey(Card_Info, on_delete=models.CASCADE, to_field='prediction', unique=True)
    dys_description = models.CharField(max_length=50, blank = True, null = True)
    dys_action = models.CharField(max_length=50, blank = True, null = True)
    def __str__(self):
        return self.dys_name
