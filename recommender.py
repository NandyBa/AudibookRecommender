import recommendation


def recommender_author_narrator_all_categories():
	dataset = recommendation.recommender_author_narrator_all_categories()
	message = "I recommend you these author and narrator couples:\n"
	for i in range(len(dataset)):
		message += dataset.iloc[i].Author + '\n	|	' + dataset.iloc[i].Narrator + '	|	' + str(dataset.iloc[i]['Log utility'])+'\n'
	
	return message



def recommender_author_all_categories():
	dataset = recommendation.recommender_author_all_categories()
	message = "I recommend you these authors:\n"
	for i in range(len(dataset)):
		message += dataset.iloc[i].Author + '\n	|	' + str(dataset.iloc[i]['Log utility'])+'\n'
	
	return message

def recommender_narrator_all_categories():
	dataset = recommendation.recommender_narrator_all_categories()
	message = "I recommend you these narrators:\n"
	for i in range(len(dataset)):
		message += dataset.iloc[i].Narrator + '\n	|	' + str(dataset.iloc[i]['Log utility'])+'\n'
	
	return message

def recommender_author_narrator(category, nb = 5):
	dataset = recommendation.recommender_author_narrator(category, nb)
	message = "I recommend you these author and narrator couples on "+category+" category:\n"
	for i in range(len(dataset)):
		message += dataset.iloc[i].Author + '\n	|	' + dataset.iloc[i].Narrator + '	|	' + str(dataset.iloc[i]['Log utility'])+'\n'
	
	return message

def recommender_author(category, nb = 5):
	dataset = recommendation.recommender_author(category, nb)
	message = "I recommend you these authors on "+category+" category:\n"
	for i in range(len(dataset)):
		message += dataset.iloc[i].Author + '\n	|	' + str(dataset.iloc[i]['Log utility'])+'\n'
	
	return message

def recommender_narrator(category, nb = 5):
	dataset = recommendation.recommender_narrator(category, nb)
	message = "I recommend you these narrators on "+category+" category:\n"
	for i in range(len(dataset)):
		message += dataset.iloc[i].Narrator + '\n	|	' + str(dataset.iloc[i]['Log utility'])+'\n'
	
	return message

def categories_list():
	return recommendation.categories_list()

