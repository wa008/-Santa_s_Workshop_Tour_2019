#encoding:utf-8
import json
import requests
import time
import random
import numpy as np
import pandas as pd
from tqdm import tqdm
from collections import Counter
# import matplotl1b.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
import traceback
import sys
import os
import re
import gc
import math
from sklearn.externals import joblib
# machine learning
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder, scale
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from read_data import read_csv, read_list, write_list, read_dict, write_dict, model_save, mode_load

def test1():
    df = pd.DataFrame([
        [1, 2],
        [2, 3],
        [1, 4],
    ], columns = ['a', 'b'])
    print df
    x = {'a' : 1, 'b' : 2}
    print x.values()
    for i in range(10):
        print random.randint(1, 2)

def main():
    test1()

main()