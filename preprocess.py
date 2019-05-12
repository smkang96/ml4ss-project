
from tqdm import tqdm
import _pickle as pickle
from Components import Comment, Post, POSPost, POSComment
from konlpy.tag import Okt

def clean_post(text):
	text_split = text.split("\n----------\n")

	title, body, categories = None, None, []
	
	if len(text_split) < 2:
		text_without_footer = text
	else:
		text_without_footer = "\n----------\n".join(text_split[:-1])
		if text_split[-1][0] == '#':
			categories = text_split[-1].split("\n")[0].split()

	text_split = text_without_footer.split("\n")
	title = text_split[0]
	body = "\n".join(text_split[1:])

	return title, body, categories


def posify(text):
	morphs = okt.pos(text, norm=True, stem=True)
	return morphs

def preprocess(index, data):
	save = []

	for p, post in tqdm(enumerate(data), total=len(data)):
		if len(post.comments) == 0: continue

		title, body, categories = clean_post(post.text)

		title_pos, body_pos = posify(title), posify(body)
		pp = POSPost(title_pos, body_pos, categories)

		for comment in post.comments:
			comment_pos = posify(comment.text)
			cp = POSComment(comment_pos)

			for reply in comment.replies:
				reply_pos = posify(reply.text)
				rp = POSComment(reply_pos)
				cp.add_comment(rp)

			pp.add_comment(cp)

		save.append(pp)

		# print(post.text)
		# print(pp)

		# for i in range(len(post.comments)):
		# 	print("  " + str(post.comments[i].text))
		# 	print("  " + str(pp.comments[i]))
		# 	for j in range(len(post.comments[i].replies)):
		# 		print("    " + str(post.comments[i].replies[j]))
		# 		print("    " + str(pp.comments[i].comments[j]))

	pickle.dump(save, open("data/v2-{}".format(index), "wb+"))

if __name__ == '__main__':
	d1 = pickle.load(open("data/v1-0", "rb"))
	d2 = pickle.load(open("data/v1-1", "rb"))
	d3 = pickle.load(open("data/v1-2", "rb"))
	d4 = pickle.load(open("data/v1-3", "rb"))
	datas = [d1, d2, d3, d4]

	okt = Okt()

	for i, data in enumerate(datas):
		preprocess(i, data)
