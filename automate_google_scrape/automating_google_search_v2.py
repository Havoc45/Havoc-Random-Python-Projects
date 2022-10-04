##### NATIVE PYTHON 3.8.3 LIBRARIES
import sys
#import time
from datetime import datetime

##### EXTERNAL LIBRARIES
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from util import *

#when reading in system inputs, the arguments should follow this format
# any input starting with a dash - will be a new key pair value
# the value entered after - option will become the value of this key
# valid keys would be
# -k Keyword -d Dork -f output filename -o Operator

# expected input will be "-k espn.com -d inurl" 
#                        "-k espn.com -d inurl -o ^& -d intext -k arsenal" 
#                        "option" "single_whitespace" "value"

#create expected values
mydorks = {'-k':[],'-d':[],'-o':[]}

keylock = False
filenamelock = False

################################################### METHODS ###########################

def transform_dorks(mydic):
    #anatomy: dork:key operator dork:key
    search_string = ''
    
    #define the positional argument of the operators
    end = len(mydic['-o'])-1

    #define number of dork key pairs
    num = len(mydic['-k'])

    for index in range(num):
        #print(index,end)
        if index <= end:
            #users may want to use operators such as [] or "" that aren't : pair dorks
            if 'none' != mydic['-d'][index].lower():
                search_string = search_string + f" {mydic['-d'][index]}:{mydic['-k'][index]} {mydic['-o'][index]}"
            else:
                search_string = search_string + f" {mydic['-k'][index]} {mydic['-o'][index]}"
        else:
            if 'none' != mydic['-d'][index].lower():
                search_string = search_string + f" {mydic['-d'][index]}:{mydic['-k'][index]}"
            else:
                search_string = search_string + f" {mydic['-k'][index]}"
                
    return search_string[1:] #remove first white space

# this function will find nested href attributes in the div class r
def find_fullurl():
    search = browser.find_elements_by_xpath("//div[@class='yuRUbf']//*[@href]")
    #n = 1
    output = []
    for item in search:
        current = item.get_attribute('href')
        #identify which base urls have the word google in them and ignore them.
        trim = web_suffix_handler(current)
        if not 'google' in current[:trim]:
            output.append(current)
            # print(n, current)
            #n+=1
    return output

############################################# EXECUTION STARTS HERE ###################################

# when option is ingested, it will expect the value for that option next
for item in sys.argv[1:]:
    #print(item)
    if item.lower().replace(' ','') in mydorks.keys():
        keylock = True
        keyseek = item
        continue
    elif keylock:
        mydorks[keyseek].append(item)
        keylock = False
        keyseek = None
        continue
    elif item.lower() == '-f':
        filenamelock = True
        continue
    elif filenamelock:
        filename = item.replace('.csv','')
        continue

valid_statement(mydorks)

#reform the gathered arguments into a search_string
search_string = transform_dorks(mydorks)
print(search_string)

#####!!!!!!###!!!!!remember to redefine the chrome application path here
CHROME_PATH = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
CHROMEDRIVER_PATH = '/usr/bin/chromedriver'
WINDOW_SIZE = "1920,1080"

chrome_options = Options()  
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.binary_location = CHROME_PATH

# Assigning the browser variable with chromedriver of Chrome. 
# Any other browser and its respective webdriver will do like geckodriver for Mozilla Firefox can be used, 
# However may require different configuration to run in background. 
### uncomment the options argument to run in the background
browser = webdriver.Chrome('chromedriver', options = chrome_options) 

execute_g_search(browser, search_string)

try:
    f = open(f'{filename}.csv','w')
except:
    #use default name if no -f filename was given
    f = open(f'output.csv','w')
    
delimiter='^'
#write header first
f.write('no^title^url^description^date^time\n')
n = 0
n_fullurl = 0
page = 1

#while our browser can still see the hyperlink next (aka next page), run all this code
while True:
    #wait until the page has loaded the first google result tagged with the class_name 'g' 
    #then find the classes 'st' & 'r' on the page
    wait_until(browser)
    #description = browser.find_elements_by_xpath("//span[@class='st']")
    description = browser.find_elements_by_xpath("//div[@class='yuRUbf']//a//h3")
    #title_url = browser.find_elements_by_xpath("//div[@class='r']")
    title_url = browser.find_elements_by_xpath("//div[@class='VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf']")
    full_url = find_fullurl()

    print(f'we are on page {str(page)}')
    
    # writing and cleansing are done here
    #if the number of descriptioins and title_url pairs are equal to the full urls found, begin writing to file 'f'
    
    if len(description) == len(full_url) and len(title_url) == len(full_url):
        for index in range(len(description)):
            title_split = title_url[index].text.split('\n')
            current_datetime = str(datetime.now()).split(' ')

            try:
                #force index error to occur then remove reference dummy to title_split[1]
                if len(title_split) > 2:
                    dummy = title_split[1]
                    del dummy
                f.write(f'{str(n+1)}{delimiter}{title_split[0]}{delimiter}{full_url[index]}{delimiter}{description[index].text}{delimiter}{current_datetime[0]}{delimiter}{current_datetime[1]}\n')
                n += 1
            except:
                #title_split may be null which means description is null. Therefore skip writing this row and don't increase the index
                continue
    else:
    # if they are uneven, we control the index of fullurl and skip affected rows. i.e projectstream.google.com 
        for index in range(len(description)):
            title_split = title_url[index].text.split('\n')
            current_datetime = str(datetime.now()).split(' ')
            #print(title_split)
            try:
                #if the URL contains the special arrow symbol, find it and slice the string and remove whitespace else, do not slice the string
                trim = title_split[1].find('›')
                title_split[1] = title_split[1][:trim].replace(' ','')
                #title_split[1] is the base url and will always be a subset of full_url. a match means we move the n_fullurl index forward else we impute a null value and do not move n_fullurl
                if title_split[1] in full_url[n_fullurl]:
                    f.write(f'{str(n+1)}{delimiter}{title_split[0]}{delimiter}{full_url[n_fullurl]}{delimiter}{description[index].text}{delimiter}{current_datetime[0]}{delimiter}{current_datetime[1]}\n')
                    n_fullurl+=1
                else:                
                    f.write(f'{str(n+1)}{delimiter}{title_split[0]}{delimiter}{title_split[1]}{delimiter}{description[index].text}{delimiter}{current_datetime[0]}{delimiter}{current_datetime[1]}\n')
                n += 1
            except Exception as e:
                #title_split may be null which means description is null. Therefore skip writing this row and don't increase the index
                #although title_split is null, this is caused by google's 'did you know','top_stories' which do have href tags for the url, thus we skip these urls too.
                #print(e)
                n_fullurl+=1
                continue
                
    #after reading all results on page, move to the next page. If 'next' is not found, we exit
    try:
        link = browser.find_element_by_link_text("Next")
        link.click()
        page+=1
    except:
        print("we've reached the end of this google search!")
        break
    
    #break condition for testing: if you've written more than the n'th row, stop.
    #if n > 10:
    #    break

f.close()

#input('done...')

browser.close()
browser.quit()
