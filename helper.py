
from datetime import datetime
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

def normalize_date(date, min_value=0):
	assert min_value < 1

	min_date, max_date = 1503479520.0, 1556428440.0 # 2017-08-23 18:12:00, 2019-04-28 14:14:00
	range_date = max_date - min_date

	return min_value + ((date.timestamp() - min_date) * (1 - min_value) / range_date)