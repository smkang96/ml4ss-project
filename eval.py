import numpy as np
import _pickle as pickle

def get_all_talkyou_links():
    '''needed to filter out non-gathered posts'''
    def talkyoulink_extractor(post):
        lines_of_post = post.text.split('\n')
        talkyou_lines = list(filter(lambda x: 'talkyou.in/pages/' in x, lines_of_post))
        if len(talkyou_lines) != 1:
            return lines_of_post[-2] # some misses but not too many
        else:
            return list(talkyou_lines)[0]
    v1, v2 = [], []
    for i in range(6):
        d1 = pickle.load(open("data/v1-{}".format(i), "rb"))
        d2 = pickle.load(open("data/v2-{}".format(i), "rb"))
        v1.append(d1)
        v2.append(d2)
    
    post_counter = 0
    full_list = []
    for i in range(6):
        for j, p in enumerate(v1[i]):
            full_list.append((post_counter, p, v2[i][j]))
            post_counter += 1

    all_talkyou_links = set()
    for p_idx, p1, _ in full_list:
        talkyou_link = talkyoulink_extractor(p1)
        all_talkyou_links.add(talkyou_link)
    return all_talkyou_links

ALL_TALKYOU_LINKS = get_all_talkyou_links()

def get_eval_set(filename):
    '''assumes file has only links listed with nothing else'''
    eval_set = set()
    with open('./eval_links.txt') as f:
        for line in f:
            eval_set.add(line.strip())
    return eval_set
        
def precision(selected_set, ref_set):
    filtered_ref_set = set(filter(lambda x: x in  ALL_TALKYOU_LINKS, ref_set))
    rel_and_sel = [x in filtered_ref_set for x in selected_set]
    num_RnS = np.sum(rel_and_sel)
    return num_RnS / len(selected_set)

def recall(selected_set, ref_set):
    filtered_ref_set = set(filter(lambda x: x in  ALL_TALKYOU_LINKS, ref_set))
    rel_and_sel = [x in filtered_ref_set for x in selected_set]
    num_RnS = np.sum(rel_and_sel)
    return num_RnS / len(list(filtered_ref_set))