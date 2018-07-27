
import keras
from keras.models import *
from keras import layers
from keras.optimizers import *
from keras.preprocessing import *
from keras.preprocessing.image import *
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from PIL import Image
import numpy as np
import pandas as pd
import sqlite3
import time
import tensorflow as tf

import glob


import sys, os, django

### unhash below if running in ipython separate from django.
#sys.path.append('/Users/leerodgers/projects/djangoproject')
#os.chdir('/Users/leerodgers/projects/djangoproject')
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoproject.settings")
#django.setup()

from dyno.models import Card_Info, Well_Profile


### load model ###
def load_keras_model():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath('dyno/utils/dyno_model_CNN_1')))
    PATH = os.path.abspath('dyno/utils/dyno_model_CNN_1')
    ROOT = os.path.join(BASE_DIR, PATH)

    global model
    model = load_model(str(ROOT))
    global graph
    graph = tf.get_default_graph()
    return model


def analyze_directory(input_directory, well_name=None):

    DIR = input_directory + '/*.*'
    MEDIA_ROOT = os.path.abspath('media/')
    SAVE_DIR = os.path.join(MEDIA_ROOT, well_name)    # fix this error

    files = glob.glob(DIR)
    num_files = len(files)

    if num_files == 0:
        print('No files in directory, or incorrect directory name format. Please confirm directory naming convention: "~/predict/well_name/images.jpg"')
        return

    print('Found %s files tied to %s. \nSaving files at %s' %(num_files, well_name, SAVE_DIR))

    return num_files, well_name, SAVE_DIR

def predict_img(predict_style = None, verbose = None, num_predicts = None, large_dataset = False):
    '''Gathers images from file, runs predicitons, and saves predictions to SQLite3 db for later rendering.
    Inputs:
        - predict_style: Predict on images without predictions, or overwrite all predictios. D
                Default: None, predict on images with no predictions
                'replace': Overwrites all predicitons with new predictions
        - num_predicts: How many predictions to make from oldest to newest item.
        - verbose: outputs printed or not, including data frame (defaults to None)
        - large_dataset: Boolean. If large dataset, will use predict_generator
    Returns: updates db prediction values
    '''


    if predict_style == 'replace':
        item_set = Card_Info.objects.all()
        print('Predicting on all images in database and overwriting old predicitons')

    else:
        item_set = Card_Info.objects.filter(prediction='')
        print('Predicting on all images in database without predictions')

    if item_set.count() == 0:
        print("All images in database have predictions. Set predict_style = 'replace' to overwrite existing predictions with new predictions")

    start_time = time.time()
    step = 0


    for item in item_set:

        if num_predicts:
            step +=1

        print('Analyzing picture %s\n' %(str(item.img_file)))

        #get correct file path

        img_file = str(item.img_file)
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(img_file)))
        MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
        img_path = os.path.join(MEDIA_ROOT, img_file)

        #process image to make uniform prediction (grayscale, 256x256, proper shape, etc)
        img = Image.open(str(img_path))
        img = img.resize((256,256))
        img = img.convert('L')
        img_predict = img_to_array(img)
        img_predict = img_predict.reshape((1,256,256,1))

        # make predictions
        with graph.as_default():
            pred = model.predict_classes(img_predict)
        if pred == 1:
            item.prediction = 'Good'
            item.save()
        else:
            item.prediction = 'Bad'
            item.save()


        if verbose == 1:
            print('image file: ' + img_file)
            print('image path: ' + img_path)
            display(img)
            print('image size: ' + str(img.size))
            print('img_predict reshape: ' + str(img_predict.shape))
            print('img_predict shape: ' + str(img_predict.shape))
            print('prediction = ' + str(item.prediction))
            print(' ')


        if num_predicts:
            if step > (num_predicts-1):
                break

    end_time = time.time()
    print('Time elapsed = ' + str(end_time- start_time))


def predict_from_directory(input_directory, well_name = None, num_saves = None, verbose = None):
    '''Predicts card images from directory

    inputs:
        - input_directory: location of directory to analyze. Must specify final structure as ~/predict/test_wellname/images.jpg
        - well_name: name of the well that card images are related to. if "None" will put images in generic folder
        - num_saves: how many of the images to save from the directory.
        - verbose: if set to one, will print file input location and final save location.

    returns:
        - predicts on directory and loads images to model
        '''

    DIR = input_directory + '/*.*'
    print(DIR)
    MEDIA_ROOT = os.path.abspath('media/')
    SAVE_DIR = os.path.join(MEDIA_ROOT, well_name)    # fix this error
    print(SAVE_DIR)

    files = glob.glob(DIR)
    num_files = len(files)

    if num_files == 0:
        print('No files in directory, or incorrect directory name format. Please confirm directory naming convention: "~/predict/well_name/images.jpg"')
        return

    try:
        os.makedirs(SAVE_DIR)
    except:
        pass

    step = 0
    preds = {}

    print('...Reading files...')
    for file in files:

        if num_saves:
            step+=1

        _, img_file = file.split('predict/')
        SAVE_PATH = os.path.join(MEDIA_ROOT, img_file)

        #process image to make uniform prediction (grayscale, 256x256, proper shape, etc)
        img = Image.open(file)
        img = img.convert('L')
        img.save(SAVE_PATH)
        img = img.resize((256,256))
        img_predict = img_to_array(img)
        img_predict = img_predict.reshape((1,256,256,1))
        img.close()

        # make predictions
        with graph.as_default():
            pred = model.predict_classes(img_predict)
        if pred == 1:
            preds['%s' % img_file] = 'Good'
        else:
            preds['%s' % img_file] = 'Bad'

        if num_saves:
            if step > (num_saves-1):
                break

    print('...generating predictions...')
    for img_file, prediction in preds.items():
        well_profile = Well_Profile.objects.first()
        x = Card_Info(associated_well_profile = well_profile, title = img_file, img_file = img_file, prediction = prediction)
        x.save()

    total_preds = len(preds)
    print('...Complete. Predicted %s images...')
