from bs4 import BeautifulSoup
import urllib.request

from urllib.request import urlopen
import os
from urllib.error import HTTPError
# from googletrans import Translator
from selenium import webdriver
import traceback
import ssl



def get_list():
    f = open("data.txt", "r")
    str = f.read()
    return list(str.split('\n'))


def make_dir():
    try:
        if not(os.path.isdir("img")):
            os.makedirs(os.path.join("img"))
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def get_image():
    make_dir()
    li = get_list()

    cnt = li.count('')
    for i in range(cnt):
        li.remove('')
    empty_list = []
    url = "https://en.wikipedia.org/wiki/"  # 이미지 src와 조합하여 다운받을 주소

    for src in li:
        url = "https://en.wikipedia.org/wiki/" + src
        try:
            html = urllib.request.urlopen(url)
        except HTTPError as e:
            empty_list.append(src)
            continue

        source = html.read()

        soup = BeautifulSoup(source, "html.parser")
        # title = soup.find(title)

        # if '(disambiguation)' in str(title):
        #     print ("dis 포함")
        #     link = soup.find(p)
        #     link2 = link.find(a)
        #     a.ttrs['href']
            
        imgclass = soup.find_all(class_='image')

        img = imgclass[0].find('img')

        if 'Question_book' in str(img) or 'Wiki_letter' in str(img):
            print("책임!")
            img = imgclass[1].find('img')
        elif 'Disambig_gray' in str(img):
            empty_list.append(src)
            continue

        t = urlopen("https:"+img.attrs['src']).read()
        filename = "img/"+src+'.jpg'
        with open(filename, "wb") as f:
            f.write(t)
            f.close()
    return empty_list


def get_image_kr(empty_list):
    base_url = 'https://www.google.com/search'
    hdr = {'User-Agent': 'Mozilla/5.0'}
    for e in empty_list:
        values = {'q': e, 'oq': e, 'aqs': 'chrome..69i57.35694j0j7', 'sourceid': 'chrome', 'ie': 'UTF-8', }

        query_string = urllib.parse.urlencode(values) 
        req = urllib.request.Request(base_url + '?' + query_string, headers=hdr) 
        context = ssl._create_unverified_context() 
        print(req._full_url)
        try:
            res = urllib.request.urlopen(req, context=context) 
        except:
            traceback.print_exc()
        soup = BeautifulSoup(res.read(), 'html.parser')
        title_class = soup.find('div', div_="kp_header")
        res = soup.find_all("span")
        print(res)
        #print(res.get_text())
        

        # driver = webdriver.Chrome('./chromedriver')
        # driver.set_window_size(800, 600)
        # driver.implicitly_wait(5)
        # driver.get('https://google.co.kr')

        # elem = driver.find_element_by_id('lst-ib')
        # elem.send_keys(e)
        # elem.submit()
        # html = driver.page_source
        # print(html)


empty_list = get_image()
get_image_kr(empty_list)
# translator = Translator()
# for e in empty_list:
#     print(translator.translate(e, src='en', dest='ko'))

# print(empty_list)
# if len(empty_list) > 0:
#     f = open("empty.txt", "w")
#     f.write('\n'.join(empty_list))
#     f.close()
# else:
#     if os.path.isfile("empty.txt"):
#         os.remove("empty.txt")