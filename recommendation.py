import numpy as np
import pandas as pd
import pickle
import time
import threading
import os

try:
    os.mkdir('data')
except:
	pass

def timer(f):
	def wrapper(*args, **kwargs):
		t = time.time()
		r = f(*args, **kwargs)
		print(time.time()-t)
		return r
	return wrapper

df = pd.read_csv("all_english_audible.csv")

df = df.sample(frac=1).reset_index(drop=True)
df = df.iloc[:20000]



category_list = df.category.unique()

def genre_binary_encoder(category):
	n = len(category_list)
	index = np.argmax(category_list==category)
	r = np.array([0]*(index)+[1]*1+[0]*(n-index-1))
	return r




df.drop(["asin"], axis=1, inplace=True)
df.dropna(inplace=True)

try:
	genres = pickle.load(open('data/genres.pkl','rb'))
except:
	genres = []
	for i in range(len(df)):
	  L = genre_binary_encoder(df.iloc[i]['category'])
	  genres.append(L)
	genres = pd.DataFrame(genres)
	genres.columns = category_list
	pickle.dump(genres,open('data/genres.pkl','wb'))

# df.drop(["category"], axis=1, inplace=True)



Data = df.merge(genres, left_index=True, right_index=True)



# drop duplicate couple, 218918 insted of 460544
# print(len(df[["author","narrator"]].drop_duplicates(keep='first')))
# print(len(df[["author","narrator"]]))
author_narrator = df[["author","narrator"]].drop_duplicates(keep='first')


def log_utility(oeuvres):
	s = 0
	if len(oeuvres) == 0:
		return 0

	for _, oeuvre in oeuvres.iterrows():
		s+= oeuvre.rating * np.log(1+oeuvre.rating_count)
	return s/len(oeuvres)

def couple_category(oeuvres):
	s = set()
	for _, oeuvre in oeuvres.iterrows():
		s.add(oeuvre.category)
	return s


