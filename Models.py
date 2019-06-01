
from collections import defaultdict
from tqdm import tqdm
import numpy as np
from sklearn.cluster import MiniBatchKMeans
from gensim.corpora import Dictionary
from gensim.models import TfidfModel, LdaModel
from gensim.models.coherencemodel import CoherenceModel

from Components import Comment, Post, POSPost, POSComment
from helper import *

class MyDictionary:
	def __init__(self, posPosts, title_weight=1, use_comments=False):
		self.title_weight = title_weight
		self.use_comments = use_comments
		self.words_list = self.get_words_list(posPosts, self.title_weight, self.use_comments)
		self.dictionary = Dictionary(self.words_list)
		self.doc2bows = [self.dictionary.doc2bow(words) for words in self.words_list]
		print("- Created MyDictionary of {} words".format(len(self.dictionary)))

	def get_words_list(self, posPosts, title_weight, use_comments):
		words_list = []
		for posPost in posPosts:
			words = [pair[0] for pair in posPost.body_pos_filtered]
			title_words = [pair[0] for pair in posPost.title_pos_filtered]
			for i in range(title_weight):
				words += title_words
			if use_comments:
				for comment in posPost.comments:
					words += [pair[0] for pair in comment.text_pos_filtered]
					for reply in comment.comments:
						words += [pair[0] for pair in reply.text_pos_filtered]
			words_list.append(words)
		return words_list

class MyTfidf:
	def __init__(self, myDictionary, smartirs='ntc'):
		self.myDictionary = myDictionary
		self.model = TfidfModel(self.myDictionary.doc2bows, smartirs=smartirs)
		self.clustering = None
		self.vectors = None
		print("- Created MyTfidf")

	def get_doc2bow(self, index):
		words = self.myDictionary.doc2bows[index]
		return self.model[words]

	def get_vector(self, index):
		if self.vectors:
			return self.vectors[index]

		doc2bow = self.get_doc2bow(index)
		vector = np.zeros(len(self.myDictionary.dictionary))
		for i, v in doc2bow:
			vector[i] = v
		return vector

	def get_vectors(self):
		if self.vectors:
			return self.vectors

		vectors = []
		for i in range(len(self.myDictionary.doc2bows)):
			vectors.append(self.get_vector(i))
		return vectors

	def cluster(self, n_clusters, add_date=False, v1=None, min_value=0):
		if self.clustering:
			return self.clustering
		
		vectors = self.get_vectors()

		if add_date:
			assert v1 is not None, "v1 must not be None!"
			assert len(v1) == len(vectors), "Lengths do not match!"
			for i, vector in enumerate(vectors):
				date_normalized = normalize_date(v1[i].date, min_value=min_value)
				np.append(vector, [date_normalized])

		self.clustering = MiniBatchKMeans(n_clusters=n_clusters)
		self.clustering.fit(vectors)
		self.clusters = defaultdict(list)
		for document_index, label in enumerate(self.clustering.labels_):
			self.clusters[label].append(document_index)

class MyLda:
	def __init__(self, myDictionary, num_topics=100):
		self.num_topics = num_topics
		self.myDictionary = myDictionary
		self.model = LdaModel(self.myDictionary.doc2bows, \
			id2word=self.myDictionary.dictionary, \
			num_topics=num_topics)
		self.coherenceModel = None
		print("- Created MyLda with {} topics".format(self.num_topics))

	def get_document_topics(self, document_index):
		doc2bow = self.myDictionary.doc2bows[document_index]
		return self.model.get_document_topics(doc2bow)

	def get_top_topic(self):
		top_topics = self.model.top_topics(corpus=self.myDictionary.doc2bows)
		average = sum([t[1] for t in top_topics]) / self.num_topics
		return top_topics, average

	def get_perplexity(self):
		return self.model.log_perplexity(self.myDictionary.doc2bows)

	def get_coherence(self):
		if not self.coherenceModel:
			self.coherenceModel = CoherenceModel(model=self.model, \
				corpus=self.myDictionary.doc2bows, \
				dictionary=self.myDictionary.dictionary, \
				coherence='u_mass')
		return self.coherenceModel.get_coherence()


if __name__  == '__main__':
	v1 = load_v1()

	# v2 = load_v2()
	# myDictionary = MyDictionary(v2, title_weight=1, use_comments=False)

	## DFs
	# words = list(myDictionary.dictionary.items())
	# word_dfs = [(myDictionary.dictionary.dfs[word_index] / len(v2), word) for word_index, word in words]
	# word_dfs.sort(key=lambda p: p[0], reverse=True)
	# print(word_dfs[:30])

	indices = [10, 100, 1000, 10000]
	index = 10000
		
	## TFIDF
	# myTfIdf = MyTfidf(myDictionary)
	# vectors = myTfIdf.get_vectors()
	# myTfIdf.cluster(100)
	# clusters = sorted(myTfIdf.clusters.items(), key=lambda k: len(k[1]), reverse=True)
	# for cluster in clusters[:20]:
	# 	print("{} {}".format(cluster[0], len(cluster[1])))
	# for i in clusters[40][1]:
	# 	print(v2[i].title)
	# 	print(v2[i].body)
	# 	print("")

	# doc2bow = myTfIdf.get_doc2bow(index)
	# doc2bow.sort(key=lambda p: p[1], reverse=True)

	# print(v2[index].title)
	# print(v2[index].body)

	# for i, v in doc2bow:
	# 	print(myDictionary.dictionary[i], v)

	# vector = myTfIdf.get_vector(index)
	# for i, v in doc2bow:
	# 	print(vector[i])

	# myLda = MyLda(myDictionary)
	# top_topics, average = myLda.get_top_topic()
	
	# pprint(top_topics)
	# print(average)

	# for index in indices:
	# 	print(v2[index].body)
	# 	for topic, prob in myLda.get_document_topics(index):
	# 		print(topic, prob)
	# 		for word_id, word_prob in myLda.model.get_topic_terms(topic):
	# 			print("  {} {}".format(myDictionary.dictionary[word_id], word_prob))

	# for n in range(50, 501, 50):
	# 	myLda = MyLda(myDictionary, num_topics=n)
	# 	perplexity = myLda.get_perplexity()
	# 	coherence = myLda.get_coherence()
	# 	print("{:3d}: perplexity {:04.2f}, coherence {:04.2}".format(n, perplexity, coherence))

