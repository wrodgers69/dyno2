
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

import sys, os, django

### unhash below if running in ipython separate from django.
#sys.path.append('/Users/leerodgers/projects/djangoproject')
#os.chdir('/Users/leerodgers/projects/djangoproject')
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoproject.settings")
#django.setup()

from dyno.models import Card_Info

#ignore for now:
def predict_generator():
    #for large size images - create prediction data_generators

    #set directory. ###Note in django app will need to update using os.path.join(BASE_DIR, ____)
    directory = '/Users/leerodgers/projects/djangoproject/images'

    prediction_datagen = ImageDataGenerator(
            rescale=1./255)

    preds = prediction_datagen.flow_from_directory(
        directory,
        target_size=(256, 256),
        color_mode='grayscale',
        classes=None,
        class_mode='binary',
        batch_size=16,
        shuffle=False,)

    for data_batch, _ in preds:   # throws away the labels that would normally be generated.
        pred_images = data_batch
        break

    print(str(preds.class_indices) + '# creating category for predict only.')
    type(preds)
    pred_images.shape


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
