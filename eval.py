
def talkyou_to_facebook(v1):
    from time import sleep
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.common.exceptions import NoSuchElementException

    all_links = [post.href for post in v1]

    driver = webdriver.Chrome()
    
    # login sequence
    cred_file = open("credentials.txt", "r")
    my_id = cred_file.readline().strip()
    my_pw = cred_file.readline().strip()
    
    driver.get("https://talkyou.in/")
    id_input = driver.find_element_by_name("username")
    pw_input = driver.find_element_by_name("password")
    
    id_input.send_keys(my_id)
    pw_input.send_keys(my_pw)
    pw_input.send_keys(Keys.RETURN)
    sleep(5)
    
    # get link information
    link_template = "https://mobile.facebook.com/story.php?story_fbid=%s&id=1384103428575043"
    
    with open('data/eval_talkyou.txt') as f, open('data/eval_facebook.txt', 'w+') as g:
        for line in f:
            if line[0] == '#':
                g.write(line)
                continue

            try:
                link = line.split("**")[0].strip()
                driver.get(link)
            
                elem = driver.find_element_by_class_name("text-right")
                elem = elem.find_element_by_css_selector("a")
                facebook_link = elem.get_attribute("href")
                
                story_fbid = facebook_link.split("_")[-1]
                final_link = link_template % story_fbid

                if final_link in all_links:
                    g.write(final_link + "\n")
                else:
                    print("Not in all_links:", final_link)

            except NoSuchElementException:
                print("NoSuchElementException:", line.strip())
                continue

def format_eval_sets(v1):
    import _pickle as pickle
    from collections import defaultdict

    def get_facebook_sets():
        eval_sets = defaultdict(set)
        with open('data/eval_facebook.txt') as f:
            current_key = None
            for line in f:
                if line[0] == '#':
                    current_key = line.strip()[2:]
                    continue
                eval_sets[current_key].add(line.strip())

        return eval_sets

    facebook_sets = get_facebook_sets()

    index_sets = defaultdict(set) # dict of ('title': set of indices)
    for post_index, post in enumerate(v1):
        for key, facebook_set in facebook_sets.items():
            if post.href in facebook_set:
                index_sets[key].add(post_index)

    pickle.dump(index_sets, open("data/eval_sets", "wb+"))
    print("- Saved {} evaluation sets".format(len(index_sets)))

def load_eval_sets():
    import _pickle as pickle
    index_sets = pickle.load(open("data/eval_sets", "rb"))
    print("- Loaded {} evaluation sets".format(len(index_sets)))
    return index_sets
        
def evaluate(posts, ref_set):
    num_RnS = sum([x in ref_set for x in posts])
    precision = num_RnS / len(posts)
    recall = num_RnS / len(ref_set)
    f1 = 2 * precision * recall / (precision + recall)
    # recall = num_RnS / len(list(ref_set))
    return precision, recall, f1

### Obsolete ###

def get_all_talkyou_links(v1):
    def extract_talkyou_link(post):
        lines_of_post = post.text.split('\n')
        talkyou_lines = list(filter(lambda x: 'talkyou.in/pages/' in x, lines_of_post))
        if len(talkyou_lines) != 1:
            return lines_of_post[-2] # some misses but not too many
        else:
            return list(talkyou_lines)[0]

    all_talkyou_links = set()
    for p1 in v1:
        talkyou_link = extract_talkyou_link(p1)
        all_talkyou_links.add(talkyou_link)
    return all_talkyou_links
