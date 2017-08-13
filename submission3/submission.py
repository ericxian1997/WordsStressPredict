import pickle

import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

import helper

Vowels = ['AA', 'AE', 'AH', 'AO', 'AW', 'AY', 'EH', 'ER', 
			'EY', 'IH', 'IY', 'OW', 'OY', 'UH', 'UW']
# 辅音字典
Consonants = ['P', 'B', 'CH', 'D', 'DH', 'F', 'G', 'HH', 'JH', 'K', 'L', 'M', 'N',
				 'NG', 'R', 'S', 'SH', 'T', 'TH', 'V', 'W', 'Y', 'Z', 'ZH']

def find_stress(vowels):
	    stress = []
	    for l in vowels:
	        for v in l: 
	            if '1' in v:
	                stress.append(l.index(v))
	    return stress

def strip_stress_mark(vowels):
	    raw_vowels = []
	    for l in vowels:
	        raw_l = []
	        for v in l:
	            raw_l.append(v.replace('0', '').replace('1', '').replace('2', ''))
	        raw_vowels.append(raw_l)
	    return raw_vowels

def resize(l, n):
	    while len(l) < n:
	        l.append(0)
	    while len(l) > n:
	        l.pop()
	    return l

def strip_stress(phonetic):
    return [i[:2] for i in phonetic.split()]

def extract_consonants(phonetic):
    return [i for i in phonetic.split() if i in Consonants]

def extract_features(line):
    print(line, ':', end='\t')
    word, phonetic = tuple(line.split(sep=":"))
    result = [number_of_syllable(phonetic), end_with_vowel(phonetic)]

    for i in range(min(4, len(word))):
    # result.extend(ord(j) for j in word[:min(4, len(word))])
        result.append(sum([ord(j) for j in word[:i+1]]))

    while len(result) < 6:
        result.append(0)
    for i in range(min(4, len(word))):
        # result.extend(ord(j) for j in word[-min(4, len(word)):])
        result.append(sum([ord(j) for j in word[-(i+1):]]))

    while len(result) < 10:
        result.append(result[0])

    phonetic = strip_stress(phonetic)   

    for i in phonetic:
        if i in Consonants:
            result.append(Consonants.index(i)+1)

    while len(result) < 20:
        result.append(0)

    for i in phonetic:
        if i in Vowels:
            result.append(Vowels.index(i)+1)

    while len(result) < 24:
        result.append(0)
    for i in result:
        print('{:3}'.format(i), end=' ')
    else:
        print()
    return np.array(result)

def extract_vowels(phonetic):
    vowel_alphabet = ['A', 'E', 'I', 'O', 'U']
    return [i for i in phonetic.split()
                for j in vowel_alphabet if i.startswith(j)]
    
def end_with_vowel(phonetic):
    syllable = phonetic.split()
    return 1 if syllable[-1] in extract_vowels(phonetic) else 0
    
def number_of_syllable(phonetic):
    return len(extract_vowels(phonetic))
    
def position_of_stress(phonetic):
    vowels = extract_vowels(phonetic)
    for vowel in vowels:
        if vowel.endswith('1'):
            return vowels.index(vowel)+1
    raise Exception("no stress: "+phonetic)
    
def generate_feature_matrix(data):
    matrix = np.ndarray((0, 24))
    for line in data:
        matrix = np.vstack((matrix, extract_features(line)))
    return matrix

def generate_target_matrix(data):
    matrix = np.ndarray((0, 1))
    for line in data:
        word, phonetic = tuple(line.split(sep=":"))
        matrix = np.vstack((matrix, position_of_stress(phonetic)))
    return matrix

def generate_X_Y(data):
    return (generate_feature_matrix(data), generate_target_matrix(data).ravel())

################# training #################

def train(data, classifier_file):# do not change the heading of the function
    with open(classifier_file, 'wb') as fd:
        X, Y = generate_X_Y(data)   
        RF = RandomForestClassifier(n_estimators=100)
        RF.fit(X, Y)
        pickle.dump(RF, file=fd)

################# testing #################

def test(data, classifier_file):# do not change the heading of the function
    with open(classifier_file, 'rb') as fd:
        classifier = pickle.load(fd)
        X =  generate_feature_matrix(data)  
        prediction = classifier.predict(X)
        return list(map(int, prediction))
