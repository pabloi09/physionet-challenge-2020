#!/usr/bin/env python

import numpy as np
import tensorflow as tf
from get_12ECG_features import get_features, get_x 
import os
import math

def run_12ECG_classifier(data, header_data, classes, model):
    data_dict = get_features(classes, data, header_data)
    x = get_x(data_dict)
    current_score = np.sum(model.predict(x), axis= 0) / x.shape[0]
    current_label = ((current_score  > 0.5) + (current_score == current_score[np.argmax(current_score)])) + np.zeros((9,))
    if math.isnan(current_label[0]):
        current_label = np.zeros((9,))
    if math.isnan(current_score[0]):
        current_score = np.zeros((9,))
    return current_label, current_score

def load_12ECG_model():
    # load the model from disk 
    checkpoint_path = "./training_1/cp.ckpt/"
    checkpoint_dir = os.path.dirname(checkpoint_path)
    loaded_model = tf.keras.models.load_model(checkpoint_dir)

    return loaded_model
