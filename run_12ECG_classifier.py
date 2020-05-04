#!/usr/bin/env python

import numpy as np
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Reshape, BatchNormalization
from tensorflow.keras.layers import Activation, Input, Dropout, Flatten, LSTM
from tensorflow.keras.layers import Bidirectional, Conv1D
from tensorflow.keras.layers import MaxPooling1D, Embedding, Concatenate
from tensorflow.keras.optimizers import Adam, RMSprop
import tensorflow as tf
from get_12ECG_features import get_features, get_x 
import os
import math

dropout = 0.25
batch_norm = 0.8

def run_12ECG_classifier(data, header_data, classes, model):
    data_dict = get_features(classes, data, header_data)
    x, tags = get_x(data_dict)
    y = model.predict([x,tags])
    for i in range(y.shape[0]):
        agmax = y[i][np.argmax(y[i])]
        y[i] = ((y[i] == agmax) + np.zeros((9,))) 
    current_score = np.sum(y, axis= 0) / y.shape[0]
    current_label = (current_score > 0.4) + np.zeros((9,))
    if(np.sum(current_label) == 0):
        agmax = current_score[np.argmax(current_score)]
        current_label = ((current_score == agmax) + np.zeros((9,))) 
    if math.isnan(current_label[0]):
         current_label = np.zeros((9,))
    return current_label,current_score

def load_12ECG_model():
    # load the model from disk 
    model = prep_classifier()
    optimizer = Adam(learning_rate = 5e-2)
    model.compile(optimizer='adam',
                loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),
                metrics=['accuracy'])
    model.load_weights("./modelo")

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


    model.summary()
    qdata.summary()
    join.summary()
    return classifier