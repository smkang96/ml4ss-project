
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
		title, body, categories = clean_post(post.text)

		title_pos, body_pos = posify(title), posify(body)
		pp = POSPost(title, body, title_pos, body_pos, categories)

		for comment in post.comments:
			comment_pos = posify(comment.text)
			cp = POSComment(comment.text, comment_pos)

			for reply in comment.replies:
				reply_pos = posify(reply.text)
				rp = POSComment(reply.text, reply_pos)
				cp.add_comment(rp)

			pp.add_comment(cp)

		save.append(pp)

	pickle.dump(save, open("data/v2-{}".format(index), "wb+"))

		# print(post.text)
		# print(pp)

		# for i in range(len(post.comments)):
		# 	print("  " + str(post.comments[i].text))
		# 	print("  " + str(pp.comments[i]))
		# 	for j in range(len(post.comments[i].replies)):
		# 		print("    " + str(post.comments[i].replies[j]))
		# 		print("    " + str(pp.comments[i].comments[j]))

if __name__ == '__main__':
	N = 6
	datas = []

	for i in range(N):
		d = pickle.load(open("data/v1-{}".format(i), "rb"))
		datas.append(d)

	okt = Okt()

	for i, data in enumerate(datas):
		preprocess(i, data)
