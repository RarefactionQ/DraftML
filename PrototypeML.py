import argparse
import csv
import numpy as np
import matplotlib.pyplot as plt

from sklearn import datasets, svm, linear_model, preprocessing, tree
from IPython.display import Image
from sklearn.externals.six import StringIO

from feature_extractors.hero_feature_extractor import HeroFeatureExtractor
from feature_extractors.hero_set_feature_extractor import HeroSetFeatureExtractor
from feature_extractors.team_feature_extractor import TeamFeatureExtractor

INPUT_FILE_DEFAULT = 'draft.txt'
OUTPUT_FEATURE_FILE_DEFAULT = 'Proto.csv'

def buildExamples(input_file, output_file):
	f = open(input_file, 'r+')
	w = open(output_file, 'w')
	draft_list = f.read().split('\n')

	for draft in draft_list:
		attributes = draft.split(',')
		# print len(attributes)
		if len(attributes) != 102: #getting rid of malformed games
			print len(attributes)
			continue
		w.write("%s.0," % attributes[0]) #winner

		features = list()
		feature_names = list()

		feature_names.append("Who Went First")
		if attributes[5] == 'Radiant':
			features.append(1.0)
		elif attributes[5] == 'Dire':
			features.append(0.0)
		else:
			features.append(-1.0)

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

		radiant_team = attributes[4]
		dire_team = attributes[9]

		features = list()
		feature_names = list()

#		hfe = HeroFeatureExtractor()
#		for index, hero in enumerate(radiant_bans):
#			features.extend(hfe.extract(hero))
#			feature_names.extend(["radiant_ban_%s:%s" % (index, x) for x in hfe.extractFeatureNames()])
#
#		for index, hero in enumerate(radiant_picks):
#			features.extend(hfe.extract(hero))
#			feature_names.extend(["radiant_pick_%s:%s" % (index, x) for x in hfe.extractFeatureNames()])
#			names = zip(feature_names,features)
#			# for name in names:
#			#  	print str(name[0])+" "+str(name[1])
#		for index, hero in enumerate(dire_bans):
#			features.extend(hfe.extract(hero))
#			feature_names.extend(["dire_ban_%s:%s" % (index, x) for x in hfe.extractFeatureNames()])
#		for index, hero in enumerate(dire_picks):
#			features.extend(hfe.extract(hero))
#			feature_names.extend(["dire_pick_%s:%s" % (index, x) for x in hfe.extractFeatureNames()])
#
#		hsfe = HeroSetFeatureExtractor()
#		features.extend(hsfe.extract(radiant_picks))
#		feature_names.extend(["radiant_picks_%s" % x for x in hsfe.extractFeatureNames()])
#		features.extend(hsfe.extract(radiant_bans))
#		feature_names.extend(["radiant_bans_%s" % x for x in hsfe.extractFeatureNames()])
#		features.extend(hsfe.extract(dire_picks))
#		feature_names.extend(["dire_picks_%s" % x for x in hsfe.extractFeatureNames()])
#		features.extend(hsfe.extract(dire_bans))
#		feature_names.extend(["dire_bans_%s" % x for x in hsfe.extractFeatureNames()])

		tfe = TeamFeatureExtractor()
		features.extend(tfe.extract(radiant_team))
		feature_names.extend(["radiant_team_%s" % x for x in tfe.extractFeatureNames()])
		features.extend(tfe.extract(dire_team))
		feature_names.extend(["dire_team_%s" % x for x in tfe.extractFeatureNames()])

		w.write(",".join(str(x) for x in features))
		w.write('\n')

	w.close()

	with open("features_" + output_file, 'w') as w:
		w.write(",".join(feature_names))
		w.close()


def getExamples(from_file):
	dataset = np.genfromtxt(from_file, delimiter = ',')
	X = dataset[:,1:] #Rest of attributes
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

def doDecisionTree(train, test, feature_names_file):	
	clf = tree.DecisionTreeClassifier()
	clf = clf.fit(train[0], train[1])

	precog = clf.predict(test[0])
	results = zip(precog,test[1])
	correct = 0
	for result in results:
	 	# print "Predicted"+" "+str(result[0])+" actual:"+str(result[1])
	 	if result[0] == result[1]:
	 		correct += 1

	accuracy = float(correct) / float(len(results))
	print "Total accuracy: "+str(accuracy)

	with open(feature_names_file, 'r') as f:
		reader = csv.reader(f)
		feature_names = reader.next()

	with open("Proto.dot", 'w') as f:
		f = tree.export_graphviz(clf, feature_names=feature_names,  
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
		doDecisionTree(train, test, "features_" + args.output_file)
	else:
		doDecisionTree(train, test, "features_" + args.output_file)


if __name__ == "__main__":
	main()
