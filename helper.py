
import _pickle as pickle

from Components import Comment, Post, POSPost, POSComment

def load_v1():
	data_total = []
	for i in range(6):
		data = pickle.load(open("data/v1-{}".format(i), "rb"))
		data_total += data
	print("- Loaded v1")
	return data_total

def load_v2():
	data_total = []
	for i in range(6):
		data = pickle.load(open("data/v2-{}".format(i), "rb"))
		data_total += data
	print("- Loaded v2")
	return data_total
