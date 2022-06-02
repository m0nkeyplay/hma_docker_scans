#!/usr/bin/env python3

#   selenium and webdriver for Chrome is required to take the screenshots
#   https://pypi.org/project/selenium/
#   https://github.com/mozilla/geckodriver/releases

import os
import datetime
import time
import random
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import re
import json
import sqlite3
import logging
import argparse
try:
    from seleniumwire import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.options import DesiredCapabilities 
    from selenium.common import exceptions
except:
    print("""selenium and webdriver for Chrome is required to take the screenshots
            https://pypi.org/project/selenium/
            https://sites.google.com/a/chromium.org/chromedriver/downloads""")
    exit()
try:
    from bs4 import BeautifulSoup
except:
    print("""Beautiful Soup is required to check links out on the pages.
            pip3 install bs4""")
    exit()

#logging.basicConfig(level=logging.DEBUG)

#   We know this is bad, but we are using proxies to test and need to be able to see as the 
#   proxy sees it - and since we are providing no data except to see the site, this is an acceptable risk
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


ap = argparse.ArgumentParser()
ap.add_argument("-u", "--url", required=True, help="Need a URL to check")
args = vars(ap.parse_args())

theURL = args["url"]

cwd = os.getcwd()
uaString = "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 MonkeyTesting"

#   dictionary of things to look for
dictOfInfo = {
    'wordpress': 'Detected: Wordpress;',
    'drupal': 'Detected: Drupal',
    'zen-cart': 'Detected: Zen Cart',
    'joomla': 'Detected: Joomla',
    'woocommerce': 'Detected: WooCommerce',
    'bigcommerce': 'Detected: BigCommerce',
    'shopify': 'Detected: Shopify',
    'magento': 'Detected: Magento',
    'wix': 'Detected: Wix',
    'bitrix24': 'Detected: Bitrix24',
    'prestashop': 'Detected: Prestashop',
    'zend': 'Detected: zend',
    'symfony': 'Detected: Symphony',
    'aws.amazon.com': 'Detected:  Possibkle AWS usage - check links',
    'cloud.google.com': 'Detected: Possible GCP usage - check links',
    'azure.microsoft.com' : 'Detected: Possible Azure usage - check links',
    'googleads' : 'Google Tracking',
    'adservice.google' : 'Google Tracking',
    'googletagservices' : 'Google Tracking',
    'static.xx.fbcdn.net' : 'Facebook Tracking',
    'beacon.js' : 'Sneaking Tracking',
    'npm.react-facebook-pixel.' : 'Facebook Tracking Pixel Courtesy of NPM Javascript Library',
    'analytics.js' : 'Most possibly Google Anlytics',
    'track.min.js' : 'Adrizer Tracking most possibly',
    'outbrain.js' : 'Those catchy click bait outbrain trackers are here',
    'geolocation.onetrust.com' : 'Location Tracking (attempt at least)',
    'atrk.js' : 'Alexa Metrics',
    'fbevents.js' : 'Facebook Tracking'

}

#   Some text so we can keep it out of functions and clean it up when needed
scriptName = """
                _     
__      __ ___ | |__  
\ \ /\ / // _ \| '_ \ 
 \ V  V /|  __/| |_) |
  \_/\_/ _\___||_.__/ 
 ___ (_)| |_  ___     
/ __|| || __|/ _ \    
\__ \| || |_|  __/    
|___/|_| \_______|    
(_) _ __   / _|  ___  
| || '_ \ | |_  / _ \ 
| || | | ||  _|| (_) |
|_||_| |_||_|   \___/ 
v 2 -- now using Docker!
@https://github.com/m0nkeyplay
########################################

"""

def is_url(url):
    returnMe = ""
    if url[:4] != "http":
        returnMe = "http://"+url.strip()
    else:
        returnMe = url.strip()
    return returnMe
        

def check_my_ip():
    ipData = []
    try:
        checkIp = requests.get('http://ip-api.com/json/',timeout=60,verify=False)
        data = checkIp.json()
        ip = data["query"]
        myCountry = data["country"]
        countryCode = data["countryCode"]
        regionName = data["regionName"]
        city = data["city"]
        print("We are currently running from %s - %s,%s (%s)"%(str(ip),str(regionName),str(city),str(myCountry)))
    except:
        print("We couldn't connect to the IP checker. Probably not going to connect to the site.")
        exit()
    ipData = [ip,myCountry,countryCode]
    return ipData

