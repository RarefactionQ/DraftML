import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets, svm, linear_model

hero_list = ['Abaddon','Alchemist','Ancient Apparition','Anti Mage','Arc Warden','Axe','Bane','Batrider','Beastmaster','Bloodseeker','Bounty Hunter','Brewmaster','Bristleback','Broodmother','Centaur Warrunner','Chaos Knight','Chen','Clinkz','Clockwerk','Crystal Maiden','Dark Seer','Dazzle','Death Prophet','Disruptor','Doom','Dragon Knight','Drow Ranger','Earth Spirit','Earthshaker','Elder Titan','Ember Spirit','Enchantress','Enigma','Faceless Void','Gyrocopter','Huskar','Invoker','Io','Jakiro','Juggernaut','Keeper of the Light','Kunkka','Legion Commander','Leshrac','Lich','Lifestealer','Lina','Lion','Lone Druid','Luna','Lycan','Magnus','Medusa','Meepo','Mirana','Morphling','Naga Siren','Natures Prophet','Necrophos','Night Stalker','Nyx Assassin','Ogre Magi','Omniknight','Oracle','Outworld Devourer','Phantom Assassin','Phantom Lancer','Phoenix','Pit Lord','Puck','Pudge','Pugna','Queen of Pain','Razor','Riki','Rubick','Sand King','Shadow Demon','Shadow Fiend','Shadow Shaman','Silencer','Skywrath Mage','Slardar','Slark','Sniper','Spectre','Spirit Breaker','Storm Spirit','Sven','Techies','Templar Assassin','Terrorblade','Tidehunter','Timbersaw','Tinker','Tiny','Treant Protector','Troll Warlord','Tusk','Undying','Ursa','Vengeful Spirit','Venomancer','Viper','Visage','Warlock','Weaver','Windranger','Winter Wyvern','Witch Doctor','Wraith King','Zeus']

hero_dict = {}
i = 0
for hero in hero_list:
	i += 1
	hero_dict[hero] = i

# for key in hero_dict:
# 	print str(hero_dict[key])+' '+key

f = open('draft.txt', 'r+')
w = open('Proto.csv', 'r+')
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
	w.write(str(hero_dict[attributes[3]])+'.,') #1st ban
	w.write(str(hero_dict[attributes[8]])+'.,') #2nd ban
	w.write(str(hero_dict[attributes[13]])+'.,') #3rd ban
	w.write(str(hero_dict[attributes[18]])+'.,') #4th ban
	w.write(str(hero_dict[attributes[23]])+'.,') #1st pick
	w.write(str(hero_dict[attributes[28]])+'.,') #2nd pick
	w.write(str(hero_dict[attributes[33]])+'.,') #3rd pick
	w.write(str(hero_dict[attributes[38]])+'.,') #4th pick
	w.write(str(hero_dict[attributes[43]])+'.,') #5th ban
	w.write(str(hero_dict[attributes[48]])+'.,') #6th ban
	w.write(str(hero_dict[attributes[53]])+'.,') #7th ban
	w.write(str(hero_dict[attributes[58]])+'.,') #8th ban
	w.write(str(hero_dict[attributes[63]])+'.,') #5th pick
	w.write(str(hero_dict[attributes[68]])+'.,') #6th pick
	w.write(str(hero_dict[attributes[73]])+'.,') #7th pick
	w.write(str(hero_dict[attributes[78]])+'.,') #8th pick
	w.write(str(hero_dict[attributes[83]])+'.,') #9th ban
	w.write(str(hero_dict[attributes[88]])+'.,') #10th ban
	w.write(str(hero_dict[attributes[93]])+'.,') #9th pick
	w.write(str(hero_dict[attributes[98]])+'.,') #10th pick
	w.write('\n')

w.close()
dataset = np.genfromtxt('Proto.csv', delimiter = ',')
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

regr = linear_model.Lasso()
scores = [regr.set_params(alpha=alpha).fit(X_train, y_train).score(X_test, y_test) for alpha in alphas]
best_alpha = alphas[scores.index(max(scores))]
regr.alpha = best_alpha
print regr.fit(X_train, y_train)
print(regr.coef_)