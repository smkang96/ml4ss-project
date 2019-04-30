
import time
import _pickle as pickle
import datetime
import argparse
from multiprocessing import Pool
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from Components import Comment, Post

def parse_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', type=str, help="file to with links")
	parser.add_argument('--test', action="store_true")

	return parser.parse_args()

def parse_number(string):
	numbers = [int(s) for s in string.split() if s.isdigit()]
	return numbers[0] if len(numbers) == 1 else False

def parse_date(string):
	today = datetime.date.today()
	string_date, string_time = [x.strip() for x in string.split(" at ")]

	if string_date == "Yesterday":
		date = today - datetime.timedelta(days=1)
	elif len(string_date.split()) == 2:
		date = datetime.datetime.strptime(string_date, "%B %d").replace(year=today.year).date()
	else:
		date = datetime.datetime.strptime(string_date, "%B %d, %Y").date()

	time = datetime.datetime.strptime(string_time, "%I:%M %p").time()
	date_and_time = datetime.datetime.combine(date, time)

	return date_and_time

def get_reactions(driver, href):
	driver.get(href)
	reactions = driver.find_element_by_class_name("scrollAreaColumn").find_elements_by_class_name("_10tn")

	total, like, haha, love, sad, wow, angry = 0, 0, 0, 0, 0, 0, 0

	for reaction in reactions:
		number = parse_number(reaction.text)
		assert number is not False, "Invalid reaction number"

		data_store = reaction.get_attribute("data-store")

		if data_store == '{"reactionType":"all"}':
			total = number
		elif data_store == '{"reactionType":1}':
			like = number
		elif data_store == '{"reactionType":2}':
			love = number
		elif data_store == '{"reactionType":3}':
			wow = number
		elif data_store == '{"reactionType":4}':
			haha = number
		elif data_store == '{"reactionType":7}':
			sad = number
		elif data_store == '{"reactionType":8}':
			angry = number
	# 	else:
	# 		raise AssertionError("Unknown reaction type")

	# if total > 0 and (like + haha + love + sad + wow + angry != total):
	# 	raise AssertionError("Incorrect total")

	return like, haha, love, sad, wow, angry

def get_post(driver, href):
	driver.get(href)

	text = driver.find_element_by_class_name("_5rgt").text
	date = parse_date(driver.find_element_by_class_name("_52jc").find_element(By.TAG_NAME, "abbr").text)

	href_reactions = driver.find_element_by_class_name("_5ton").find_element(By.TAG_NAME, "a").get_attribute("href")
	reactions = get_reactions(driver, href_reactions)

	return Post(href, date, text, *reactions)

def get_comments(driver, post):
	driver.get(post.href)

	try:
		comments = driver.find_element_by_class_name("_333v").find_elements_by_xpath("./div[contains(@class, '_2a_i')")
	except NoSuchElementException:
		return post

	tuples = []
	for comment in comments:
		text_comment = comment.find_element_by_class_name("_2b06").find_elements(By.TAG_NAME, "div")[1].text

		container = comment.find_element_by_class_name("_2a_m").find_elements_by_class_name("_2b1h")
		if len(container) == 0:
			href_replies = False
		else:
			href_replies = container[0].find_element(By.TAG_NAME, "a").get_attribute("href")

		text_reactions = comment.find_element_by_class_name("_14va").text
		if not text_reactions:
			href_reactions = False
		else:
			href_reactions = comment.find_element_by_class_name("_14v8").get_attribute("href")

		tuples.append((text_comment, href_replies, href_reactions))

	for t in tuples:
		if t[2]:
			reactions = get_reactions(driver, t[2])
		else:
			reactions = 0, 0, 0, 0, 0, 0

		comment = Comment(t[0], *reactions)

		if t[1]:
			get_replies(driver, comment, t[1])

		post.add_comment(comment)

	return post

def get_replies(driver, comment, href):
	driver.get(href)

	tuples = []
	replies = driver.find_element_by_class_name("_3u3w").find_elements_by_class_name("_2a_i")

	for reply in replies:
		text_reply = reply.find_element_by_class_name("_2b06").find_elements(By.TAG_NAME, "div")[1].text

		text_reactions = reply.find_element_by_class_name("_14va").text
		if not text_reactions:
			href_reactions = False
		else:
			href_reactions = reply.find_element_by_class_name("_14v8").get_attribute("href")

		tuples.append((text_reply, href_reactions))

	for t in tuples:
		if t[1]:
			reactions = get_reactions(driver, t[1])
		else:
			reactions = 0, 0, 0, 0, 0, 0

		reply = Comment(t[0], *reactions, parent=comment)
		comment.add_reply(reply)

	return comment

def parse(ranges):
	start, end = ranges

	driver = webdriver.Chrome()
	driver.get("https://mobile.facebook.com/")
	id_input = driver.find_element_by_id("m_login_email")
	pw_input = driver.find_element_by_id("m_login_password")

	id_input.send_keys(my_id)
	pw_input.send_keys(my_pw)
	pw_input.send_keys(Keys.RETURN)
	time.sleep(4)

	posts = []
	completed, total = 0, end-start

	for line in tqdm(links[start:end], total=total):
		href_post = line.strip()
		try:
			try:
				post = get_post(driver, href_post)
			except NoSuchElementException as e:
				print("{} {}".format(href_post, "photo"))
				continue

			get_comments(driver, post)
		except Exception as e:
			print("{} {}".format(href_post, str(e)))
			continue

		posts.append(post)
		completed += 1

	pickle.dump(posts, open("data/{}-{}.pkl".format(start, end), "wb+"))

	return completed

if __name__ == '__main__':
	START = time.time()

	args = parse_arguments()

	if not args.test and not args.f:
		raise AssertionError("Invalid CLI")

	if args.test:
		# Test code
		driver = webdriver.Chrome()
		driver.get("https://mobile.facebook.com/")
		id_input = driver.find_element_by_id("m_login_email")
		pw_input = driver.find_element_by_id("m_login_password")

		id_input.send_keys(my_id)
		pw_input.send_keys(my_pw)
		pw_input.send_keys(Keys.RETURN)
		time.sleep(3)

		href = "https://mobile.facebook.com/story.php?story_fbid=2276312152687495&id=1384103428575043"

		post = get_post(driver, href)
		get_comments(driver, post)

		# print(post)
		# for comment in post.comments:
		# 	print("  {}".format(str(comment)))
		# 	for reply in comment.replies:
		# 		print("    {}".format(str(reply)))

		sys.exit(0)

	with open("credentials.txt", "r") as cred_file:
		my_id = cred_file.readline().strip()
		my_pw = cred_file.readline().strip()

	links = []
	with open(args.f, "r") as file:
		for line in file:
			links.append(line.strip())

	total, cores = len(links), 4

	pool = Pool(cores)
	ranges = [(i * total//cores, (i+1) * total//cores) for i in range(cores)]

	completed = 0
	for c in pool.map(parse, ranges):
		completed += c

	END = time.time()

	print("Completed {}/{} ({}%) in {} seconds." \
		.format(completed, total, completed/total*100, END-START))


	

