
import os
import argparse
import _pickle as pickle
from tqdm import tqdm

from Components import Comment, Post, POSPost, POSComment
from Models import MyDictionary, MyTfidf, MyLda
from helper import load_v1, load_v2
from eval import load_eval_sets, evaluate

# SMARTIRS_LIST = ['ntc', 'ltc', 'lpc']
CLUSTER_SIZES = [50, 100, 150, 200, 250, 300, 400, 500]

def parse_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument('-c', action='store_true')
	parser.add_argument('-t', action='store_true', help="Run tf-idf")
	parser.add_argument('-l', action='store_true', help="Run LDA")
	return parser.parse_args()

def create_models():
	# Dictionaries
	if not os.path.isfile('models/dictionary/1_f'):
		dictionary_1_f = MyDictionary(v2, title_weight=1, use_comments=False)
		pickle.dump(dictionary_1_f, open("models/dictionary/1_f", "wb+"))

	if not os.path.isfile('models/dictionary/1_t'):
		dictionary_1_t = MyDictionary(v2, title_weight=1, use_comments=True)
		pickle.dump(dictionary_1_t, open("models/dictionary/1_t", "wb+"))

	dictionary_1_f = pickle.load(open("models/dictionary/1_f", "rb"))
	dictionary_1_t = pickle.load(open("models/dictionary/1_t", "rb"))

	# Tf-idf
	for size in CLUSTER_SIZES:
		name_f_d1f = 'models/tfidf/{}_f_d1f'.format(size)
		name_f_d1t = 'models/tfidf/{}_f_d1t'.format(size)
		name_t_d1f = 'models/tfidf/{}_t_d1f'.format(size)
		name_t_d1t = 'models/tfidf/{}_t_d1t'.format(size)

		if not os.path.isfile(name_f_d1f):
			tfidf_f_d1f = MyTfidf(dictionary_1_f)
			tfidf_f_d1f.cluster(size, add_date=False)
			pickle.dump(tfidf_f_d1f, open(name_f_d1f, "wb+"))

		if not os.path.isfile(name_f_d1t):
			tfidf_f_d1t = MyTfidf(dictionary_1_t)
			tfidf_f_d1t.cluster(size, add_date=False)
			pickle.dump(tfidf_f_d1t, open(name_f_d1t, "wb+"))

		if not os.path.isfile(name_t_d1f):
			tfidf_t_d1f = MyTfidf(dictionary_1_f)
			tfidf_t_d1f.cluster(size, add_date=True, v1=v1)
			pickle.dump(tfidf_t_d1f, open(name_t_d1f, "wb+"))

		if not os.path.isfile(name_t_d1t):
			tfidf_t_d1t = MyTfidf(dictionary_1_t)
			tfidf_t_d1t.cluster(size, add_date=True, v1=v1)
			pickle.dump(tfidf_t_d1t, open(name_t_d1t, "wb+"))

	# LDA
	for size in CLUSTER_SIZES:
		name_d1f = "models/lda/{}_d1f".format(size)
		name_d1t = "models/lda/{}_d1t".format(size)

		if not os.path.isfile(name_d1f):
			lda_d1f = MyLda(dictionary_1_f, num_topics=size)
			pickle.dump(lda_d1f, open(name_d1f, "wb+"))

		if not os.path.isfile(name_d1t):
			lda_d1t = MyLda(dictionary_1_t, num_topics=size)
			pickle.dump(lda_d1t, open(name_d1t, "wb+"))

def save_results(results_all, filename, eval_sets):
	eval_labels = list(eval_sets.keys())

	with open(filename, "w+") as f:
		for i, tuples in enumerate(results_all):
			f.write("{}\n".format(CLUSTER_SIZES[i]))

			for label, results in tuples:
				max_p_and_r = []
				for eval_label in eval_labels:
					precisions, recalls, clusters = results[eval_label]
					max_precision, max_recall = max(precisions), max(recalls)
					max_p_and_r.append("{:0.04f}|{:0.04f}".format(max_precision, max_recall))
				line = "{}|{}\n".format(label, "|".join(max_p_and_r))
				f.write(line)

