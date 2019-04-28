from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, codecs

driver = webdriver.Chrome()

# login sequence
cred_file = open("credentials.txt", "r")
my_id = cred_file.readline().strip()
my_pw = cred_file.readline().strip()

driver.get("https://mobile.facebook.com/")
time.sleep(2)
id_input = driver.find_element_by_id("m_login_email")
pw_input = driver.find_element_by_id("m_login_password")

id_input.send_keys(my_id)
pw_input.send_keys(my_pw)
pw_input.send_keys(Keys.RETURN)

time.sleep(3)
driver.get("https://mobile.facebook.com/KaDaejeon/")

f = codecs.open("ok2.txt", "w", "utf-8")

found_hrefs = set()
for s_idx in range(1000):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

stuff = driver.find_elements_by_class_name("_15kq")
for e_idx, elem in enumerate(stuff):
    e_href = elem.get_attribute("href")
    
    if e_href in found_hrefs:
        continue
    else:
        f.write(("[%d]" % e_idx) + e_href)
        f.write("\r\n")
        found_hrefs.add(e_href)

f.close()