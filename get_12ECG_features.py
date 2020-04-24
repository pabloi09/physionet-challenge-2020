#!/usr/bin/env python

import numpy as np
from scipy.signal import butter, lfilter, resample
from scipy import stats


def get_slices(signal):
    signals = []
    while len(signal) > 2999:
        signals.append(resample(signal[:3000],256))
        signal = signal[3001:]

    return signals

def bandpass_filter(data, lowcut, highcut, signal_freq, filter_order):
    
        nyquist_freq = 0.5 * signal_freq
        low = lowcut / nyquist_freq
        high = highcut / nyquist_freq
        b, a = butter(filter_order, [low, high], btype="band")
        y = lfilter(b, a, data)
        y[:5] = y[5]
        
        return y

def normalize(signal):
    signal -= np.mean(signal)
    minimum = np.amin(signal)
    maximum = np.amax(signal)
    
    return (signal - minimum) / ( maximum - minimum)

def get_features(classes,data, header_data):
    
    #data_dict {fs, n_samples,"age","sex","output":[0 1 0 1 0],"prescript","hist","sympt", 
    #leads:[{"gain","name",samples:[]}]}
    data_dict = {}
    _,n_leads,fs,n_samples,_,_ = header_data[0].split()
    n_leads,fs,n_samples = map(int,[n_leads,fs,n_samples])
    
    data_dict["n_leads"] = n_leads
    data_dict["fs"] = fs
    data_dict["n_samples"] = n_samples
    data_dict["leads"] = []
    
    for i in range(n_leads):
        tmp = header_data[i + 1].split()
        lead_name = tmp[-1]
        gain_mv = int(tmp[2].replace("/mV",""))
        lead = {}
        lead["name"] = lead_name
        lead["gain_mv"] = gain_mv
        lead["samples"] = data[i]
        data_dict["leads"].append(lead)
    
    for line in header_data:
        if "#Age" in line:
            age = line.split(": ")[1]
            data_dict["age"] = int(age if not "NaN" in age else 57)
        elif "#Sex" in line:
            data_dict["sex"] = line.split(": ")[1].replace("\n","")
        elif "#Dx" in line:
            data_dict["output"] = np.zeros((1,9))
            for c in line.split(": ")[1].replace("\n","").split(","):
                data_dict["output"] += (classes == c)
        elif "#Rx" in line:
            data_dict["Rx"] = line.split(": ")[1].replace("\n","")
        elif "#Hx" in line:
            data_dict["Hx"] = line.split(": ")[1].replace("\n","")
        elif "#Sx" in line:
            data_dict["Sx"] = line.split(": ")[1].replace("\n","")
    return data_dict

def get_x(data_dict):
    filter_lowcut = 0.001
    filter_highcut = 15.0
    filter_order = 1
    signals = []
    for lead in data_dict["leads"]:
      filtered = bandpass_filter(lead["samples"], lowcut=filter_lowcut, highcut=filter_highcut, signal_freq = data_dict["fs"], filter_order = filter_order)
      for s in get_slices(filtered):
        try:
          normalized = normalize(s)
          signals.append(normalized)
        except:
          continue
    x = np.asarray(signals)
    return x