from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from multiprocessing import Pool
import time, selenium

def processor(bounds):
    id_min, id_max = bounds
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
    
    # end login sequence
    
    # get link information
    link_template = "https://mobile.facebook.com/story.php?story_fbid=%s&id=1384103428575043"
    
    found_hrefs = []
    for s_idx in range(id_min, id_max):
        try:
            driver.get("https://talkyou.in/pages/KaDaejeon/posts/%d/" % s_idx)
        
            elem = driver.find_element_by_class_name("text-right")
            elem = elem.find_element_by_css_selector("a")
            facebook_link = elem.get_attribute("href")
            
            story_fbid = facebook_link.split("_")[-1]
            final_link = link_template % story_fbid
            found_hrefs.append(final_link)
        except selenium.common.exceptions.NoSuchElementException:
            continue
    
    return found_hrefs

if __name__ == '__main__':
    num_parallel = 3
    true_max = 23800
    p = Pool(num_parallel)
    all_links = []
    ranges = [((1 + i*(true_max/num_parallel)), (1 + (i+1)*(true_max/num_parallel)))
               for i in range(num_parallel)]
    for link_list in p.map(processor, ranges):
        all_links += link_list
    
    with open("mobilefb_links.txt", "w") as f:
        for link in all_links:
            f.write(link)
            f.write("\n")
