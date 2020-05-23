#!/usr/bin/env python

import numpy as np
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Reshape, BatchNormalization
from tensorflow.keras.layers import Activation, Input, Dropout, Flatten, LSTM
from tensorflow.keras.layers import Bidirectional, Conv1D
from tensorflow.keras.layers import MaxPooling1D, Embedding, Concatenate
from tensorflow.keras.optimizers import Adam, RMSprop
import tensorflow as tf
from get_12ECG_features import get_features, get_x , get_for_web
import os
import math
import requests
import json
dropout = 0.25
batch_norm = 0.8

def run_12ECG_classifier(data, header_data, classes, model):
    data_dict = get_features(classes, data, header_data)
    x, tags = get_x(data_dict)
    leads = get_for_web(data_dict)
    current_score = 1/2 * evaluate_with_t(x,tags,model["transformations"]) + 1/4 * evaluate_with_gan(x,tags,model["gan"]) + 1/4 * evaluate_with_hybrid(x,tags,model["hybrid"])
    current_score = filters_total(current_score)
    current_label = (current_score > 0.5) + np.zeros((9,))
    if(np.sum(current_label) == 0):
        agmax = current_score[np.argmax(current_score)]
        current_label = ((current_score == agmax) + np.zeros((9,))) 
    if math.isnan(current_label[0]):
         current_label = np.zeros((9,))
    return current_label,current_score,data_dict["output"],leads, data_dict["fs"]

def evaluate_with_t(x,tags,model):
    y = model.predict([x,tags])
    for i in range(y.shape[0]):
        argsmax = np.argsort(-y[i])
        argmax = y[i][argsmax[0]]
        y[i] = ((y[i] == argmax) + np.zeros((9,)))
    current_score = np.sum(y, axis= 0) / y.shape[0]
    current_score = filters_t(current_score)
    return current_score

def evaluate_with_gan(x,tags,model):
    y = model.predict([x,tags])
    for i in range(y.shape[0]):
        argsmax = np.argsort(-y[i])
        argmax = y[i][argsmax[0]]
        y[i] = ((y[i] == argmax) + np.zeros((9,)))
    current_score = np.sum(y, axis= 0) / y.shape[0]
    current_score = filters_gan(current_score)
    return current_score

def evaluate_with_hybrid(x,tags,model):
    y = model.predict([x,tags])
    for i in range(y.shape[0]):
        argsmax = np.argsort(-y[i])
        argmax = y[i][argsmax[0]]
        y[i] = ((y[i] == argmax) + np.zeros((9,)))
    current_score = np.sum(y, axis= 0) / y.shape[0]
    current_score = filters_hybrid(current_score)
    return current_score

def filters_total(array):
    argsmax = np.argsort(-array)
    array = filter(argsmax,array,[6,8])
    return array

def filters_t(array):
    argsmax = np.argsort(-array)
    array = filter(argsmax,array,[6,1])
    array = filter(argsmax,array,[6,4])
    array = filter(argsmax,array,[6,7])
    array = filter(argsmax,array,[6,8,3,8])
    return array

def filters_gan(array):
    argsmax = np.argsort(-array)
    array = filter(argsmax,array,[6,4])
    array = filter(argsmax,array,[6,7])
    array = filter(argsmax,array,[6,8,3,8])
    return array

def filters_hybrid(array):
    argsmax = np.argsort(-array)
    array = filter(argsmax,array,[6,1])
    array = filter(argsmax,array,[6,4])
    array = filter(argsmax,array,[6,7,5,7,3,7])
    array = filter(argsmax,array,[6,8])
    return array

def filter(argsmax,array,changes=[]):
    for i in range(int(len(changes)/2)):
        if(argsmax[0] == changes[2*i] and argsmax[1] == changes[2*i+1]):
            tmp = array[argsmax[0]]
            array[argsmax[0]] = array[argsmax[1]]
            array[argsmax[1]] = tmp 
    return array



def load_12ECG_model():

    model = {}
    keys = ["transformations","gan","hybrid"]
    for key in keys:
        # load the model from disk 
        m = prep_classifier()
        optimizer = Adam(learning_rate = 5e-2)
        m.compile(optimizer='adam',
                    loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),
                    metrics=['accuracy'])
        m.load_weights("./classifier/{}/modelo".format(key))
        model[key] = m
    
    return model


def prep_classifier():
    
    model = Sequential()

    model.add(Reshape((16,16)))
    model.add(Bidirectional(LSTM(16,return_sequences=True)))
    model.add(Bidirectional(LSTM(16,return_sequences=True), merge_mode = "ave"))

    model.add(Reshape((256,1)))

    model.add(Conv1D(16, kernel_size = 3, padding = "same"))
    model.add(BatchNormalization(momentum=batch_norm))
    model.add(Activation("relu"))
    model.add(MaxPooling1D())
    model.add(Dropout(dropout))
    
    model.add(Conv1D(32, kernel_size = 3, padding = "same"))
    model.add(BatchNormalization(momentum=batch_norm))
    model.add(Activation("relu"))
    model.add(MaxPooling1D())
    model.add(Dropout(dropout))
    
    model.add(Conv1D(64, kernel_size = 3, padding = "same"))
    model.add(BatchNormalization(momentum=batch_norm))
    model.add(Activation("relu"))
    model.add(MaxPooling1D())
    model.add(Dropout(dropout))

    model.add(Conv1D(128, kernel_size = 3, padding = "same"))
    model.add(BatchNormalization(momentum=batch_norm))
    model.add(Activation("relu"))
    model.add(MaxPooling1D())
    model.add(Dropout(dropout))

    model.add(Flatten())
    qdata = Sequential()
    qdata.add(Embedding(164,64, input_length=3))
    qdata.add(Flatten())
    
    join = Sequential()
    join.add(Concatenate())
    join.add(Dense(512))
    join.add(BatchNormalization(momentum=batch_norm))
    join.add(Activation("relu"))
    join.add(Dense(64))
    join.add(BatchNormalization(momentum=batch_norm))
    join.add(Activation("relu"))

    join.add(Dense(9,activation="softmax"))


    signal = Input(shape = (256,1))
    qualdata = Input(shape = (3,))
    feat_signal = model(signal)
    feat_qdata = qdata(qualdata)

    out = join([feat_signal,feat_qdata])

    classifier = Model([signal,qualdata],out)

    return classifier