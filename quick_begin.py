#encoding:utf-8
import json
import time
import random
import numpy as np
import pandas as pd
from collections import Counter
import warnings
warnings.filterwarnings('ignore')
import sys
from sklearn.externals import joblib

from read_data import read_csv, read_list, write_list, read_dict, write_dict, model_save, mode_load, data_path, write_submission
from cost_function import cost_function

def beginner():
    data = read_csv('family_data.csv')
    family_size_dict = data[['n_people']].to_dict()['n_people']
    cols = ['choice_' + str(i) for i in range(10)]
    choice_dict = data[cols].to_dict()
    N_DAYS = 100
    days = list(range(N_DAYS,0,-1))

    submission = read_csv('sample_submission.csv')
    best = submission['assigned_day'].tolist()
    start_score = cost_function(best, choice_dict, family_size_dict)

    new = [x for x in best]
    pre_time = time.time()
    # loop over each family
    for fam_id, _ in enumerate(best):
        # loop over each family choice
        for pick in range(10):
            day = choice_dict['choice_' + str(pick)][fam_id]
            temp = [x for x in new]
            temp[fam_id] = day # add in the new pick
            if cost_function(temp, choice_dict, family_size_dict) < start_score:
                new = [x for x in temp]
                start_score = cost_function(new, choice_dict, family_size_dict)
        if fam_id % 500 == 0:
            print 'time = ', time.time() - pre_time
            pre_time = time.time()

    submission['assigned_day'] = new
    score = cost_function(new, choice_dict, family_size_dict)
    submission.to_csv(data_path + 'submission_20191207_01.csv', index = False)
    print 'Score = ', score

beginner()