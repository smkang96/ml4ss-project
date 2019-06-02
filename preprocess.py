
from tqdm import tqdm
import _pickle as pickle
from konlpy.tag import Okt

from Components import Comment, Post, POSPost, POSComment

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

def filter_pos(pos_list):
	allowed_tags = set(['Noun', 'Verb', 'Adjective'])
	stopwords = set(['하다', '있다', '되다', '이다', '같다', '없다'])
	return [pos for pos in pos_list if pos[1] in allowed_tags and pos[0] not in stopwords]

def preprocess(index, data):
	save = []

	for p, post in tqdm(enumerate(data), total=len(data)):
		title, body, categories = clean_post(post.text)

		title_pos, body_pos = posify(title), posify(body)
		title_pos_filtered, body_pos_filtered = filter_pos(title_pos), filter_pos(body_pos)
		pp = POSPost(title, body, title_pos, title_pos_filtered, body_pos, body_pos_filtered, categories)

		for comment in post.comments:
			comment_pos = posify(comment.text)
			comment_pos_filtered = filter_pos(comment_pos)
			cp = POSComment(comment.text, comment_pos, comment_pos_filtered)

			for reply in comment.replies:
				reply_pos = posify(reply.text)
				reply_pos_filtered = filter_pos(reply_pos)
				rp = POSComment(reply.text, reply_pos, reply_pos_filtered)
				cp.add_comment(rp)

			pp.add_comment(cp)

		save.append(pp)

	pickle.dump(save, open("data/v2-{}".format(index), "wb+"))

if __name__ == '__main__':
	N = 6
	datas = []

	for i in range(N):
		d = pickle.load(open("data/v1-{}".format(i), "rb"))
		datas.append(d)

	okt = Okt()

	for i, data in enumerate(datas):
		preprocess(i, data)
