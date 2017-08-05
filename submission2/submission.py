## import modules here 
import pickle
from sklearn.ensemble import RandomForestClassifier

# 元音字典
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

################# training #################

def train(data, classifier_file):# do not change the heading of the function
	# 提取数据的音节部分
    syllables = [x[x.find(':')+1:].split() for x in data]

    # 提取数据的元音部分
    vowels = [[v for v in l if v not in Consonants] for l in syllables]

    # 去除元音中的重音标记（数字）
    raw_vowels = strip_stress_mark(vowels)

    # 把元音转化为元音编号（0代表空，1~15）
    vowels_in_code = [[Vowels.index(x)+1 for x in l] for l in raw_vowels]
    vowels_in_code = [resize(l, 4) for l in vowels_in_code]

    # 提取数据的辅音部分
    consonants = [[v for v in l if v in Consonants] for l in syllables]

	# 把辅音转化为辅音编号
    consonants_in_code = [[Consonants.index(x)+1 for x in l] for l in consonants]
    consonants_in_code = [resize(l, 10) for l in consonants_in_code]

	# 找数据的重音位置（0~4代表位置1~5）
    stress = find_stress(vowels)
    
    X = []
    for i in range(len(vowels_in_code)):
        x = [0] * 14
        x[0:10] = consonants_in_code[i]
        x[10:14] = vowels_in_code[i]
        X.append(x)
    
    y = stress

    clf = RandomForestClassifier(n_estimators=3000, criterion='entropy', max_features='log2', max_depth=130)
    clf.fit(X, y)
    output = open(classifier_file, 'wb')
    pickle.dump(clf, output)

    pass # **replace** this line with your code    

################# testing #################

def test(data, classifier_file):# do not change the heading of the function
    # 提取数据的音节部分
    syllables = [x[x.find(':')+1:].split() for x in data]
	
    # 提取数据的元音部分
    vowels = [[v for v in l if v not in Consonants] for l in syllables]

    # 把元音转化为元音编号（0代表空，1~15）
    vowels_in_code = [[Vowels.index(x)+1 for x in l] for l in vowels]
    vowels_in_code = [resize(l, 4) for l in vowels_in_code]

    # 提取数据的辅音部分
    consonants = [[v for v in l if v in Consonants] for l in syllables]
	
	# 把辅音转化为辅音编号
    consonants_in_code = [[Consonants.index(x)+1 for x in l] for l in consonants]
    consonants_in_code = [resize(l, 10) for l in consonants_in_code]

    X = []
    for i in range(len(vowels_in_code)):
        x = [0] * 14
        x[0:10] = consonants_in_code[i]
        x[10:14] = vowels_in_code[i]
        X.append(x)
	    
    clf = pickle.load(open(classifier_file, 'rb'))
    y_predict = clf.predict(X)
    return [x+1 for x in y_predict.tolist()]