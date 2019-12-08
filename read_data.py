#coding=utf-8
import numpy as np
import pandas as pd
import random
import time
import warnings
from sklearn.externals import joblib
warnings.filterwarnings("ignore")
data_path = 'D:\kaggle\data\Santa_s_Workshop_Tour_2019\c'[ : -1]
# data_path = '/mnt/d/kaggle/data/Santa_s_Workshop_Tour_2019/'

def read_csv(data_name = 'family_data.csv', read_row = -1):
    print data_name, read_row
    pre_time = time.time()
    if read_row == -1:
        df = pd.read_csv(data_path + data_name)
    else:
        df = pd.read_csv(data_path + data_name, nrows = read_row)
    print 'shape, time = ', df.shape, time.time() - pre_time
    return df

def write_submission(data_name, df):
    df.to_csv(data_path + data_name, index = False)

def read_list(data_name):
    f = open(data_path + data_name, 'r')
    datas = f.read()
    return datas.split('\n')

def write_list(data_name, datas):
    f = open(data_path + data_name, 'w')
    f.write('\n'.join(datas))

def read_dict(data_name):
    f = open(data_path + data_name, 'r')
    return json.loads(f.read())

def write_dict(data_name, datas):
    f = open(data_path + data_name, 'w')
    f.write(json.dumps(datas))

def model_save(model, name = 'lr'):
    joblib.dump(model, data_path + name + '_model.joblib')

def mode_load(name = 'lr'):
    return joblib.load(data_path + name + '_model.joblib')