def thread_process_log_utility(j, nb_lots, dataset, category, typeRecommandation):
	try:
		log_utility_j = pickle.load(open('data/log_utility-'+typeRecommandation+'-'+category+'-'+str(j)+'on'+str(nb_lots)+'.pkl','rb'))

	except:

		if typeRecommandation == "author-narrator":
			Author = pd.Series(dtype='str', name="Author")
			Narrator = pd.Series(dtype='str', name="Narrator")
			Log_utility = pd.Series(dtype='int', name="Log utility")
			for i in range(j*len(dataset)//nb_lots, (j+1)*len(dataset)//nb_lots):
				author, narrator = dataset.iloc[i]
				oeuvres = df[(df['author'] == author) & (df['narrator'] == narrator)]
				Author[str(i)] = author
				Narrator[str(i)] = narrator
				Log_utility[str(i)] = log_utility(oeuvres)

			log_utility_j = pd.DataFrame({ "Author": Author, "Narrator": Narrator, "Log utility": Log_utility})

			pickle.dump(log_utility_j,open('data/log_utility-'+typeRecommandation+'-'+category+'-'+str(j)+'on'+str(nb_lots)+'.pkl','wb'))

		elif typeRecommandation == "author":
			Author = pd.Series(dtype='str', name="Author")
			Log_utility = pd.Series(dtype='int', name="Log utility")
			for i in range(j*len(dataset)//nb_lots, (j+1)*len(dataset)//nb_lots):
				author= dataset.iloc[i].iloc[0]
				oeuvres = df[(df['author'] == author)]
				Author[str(i)] = author
				Log_utility[str(i)] = log_utility(oeuvres)

			log_utility_j = pd.DataFrame({ "Author": Author, "Log utility": Log_utility})

			pickle.dump(log_utility_j,open('data/log_utility-'+typeRecommandation+'-'+category+'-'+str(j)+'on'+str(nb_lots)+'.pkl','wb'))

		elif typeRecommandation == "narrator":
			Narrator = pd.Series(dtype='str', name="Narrator")
			Log_utility = pd.Series(dtype='int', name="Log utility")
			for i in range(j*len(dataset)//nb_lots, (j+1)*len(dataset)//nb_lots):
				narrator = dataset.iloc[i].iloc[0]
				oeuvres = df[(df['narrator'] == narrator)]
				Narrator[str(i)] = narrator
				Log_utility[str(i)] = log_utility(oeuvres)

			log_utility_j = pd.DataFrame({ "Narrator": Narrator, "Log utility": Log_utility})

			pickle.dump(log_utility_j,open('data/log_utility-'+typeRecommandation+'-'+category+'-'+str(j)+'on'+str(nb_lots)+'.pkl','wb'))


def run_thread_log_utility_category(category, typeRecommandation):
	threads =[]

	if typeRecommandation == 'author':
		dataset = df[(df['category'] == category)][["author"]].drop_duplicates(keep='first')
	elif typeRecommandation == 'narrator':
		dataset = df[(df['category'] == category)][["narrator"]].drop_duplicates(keep='first')
	elif typeRecommandation == 'author-narrator':
		dataset = df[(df['category'] == category)][["author","narrator"]].drop_duplicates(keep='first')
	else:
		dataset = pd.DataFrame()

	nb_lots = 10
	for i in range(0,nb_lots):
		t = threading.Thread(target=thread_process_log_utility(i, nb_lots, dataset, category, typeRecommandation))
		t.daemon = True
		threads.append(t)

	for i in range(0,nb_lots):
		threads[i].start()

	for i in range(0,nb_lots):
		threads[i].join()

def get_log_utility(category, typeRecommandation):
	try:
		d = pickle.load(open('data/log_utility-'+typeRecommandation+'-'+category+'.pkl','rb'))
	except:	
		nb_lots = 10
		d = None
		run_thread_log_utility_category(category, typeRecommandation)

		if typeRecommandation in ["author","author-narrator"]:
			Author = pd.Series(dtype='str', name="Author")

		if typeRecommandation in ["narrator","author-narrator"]:
			Narrator = pd.Series(dtype='str', name="Narrator")

		Log_utility = pd.Series(dtype='int', name="Log utility")


		if typeRecommandation == "author-narrator":
			d = pd.DataFrame({ "Author": Author, "Narrator": Narrator, "Log utility": Log_utility})
		elif typeRecommandation == "auhor":
			d = pd.DataFrame({ "Author": Author, "Log utility": Log_utility})
		elif typeRecommandation == "narrator":
			d = pd.DataFrame({ "Narrator": Narrator, "Log utility": Log_utility})



		for i in range(0,nb_lots):
			filei = 'data/log_utility-'+typeRecommandation+'-'+category+'-'+str(i)+'on'+str(nb_lots)+'.pkl'
			di = pickle.load(open(filei,'rb'))
			d = pd.concat([d,di])
			os.remove(filei)
		pickle.dump(d,open('data/log_utility-'+typeRecommandation+'-'+category+'.pkl','wb'))
	return d


def compile_author_narrator_log_utility_for_all_categories():
	for category in df.category.unique():
		get_author_narrator_log_utility(category)

# Lancer cette fonction lors du déploiement du bot
# compile_author_narrator_log_utility_for_all_categories()


def recommender_author_narrator(category, nb = 5):
	df = get_log_utility(category, "author-narrator")
	df = df.sort_values('Log utility', ascending = False).iloc[:nb]
	return df

def recommender_author(category, nb = 5):
	df = get_log_utility(category, "author")
	df = df.sort_values('Log utility', ascending = False).iloc[:nb]
	return df

def recommender_narrator(category, nb = 5):
	df = get_log_utility(category, "narrator")
	df = df.sort_values('Log utility', ascending = False).iloc[:nb]
	return df

@timer
def recommender_author_narrator_all_categories(nb = 5):

	Author = pd.Series(dtype='str', name="Author")
	Narrator = pd.Series(dtype='str', name="Narrator")
	Log_utility = pd.Series(dtype='int', name="Log utility")
	d = pd.DataFrame({ "Author": Author, "Narrator": Narrator, "Log utility": Log_utility})

	for category in category_list:
		di = recommender_author_narrator(category, nb)
		d = pd.concat([d, di])
	d = d.sort_values('Log utility', ascending = False).iloc[:nb]
	return d

@timer
def recommender_author_all_categories(nb = 5):

	Author = pd.Series(dtype='str', name="Author")
	Log_utility = pd.Series(dtype='int', name="Log utility")
	d = pd.DataFrame({ "Author": Author ,"Log utility": Log_utility})

	for category in category_list:
		di = recommender_author(category, nb)
		d = pd.concat([d, di])
	d = d.sort_values('Log utility', ascending = False).iloc[:nb]
	return d

@timer
def recommender_narrator_all_categories(nb = 5):

	Narrator = pd.Series(dtype='str', name="Narrator")
	Log_utility = pd.Series(dtype='int', name="Log utility")
	d = pd.DataFrame({ "Narrator": Narrator, "Log utility": Log_utility})

	for category in category_list:
		di = recommender_narrator(category, nb)
		d = pd.concat([d, di])
	d = d.sort_values('Log utility', ascending = False).iloc[:nb]
	return d

def categories_list():
	return df.category.unique()
