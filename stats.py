
import _pickle as pickle
from Components import Comment, Post, POSPost, POSComment

def get_total():
	total = 0
	for v in v1:
		total += len(v)
	print("Total: {}\n".format(total))

def get_average():
	length, reactions, comments, total = 0, 0, 0, 0
	for n in range(N):
		total += len(v1[n])
		for i, post in enumerate(v1[n]):
			length += len(v2[n][i].body)

			r = post.like + post.haha + post.love + post.love + post.sad + post.angry
			reactions += r

			comment_count = len(post.comments)
			for comment in post.comments:
				comment_count += len(comment.replies)
			comments += comment_count

	print("Average length {}".format(length / total))
	print("Average reactions {}".format(reactions / total))
	print("Average comments {}\n".format(comments / total))

def get_examples():
	n, index = 0, 151
	print("Example {} {}".format(n, index))
	print(v1[n][index].href)
	print(v1[n][index].text)
	print(v2[n][index].title)
	print(v2[n][index].title_pos)
	print(v2[n][index].body)
	print(v2[n][index].body_pos)
	print(v2[n][index].categories)
	print("")

def get_extremes():
	max_longest, max_likes, max_comments = 0, 0, 0
	n_longest, n_likes, n_comments = 0, 0, 0
	i_longest, i_likes, i_comments = 0, 0, 0

	for n in range(N):
		for i, post in enumerate(v1[n]):
			if len(v2[n][i].body) > max_longest:
				max_longest, n_longest, i_longest = len(v2[n][i].body), n, i

			reactions = post.like + post.haha + post.love + post.love + post.sad + post.angry
			if reactions > max_likes:
				max_likes, n_likes, i_likes = reactions, n, i

			comment_count = len(post.comments)
			for comment in post.comments:
				comment_count += len(comment.replies)

			if comment_count > max_comments:
				max_comments, n_comments, i_comments = comment_count, n, i

	print("Longest {} {}".format(v1[n_longest][i_longest].href, max_longest))
	print("Likes {}".format(v1[n_likes][i_likes].href))
	print("Comments {}\n".format(v1[n_comments][i_comments].href))

if __name__ == '__main__':
	modes = set(["total", "average", "extremes", "example"])

	N = 6
	v1, v2 = [], []

	for i in range(N):
		d1 = pickle.load(open("data/v1-{}".format(i), "rb"))
		d2 = pickle.load(open("data/v2-{}".format(i), "rb"))
		v1.append(d1)
		v2.append(d2)


	if "total" in modes:
		get_total()
	if "average" in modes:
		get_average()
	if "extremes" in modes:
		get_extremes()
	if "example" in modes:
		get_examples()