#   Send a clean error message from requests if we get one
def search_error(errorMessage):
    searchFor = "(\[Errno\s\d+\])(.*)'"
    match = re.search(searchFor,errorMessage)
    if match:
        return match.group(2).replace(',','-')
    else:
        return ''

#   Grab the title of the web page
def search_title(webPage):
    searchFor = "<title>(.*)</title>"
    match = re.search(searchFor,webPage)
    if match:
        return match.group(1)[0:30].strip() 
    else:
        return ''

#   Grab the codes it took to get to the final page
def search_history(theText):  
    for code in theText:
        httpCode = re.search('\d{3}',str(code))
    return httpCode[0]

#   uniform text from a URL for file names etc
def name_clean(someText):
    cleaned = someText.replace('http://','').replace('https://','').replace('.','-').replace('/','').strip()
    return cleaned

#   Get links on the page
#   Write it to a file
def get_links(pageText):
    writeMe = ''
    soup = BeautifulSoup(pageText, 'html.parser')
    monkey_link_list_items = soup.find_all('a')
    for monkey in monkey_link_list_items:
        href = monkey.get('href')
        if href and href != "None":
            if href[0] != '#':
                writeMe += str(href+'\n')
    return writeMe

#   check on some common server techs
def server_stuff(field,searchFor,say):
    serverTech = ""
    if field.find(str(searchFor)) > 0:
        serverTech += say.strip(';')+"\n"
        return serverTech      
    else:
        return ''

#   Use Custom Headers for the screenshot
def interceptor(request):
    del request.headers['User-Agent']
    request.headers['User-Agent'] = uaString

# Take a screenshot
def take_screenshot(url,finalUrl):
    taken = str(int(time.time()))
    options = Options()
    options.headless = True
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    capabilities = DesiredCapabilities.CHROME.copy()
    capabilities['acceptInsecureCerts'] = True
    fileName = name_clean(url)+taken
    fileName = fileName+'.png'
    saveFile = 'screenshots/'+fileName
    

    with webdriver.Chrome(options=options,desired_capabilities=capabilities) as driver:
        try:
            driver.request_interceptor = interceptor
            driver.get(finalUrl)
            driver.save_screenshot(saveFile)
            toReturn = fileName
            driver.quit()
        except:
            toReturn = 'Unable to get screenshot'
            print(toReturn)
            driver.quit()
        if driver:
            driver.quit()
    return toReturn

#   This is the part where we check the site
def get_it(url):
    timeStamp = str(datetime.datetime.now()).split('.')[0]        
    serverFind = []
    try:
        print("Checking %s..."%url)
        r = requests.get(url,stream=True,allow_redirects=True,timeout=60,headers=headers,verify=False)
        finalURL = str(r.url)
        print("  Landed on %s"%finalURL)
        status = str(r.status_code)
        print("  Status: %s"%status)
        hops = ''
        if r.history:
            hops = str(search_history(r.history))
        try:
            rServer = str(r.headers["Server"]).replace(',',' ')
            print("  Server Type: %s"%rServer)
        except:
            rServer = ''
        try:
            rPoweredBy = str(r.headers["X-Powered-By"]).replace(',',' ')
            serverFind.append('X-Powered By: '+rPoweredBy+';')
            print("  X-Powered By: %s"%rPoweredBy)
        except:
            rServer = ''
        try:
            titleText = search_title(r.text.lower()).replace(',', ' ')
            print("  Page Title: %s"%titleText)
        except:
            titleText = ''
        try:
            linkInfo = get_links(r.text)
            print("  Links on page.")
            print(linkInfo)
        except:
            linkInfo = ''
        print("Working on getting a screenshot here.")
        try:
            
            pic = take_screenshot(url,finalURL)
            if pic != 'Unable to get screenshot':
                print("  Screenshot captured.\nSaved in: screenshots/%s"%pic)
            else:
                print("  Unable to capture screenshot.")
        except:
            pic = ''
        for k,v in dictOfInfo.items():
            moreInfo = server_stuff(r.text,k,v)
            if moreInfo:
                serverFind.append(moreInfo)
        if len(serverFind) >= 1:
            print("Misc Server Info:")
            for x in serverFind:
                print(x+"\n")

    except requests.exceptions.RequestException as err:
        print("  Did not connect: %s" %search_error(str(err)))

if __name__ == '__main__':
    print(scriptName)
    iAm = check_my_ip()
    myIp = str(iAm[0])
    headers = {}
    headers['User-Agent'] = uaString
    get_it(is_url(theURL))
    print("\n*************************")
    print("Done.  Thanks.")
