
class Comment:
	def __init__(self, text, like=0, haha=0, love=0, sad=0, wow=0, angry=0, parent=None):
		self.text = text
		self.like = like
		self.haha = haha
		self.love = love
		self.sad = sad
		self.wow = wow
		self.angry = angry
		self.parent = parent
		self.replies = []

	def __str__(self):
		short = "{}...".format(self.text[:7]) if len(self.text) > 10 else self.text
		parent = "Y" if self.parent else "N"
		count = len(self.replies)

		return "<COMMENT({}) text={} like={} haha={} love={} sad={} wow={} angry={} parent={}>"\
				.format(count, short, self.like, self.haha, self.love, self.sad, self.wow, self.angry, parent)

	def __repr__(self):
		return self.__str__()

	def set_like(self, count):
		self.count = count

	def set_haha(self, count):
		self.haha = count

	def set_love(self, count):
		self.love = count

	def set_sad(self, count):
		self.sad = count

	def set_wow(self, count):
		self.wow = count

	def set_angry(self, count):
		self.angry = count

	def set_parent(self, parent):
		self.parent = parent

	def add_reply(self, reply):
		self.replies.append(reply)

	def get_reactions(self):
		return self.like + self.haha + self.love + self.sad + self.wow + self.angry

class Post:
	def __init__(self, href, date, text, like=0, haha=0, love=0, sad=0, wow=0, angry=0):
		self.href = href
		self.date = date
		self.text = text
		self.like = like
		self.haha = haha
		self.love = love
		self.sad = sad
		self.wow = wow
		self.angry = angry
		self.comments = []

	def __str__(self):
		short = "{}...".format(self.text[:7]) if len(self.text) > 10 else self.text
		count = len(self.comments)

		return "<POST({}) text={} date={} like={} haha={} love={} sad={} wow={} angry={}>"\
				.format(count, short, self.date, self.like, self.haha, self.love, self.sad, self.wow, self.angry)

	def __repr__(self):
		return self.__str__()

	def add_comment(self, comment):
		self.comments.append(comment)

	def get_reactions(self):
		return self.like + self.haha + self.love + self.sad + self.wow + self.angry

class POSPost:
	def __init__(self, title_pos, body_pos, categories):
		self.title_pos = title_pos
		self.body_pos = body_pos
		self.categories = categories
		self.comments = []

	def add_comment(self, comment):
		self.comments.append(comment)

	def __str__(self):
		return "<POSPost({}) {}..., {}...>".format(len(self.comments),  str(self.title_pos)[:10], str(self.body_pos)[:10])

class POSComment:
	def __init__(self, text_pos):
		self.text_pos = text_pos
		self.comments = []

	def add_comment(self, comment):
		self.comments.append(comment)

	def __str__(self):
		return "<POSPost({}) {}...>".format(len(self.comments), str(self.text_pos)[:10])

