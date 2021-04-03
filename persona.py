import pickle
import os

try:
    os.mkdir('data')
except:
	pass

class Persona:
	@staticmethod
	def get(id):
		try:
			p = pickle.load(open('data/personna-id-'+str(id)+'.pkl','rb'))
			return p
		except:
			return Persona(id)

	def __init__(self, id):
		self.id = id
		self.FavoriteCategories = set()
		self.lastIntent = 'greeting'

	def addFavoriteCategory(self, category):
		self.FavoriteCategories.add(category)
		self.save()

	def setLastIntent(self, intent):
		self.lastIntent = intent

	def save(self):
		pickle.dump(self, open('data/personna-id-'+str(self.id)+'.pkl','wb'))