def evaluate_tfidf(eval_sets):
	def _evaluate(tfidf, eval_sets):
		results = dict()

		for key, reference_set in eval_sets.items():
			precisions, recalls, clusters = [], [], set()
			for post in reference_set:
				cluster = tfidf.id2cluster[post]
				posts_in_cluster = tfidf.cluster2ids[cluster]
				precision, recall = evaluate(posts_in_cluster, reference_set)
				precisions.append(precision)
				recalls.append(recall)
				clusters.add(cluster)
			results[key] = (precisions, recalls, clusters)
		return results

	# Load models
	tfidfs_f_d1f, tfidfs_f_d1t, tfidfs_t_d1f, tfidfs_t_d1t = dict(), dict(), dict(), dict()

	for size in CLUSTER_SIZES:
		name_f_d1f = 'models/tfidf/{}_f_d1f'.format(size)
		name_f_d1t = 'models/tfidf/{}_f_d1t'.format(size)
		name_t_d1f = 'models/tfidf/{}_t_d1f'.format(size)
		name_t_d1t = 'models/tfidf/{}_t_d1t'.format(size)

		tfidfs_f_d1f[size] = pickle.load(open(name_f_d1f, "rb"))
		tfidfs_f_d1t[size] = pickle.load(open(name_f_d1t, "rb"))
		tfidfs_t_d1f[size] = pickle.load(open(name_t_d1f, "rb"))
		tfidfs_t_d1t[size] = pickle.load(open(name_t_d1t, "rb"))

	print("(evaluate_tfidf) Loaded models")

	# Evaluate
	results_all = []
	for size in CLUSTER_SIZES:
		tfidf_f_d1f = tfidfs_f_d1f[size]
		tfidf_f_d1t = tfidfs_f_d1t[size]
		tfidf_t_d1f = tfidfs_t_d1f[size]
		tfidf_t_d1t = tfidfs_t_d1t[size]

		results_f_d1f = _evaluate(tfidf_f_d1f, eval_sets)
		results_f_d1t = _evaluate(tfidf_f_d1t, eval_sets)
		results_t_d1f = _evaluate(tfidf_t_d1f, eval_sets)
		results_t_d1t = _evaluate(tfidf_t_d1t, eval_sets)

		pairs = (("Time N, Comments N", results_f_d1f),
				 ("Time N, Comments Y", results_f_d1t),
				 ("Time Y, Comments N", results_t_d1f),
				 ("Time Y, Comments Y", results_t_d1t))
		results_all.append(pairs)

	save_results(results_all, "results/tfidf.txt", eval_sets)
	pickle.dump(results_all, open("results/tfidf.pkl", "wb+"))
	print("(evaluate_tfidf) Finished evaluating")

def evaluate_lda(eval_sets):
	def _evaluate(lda, eval_sets):
		results = dict()

		for key, reference_set in eval_sets.items():
			precisions, recalls, topics = [], [], set()
			for post in reference_set:
				candidate_topics = lda.id2topics[post]
				this_precision, this_recall, this_topic = 0, 0, candidate_topics[0]
				for topic in candidate_topics:
					posts_in_topic = lda.topic2ids[topic]
					precision, recall = evaluate(posts_in_topic, reference_set)
					if recall > this_recall:
						this_precision, this_recall, this_topic = precision, recall, topic
				precisions.append(this_precision)
				recalls.append(this_recall)
				topics.add(this_topic)
			results[key] = (precisions, recalls, topics)
		return results

	# Load models
	ldas_d1f, ldas_d1t = dict(), dict()
	for size in CLUSTER_SIZES:
		name_d1f = 'models/lda/{}_d1f'.format(size)
		name_d1t = 'models/lda/{}_d1t'.format(size)

		ldas_d1f[size] = pickle.load(open(name_d1f, "rb"))
		ldas_d1t[size] = pickle.load(open(name_d1t, "rb"))

	print("(evaluate_lda) Loaded models")

	# Evalutate
	results_all = []
	for size in CLUSTER_SIZES:
		lda_d1f = ldas_d1f[size]
		lda_d1t = ldas_d1t[size]

		results_d1f = _evaluate(lda_d1f, eval_sets)
		results_d1t = _evaluate(lda_d1t, eval_sets)

		pairs = (("Comments N", results_d1f),
				 ("Comments Y", results_d1t))
		results_all.append(pairs)

	save_results(results_all, "results/lda.txt", eval_sets)
	pickle.dump(results_all, open("results/lda.pkl", "wb+"))
	print("(evaluate_lda) Finished evaluating")

if __name__ == '__main__':
	args = parse_arguments()
	v1, v2 = load_v1(), load_v2()

	### Create models ###
	if args.c:
		print("(main) Creating models")
		create_models()

	### Load models and evaluation data ###
	dictionary_1_f = pickle.load(open("models/dictionary/1_f", "rb"))
	dictionary_1_t = pickle.load(open("models/dictionary/1_t", "rb"))
	eval_sets = load_eval_sets() # Dict: (titles -> set of indices)

	### Tf-idf ###
	if args.t:
		print("(main) Running tf-idf")
		evaluate_tfidf(eval_sets)

	# LDA
	if args.l:
		print("(main) Running LDA")
		evaluate_lda(eval_sets)
		

