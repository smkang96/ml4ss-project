
import _pickle as pickle
from Components import Comment, Post, POSPost, POSComment

def get_stats():
	pass

if __name__ == '__main__':
	N = 6
	v1, v2 = [], []

	for i in range(N):
		d1 = pickle.load(open("data/v1-{}".format(i), "rb"))
		d2 = pickle.load(open("data/v2-{}".format(i), "rb"))
		v1.append(d1)
		v2.append(d2)

	## Total
	total = 0
	for v in v1:
		total += len(v)
	print("total {}".format(total))

	## Average
	length, reactions, comments = 0, 0, 0
	for n in range(N):
		for i, post in enumerate(v1[n]):
			length += len(v2[n][i].body)

			r = post.like + post.haha + post.love + post.love + post.sad + post.angry
			reactions += r

			comment_count = len(post.comments)
			for comment in post.comments:
				comment_count += len(comment.replies)
			comments += comment_count

	print("average length {}".format(length / total))
	print("average reactions {}".format(reactions / total))
	print("average comments {}".format(comments / total))

	## Longest, most likes, most comments
	# max_longest, max_likes, max_comments = 0, 0, 0
	# n_longest, n_likes, n_comments = 0, 0, 0
	# i_longest, i_likes, i_comments = 0, 0, 0

	# for n in range(N):
	# 	for i, post in enumerate(v1[n]):
	# 		if len(v2[n][i].body) > max_longest:
	# 			max_longest, n_longest, i_longest = len(v2[n][i].body), n, i

	# 		reactions = post.like + post.haha + post.love + post.love + post.sad + post.angry
	# 		if reactions > max_likes:
	# 			max_likes, n_likes, i_likes = reactions, n, i

			# comment_count = len(post.comments)
			# for comment in post.comments:
			# 	comment_count += len(comment.replies)

			# if comment_count > max_comments:
			# 	max_comments, n_comments, i_comments = comment_count, n, i

	# print("longest {}".format(v1[n_longest][i_longest].href))
	# print("likes {}".format(v1[n_likes][i_likes].href))
	# print("comments {}".format(v1[n_comments][i_comments].href))

	## Print an example
	# index = 151
	# print(v1_0[index].href)
	# print(v1_0[index].text)
	# print(v2_0[index].title)
	# print(v2_0[index].title_pos)
	# print(v2_0[index].body)
	# print(v2_0[index].body_pos)
	# print(v2_0[index].categories)