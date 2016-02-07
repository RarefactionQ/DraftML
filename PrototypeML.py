import argparse
import numpy as np
import matplotlib.pyplot as plt

from sklearn import datasets, svm, linear_model, tree
from IPython.display import Image
from sklearn.externals.six import StringIO

from feature_extractors.hero_feature_extractor import HeroFeatureExtractor

INPUT_FILE_DEFAULT = 'draft.txt'
OUTPUT_FEATURE_FILE_DEFAULT = 'Proto.csv'

def buildExamples(input_file, output_file):
	f = open(input_file, 'r+')
	w = open(output_file, 'w')
	draft_list = f.read().split('\n')
	# for elem in draft_list:
		# print elem
	# print len(draft_list)
	for draft in draft_list:
		attributes = draft.split(',')
		# print len(attributes)
		# if len(attributes) != 102:
		# 	for attr in attributes:
		# 		print attr

		# for attr in attributes:
			# print attr
		# break

		w.write(attributes[0]+'.,') #winner
		if attributes[5] == 'Radiant':
			w.write('1.,')
		elif attributes[5] == 'Dire':
			w.write('0.,')
		else:
			w.write('-1.,') # this shouldn't happen

		hero_pick_indexes = [3, 8, 13, 18, 23, 28, 33, 38, 43, 48, 53, 58, 63, 68, 73, 78, 83, 88, 93, 98]
		features = list()
		for hero_pick_index in hero_pick_indexes:
			features.extend(HeroFeatureExtractor.extract(attributes[hero_pick_index]))

		w.write(",".join(str(x) for x in features))
		w.write('\n')

	w.close()


def getExamples(from_file):
	dataset = np.genfromtxt(from_file, delimiter = ',')
	# print (dataset.shape)
	X = dataset[:,1:-1] #Rest of attributes
	y = dataset[:,0] #Target

	# print X.shape[1]

	n_sample = len(X) # from plot_iris_exercise.py

	np.random.seed(0)
	order = np.random.permutation(n_sample)
	X = X[order]
	y = y[order].astype(np.float)

	X_train = X[:.9 * n_sample]
	y_train = y[:.9 * n_sample]
	X_test = X[.9 * n_sample:]
	y_test = y[.9 * n_sample:]

	alphas = np.logspace(-4, -1, 6)
	# alphas = np.logspace(-4, -1, 6)

	return ((X_train, y_train), (X_test, y_test))

def doDecisionTree(train, test):	
	# regr = linear_model.Lasso()
	# scores = [regr.set_params(alpha=alpha).fit(X_train, y_train).score(X_test, y_test) for alpha in alphas]
	# best_alpha = alphas[scores.index(max(scores))]
	# regr.alpha = best_alpha
	# print regr.fit(X_train, y_train)
	# print(regr.coef_)

	clf = tree.DecisionTreeClassifier()
	clf = clf.fit(train[0], train[1])

	# for x in X_train:
	# 	print x
	# for y in y_train:
	# 	print y

	with open("Proto.dot", 'w') as f:
		f = tree.export_graphviz(clf, feature_names=["first","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21"],  
							class_names=["Dire","Radiant"],  
							filled=True, rounded=True,  
							special_characters=True, out_file=f)
	

def main():
	parser = argparse.ArgumentParser(description='Predict some Dota winners.')
	parser.add_argument('-i', '--input_file', type=str, default=INPUT_FILE_DEFAULT,
					help='File to read example matches from')
	parser.add_argument('-o', '--output_file', type=str, default=OUTPUT_FEATURE_FILE_DEFAULT,
					help='File to output extracted features to')
	args = parser.parse_args()

	buildExamples(input_file=args.input_file, output_file=args.output_file)
	train, test = getExamples(args.output_file)
	doDecisionTree(train, test)


if __name__ == "__main__":
	main()
