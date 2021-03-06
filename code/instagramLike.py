import time
from datetime import datetime
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Function to fetch links of posts
def get_all_links(driver,hashtag):
    links = []
    elements = driver.find_elements_by_tag_name('a')
    for elem in elements:
        href = elem.get_attribute("href")
        if "tagged="+hashtag in href:
            links.append(href)
    return links

# User information
user = "xxx"
pwd = "xxx"
hashtag = "largemouthbass"

# Start Chrome
driver = webdriver.Chrome('.\chromedriver.exe')

# Access Website
driver.get("http://www.instagram.com/accounts/login")
assert "Instagram" in driver.title

# Login to Website
time.sleep(5)
driver.find_element_by_xpath("//input[@name='username']").send_keys(user)
driver.find_element_by_xpath("//input[@name='password']").send_keys(pwd)
driver.find_element_by_xpath("//input[@name='password']").send_keys(Keys.RETURN)

# Clear Notification Screen
try:
    time.sleep(5)
    driver.find_element_by_xpath('.//div[@class="_hkmnt _g3lyc"][contains(., "Not Now")]').click()
except:
    print("No Notification Dialogue")

# Go to hashtag page and collect links
#driver.find_element_by_xpath('//input[@placeholder="Search"]').send_keys('#fishing')
time.sleep(2)
hashtagurl = "https://www.instagram.com/explore/tags/" + hashtag + "/"
driver.get(hashtagurl)
time.sleep(2)
try:
    links = get_all_links(driver,hashtag)
except:
    print("Error acquiring links")

# Open link, like post, log activity
data = {}
data['like'] = []

for link in links:
    try:
        driver.get(link)
        time.sleep(5)
        driver.find_element_by_xpath('.//span[@class="_8scx2 coreSpriteHeartOpen"][contains(., "Like")]').click()
        account = driver.find_element_by_xpath('.//a[@class="_2g7d5 notranslate _iadoq"]').text
        if driver.find_element_by_xpath('.//button[@class="_qv64e _iokts _4tgw8 _njrw0"]').text == 'Follow':
            follow = 'No'
        else:
            follow = 'Yes'
        jsonentry = {'datetime':str(datetime.now()),'account':account,'follow':follow,'link':link}
        print(jsonentry)
        data['like'].append(jsonentry)
    except:
        print("Problem with URL - Can't find element - Post already Liked")

try:
    with open('data.txt', 'a') as outfile:
        outfile.write("\r,")
        json.dump(data, outfile)
        outfile.close()
except:
    print("Not possible to write to json file")

driver.close()