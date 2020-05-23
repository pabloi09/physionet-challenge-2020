from run_12ECG_classifier import load_12ECG_model, run_12ECG_classifier
from driver import load_challenge_data
import numpy as np
import tensorflow as tf

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ClassifierInterface(metaclass=Singleton):
    
    def __init__(self):
        self.classes = np.array([ "AF" ,"I-AVB" ,"LBBB" ,"Normal" ,"PAC" ,"PVC" ,"RBBB" ,"STD" ,"STE" ])
        self.model = load_12ECG_model()

    def predict(self,file_path):
        data, header_data = load_challenge_data(file_path)
        current_label,current_score,real_out,leads,fs = run_12ECG_classifier(data, header_data, self.classes, self.model)
        
        return current_label, current_score, real_out, leads, self.classes,fs

