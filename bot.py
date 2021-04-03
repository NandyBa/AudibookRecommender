import recommender

def greeting(persona, kind, category = None):
	return "Hi! we are a chatbot and recommendation system specialized in audiobooks."

def different(persona, kind, category = None):
	message = "The categories are:\n"
	for category in recommender.category_list():
		message += category+'\n'

	return message

def all(persona, kind, category = None):
	f = globals()[kind]
	return f(persona, kind, None)

def specific(persona, kind, category):
	f = globals()[kind+'_category']
	return f(persona, kind, category)


def author_category(persona, kind, category):
	message = ''
	if persona.FavoriteCategories == set() or category != None:
		if category == None:
			message = "Please specify some categories you liked"
		else:
			persona.addFavoriteCategory(category)
	
	if persona.FavoriteCategories != set():
		for category in persona.FavoriteCategories:
			message += recommender.recommender_author(category)+'\n\n'
	return message

def author(persona, kind, category):
	message = recommender.recommender_author_all_categories()
	return message

def narrator_category(persona, kind, category):
	message = ''
	if persona.FavoriteCategories == set() or category != None:
		if category == None:
			message = "Please specify some categories you liked"
		else:
			persona.addFavoriteCategory(category)
	
	if persona.FavoriteCategories != set():
			for category in persona.FavoriteCategories:
				message += recommender.recommender_narrator(category)+'\n\n'
	return message

def narrator(persona, kind, category):
	message = recommender.recommender_narrator_all_categories()
	return message

def author_narrator_category(persona, kind, category):
	message = ''
	if persona.FavoriteCategories == set() or category != None:
		if category == None:
			message = "Please specify some categories you liked"
		else:
			persona.addFavoriteCategory(category)
	
	if persona.FavoriteCategories != set():
			for category in persona.FavoriteCategories:
				message += recommender.recommender_author_narrator(category)+'\n\n'
	return message

def author_narrator(persona, kind, category):
	message = recommender.recommender_author_narrator_all_categories()
	return message

