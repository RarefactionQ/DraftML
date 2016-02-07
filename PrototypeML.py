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

	for draft in draft_list:
		attributes = draft.split(',')

		w.write(attributes[0]+'.,') #winner
		if attributes[5] == 'Radiant':
			w.write('1.,')
		elif attributes[5] == 'Dire':
			w.write('0.,')
		else:
			w.write('-1.,') # this shouldn't happen

		radiant_ban_orders = [1, 3, 9, 11, 18]
		dire_ban_orders = [2, 4, 10, 12, 17] 
		radiant_pick_orders = [5, 8, 14, 16, 20]
		dire_pick_orders = [6, 7, 13, 15, 19]

		offset_spaces = 3
		attributes_per_hero = 5
		hero_pick_indexes = [offset_spaces + x * attributes_per_hero for x in range(0, 20)]

		radiant_bans = [attributes[hero_pick_indexes[x-1]] for x in radiant_ban_orders]
		radiant_picks = [attributes[hero_pick_indexes[x-1]] for x in radiant_pick_orders]
		dire_bans = [attributes[hero_pick_indexes[x-1]] for x in dire_ban_orders]
		dire_picks = [attributes[hero_pick_indexes[x-1]] for x in dire_pick_orders]

		heroes = list()
		heroes.extend(radiant_bans)
		heroes.extend(radiant_picks)
		heroes.extend(dire_bans)
		heroes.extend(dire_picks)

		features = list()
		for hero in heroes:
			features.extend(HeroFeatureExtractor.extract(hero))

		w.write(",".join(str(x) for x in features))
		w.write('\n')

	w.close()


def getExamples(from_file):
	dataset = np.genfromtxt(from_file, delimiter = ',')
	X = dataset[:,1:-1] #Rest of attributes
	y = dataset[:,0] #Target

	n_sample = len(X) # from plot_iris_exercise.py

	np.random.seed(0)
	order = np.random.permutation(n_sample)
	X = X[order]
	y = y[order].astype(np.float)

	X_train = X[:.9 * n_sample]
	y_train = y[:.9 * n_sample]
	X_test = X[.9 * n_sample:]
	y_test = y[.9 * n_sample:]

	return ((X_train, y_train), (X_test, y_test))


def doDecisionTree(train, test):
	clf = tree.DecisionTreeClassifier()
	clf = clf.fit(train[0], train[1])

	with open("Proto.dot", 'w') as f:
		f = tree.export_graphviz(clf, feature_names=range(0, len(train[0])),  
							class_names=["Dire","Radiant"],  
							filled=True, rounded=True,  
							special_characters=True, out_file=f)
	

def doLogisticRegression(train, test):
	lr = linear_model.LogisticRegression()
	lr.fit(train[0], train[1])
	print "Average performance: %s" % lr.score(test[0], test[1])


def main():
	parser = argparse.ArgumentParser(description='Predict some Dota winners.')
	parser.add_argument('-i', '--input_file', type=str, default=INPUT_FILE_DEFAULT,
					help='File to read example matches from')
	parser.add_argument('-o', '--output_file', type=str, default=OUTPUT_FEATURE_FILE_DEFAULT,
					help='File to output extracted features to')
	parser.add_argument('-m', '--model', type=str,
					help='Model to use for predictions')
	args = parser.parse_args()

	buildExamples(input_file=args.input_file, output_file=args.output_file)
	train, test = getExamples(args.output_file)

	if args.model == "lr":
		doLogisticRegression(train, test)
	elif args.model == "dt":
		doDecisionTree(train, test)
	else:
		doDecisionTree(train, test)


if __name__ == "__main__":
	main()
