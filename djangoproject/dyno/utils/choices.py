from dyno.models import Well_Profile

def well_choice_gen():
    well = Well_Profile.objects.all()
    well_choices = [('','--Please assign to Well--')]
    for item in well:
        well_choices.append((item.well_name, item.well_name))

    return well_choices
