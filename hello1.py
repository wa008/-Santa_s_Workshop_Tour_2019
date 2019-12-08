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

def main():
    print 'main', '-' * 50
    pre_time = time.time()
    data = read_csv('family_data.csv')
    family_size_dict = data[['n_people']].to_dict()['n_people']
    cols = ['choice_' + str(i) for i in range(10)]
    choice_dict = data[cols].to_dict()
    N_DAYS = 100
    days = list(range(N_DAYS,0,-1))
    max_occu = 300
    min_occu = 125

    submission = read_csv('sample_submission.csv')
    best = [choice_dict['choice_0'][x] for x in range(len(data))]
    best_score = cost_function(best, choice_dict, family_size_dict)

    daily_occupancy = {k : 0 for k in days}
    for fam_id, day in enumerate(best):
        daily_occupancy[day] += family_size_dict[fam_id]
    for fam_id, now_day in enumerate(best):
        random.seed(time.time())
        now_occu = daily_occupancy[now_day]
        now_size = family_size_dict[fam_id]
        if now_occu > max_occu:
            answer_day = -1
            for day in days:
                if daily_occupancy[day] < min_occu:
                    answer_day = day
                    break
            if answer_day == -1:
                for _ in range(100):
                    temp_day = random.randint(1, 100)
                    if daily_occupancy[temp_day] + now_size <= max_occu:
                        answer_day = temp_day
                        break
            if answer_day == -1:
                print 'fam_id = ', fam_id
            else:
                best[fam_id] = answer_day
                daily_occupancy[now_day] -= now_size
                daily_occupancy[answer_day] += now_size
    for day in days:
        assert daily_occupancy[day] >= min_occu and daily_occupancy[day] <= max_occu

    best_score = cost_function(best, choice_dict, family_size_dict)
    print 'deal with max min daily_occupancy time, score = ', time.time() - pre_time, best_score
    pre_time = time.time()
    submission['assigned_day'] = best
    write_submission('submission_20191207_deal_with_max_min', submission)

    for _ in range(100):
        pre_all_score = best_score
        for fam_id, now_day in enumerate(best):
            random.seed(time.time())
            now_occu = daily_occupancy[now_day]
            now_size = family_size_dict[fam_id]
            if daily_occupancy[now_day] - now_size < min_occu:
                continue
            for pick in range(10):
                new_day = choice_dict['choice_' + str(pick)][fam_id]
                if new_day == now_day or daily_occupancy[now_day] - now_size < min_occu or daily_occupancy[new_day] + now_size > max_occu:
                    continue
                temp = [x for x in best]
                temp[fam_id] = new_day # add in the new pick
                temp_score = cost_function(temp, choice_dict, family_size_dict) 
                if temp_score < best_score:
                    best[fam_id] = new_day
                    best_score = temp_score
                    daily_occupancy[now_day] -= now_size
                    daily_occupancy[new_day] += now_size
            for __ in range(10):
                new_day = random.randint(1, 100)
                if new_day == now_day or daily_occupancy[now_day] - now_size < min_occu or daily_occupancy[new_day] + now_size > max_occu:
                    continue
                temp = [x for x in best]
                temp[fam_id] = new_day
                temp_score = cost_function(temp, choice_dict, family_size_dict)
                if temp_score < best_score:
                    best[fam_id] = new_day
                    best_score = temp_score
                    daily_occupancy[now_day] -= now_size
                    daily_occupancy[new_day] += now_size
            if fam_id % 500 == 0:
                print 'best_score = ', best_score, time.time() - pre_time
                pre_time = time.time()
        if best_score < pre_all_score:
            submission['assigned_day'] = best
            write_submission('submission_20191207_' + str(_), submission)
            print 'write_submission, score = ', _, best_score
        if best_score >= pre_all_score:
            not_better += 1
        else:
            not_better = 0
        if not_better > 3:
            break
    print 'not_better = ', not_better

main()