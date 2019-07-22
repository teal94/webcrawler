from bs4 import BeautifulSoup
import urllib.request

from urllib.request import urlopen
import os
from urllib.error import HTTPError
from googletrans import Translator
from selenium import webdriver
import traceback
import ssl
from selenium.webdriver.support.ui import WebDriverWait
import time


not_found_list = []
def get_list():
    f = open("data2.txt", "r")
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

    for src in li:
        url = ("https://en.wikipedia.org/wiki/" + src.lower())
        try:
            html = urllib.request.urlopen(url)
        except HTTPError as e:
            empty_list.append(src)
            continue

        source = html.read()

        soup = BeautifulSoup(source, "html.parser")
            
        imgclass = soup.find_all(class_='image')

        img = imgclass[0].find('img')

        if 'Question_book' in str(img) or 'Wiki_letter' in str(img):
            print("책임!")
            img = imgclass[1].find('img')
        elif 'Disambig_gray' in str(img) or 'DAB_list_gray' in str(img):
            empty_list.append(src)
            continue

        t = urlopen("https:"+img.attrs['src']).read()
        filename = "img/"+src+'.jpg'
        with open(filename, "wb") as f:
            f.write(t)
            f.close()
    return empty_list


def get_image_kr(empty_list):
    
    save_list = []
    print(empty_list)
    for (name, e) in empty_list:
        print (name, e)
        if e.count(' ') > 0:
            e = e.replace(' ', '_')
        url = ("https://ko.wikipedia.org/wiki/" + urllib.parse.quote_plus(e))
        print(url)
        try:
            html = urllib.request.urlopen(url)
        except HTTPError as error:
            if e.count('_') > 0:
                e = e.replace('_', '')
                url = ("https://ko.wikipedia.org/wiki/" + urllib.parse.quote_plus(e))
                try:
                    html = urllib.request.urlopen(url)
                except HTTPError as error:
                    save_list.append([name, e])
                    print("http에러", name)
                    continue
                
            save_list.append([name, e])
            print("http에러" + name)
            continue

        source = html.read()

        soup = BeautifulSoup(source, "html.parser")
            
        imgclass = soup.find_all(class_='image')

        img = imgclass[0].find('img')

        if 'Question_book' in str(img) or 'Wiki_letter' in str(img):
            img = imgclass[1].find('img')
        elif 'Disambig' in str(img) or 'DBA_list_gray' in str(img):
            if len(imgclass) > 1:
                img = imgclass[1].find('img')
            else:
                save_list.append([name, e])
                print("Disambig_gray" + name)
                continue

        t = urlopen("https:"+img.attrs['src']).read()
        filename = "img/"+name+'.jpg'
        with open(filename, "wb") as f:
            f.write(t)
            f.close()

    return save_list

def convert_en_to_ko(empty_list):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    driver = webdriver.Chrome('./chromedriver', chrome_options=options)
    driver.set_window_size(100, 100)
    driver.implicitly_wait(1)
    save_list = []
    # 오류 하나 해결해야함 화살표
    for e in empty_list:
        driver.get('https://google.co.kr')
        elem = driver.find_element_by_name('q')
        elem.send_keys(e)
        elem.submit()
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        
        imgclass = soup.find_all(class_='kno-ecr-pt kno-fb-ctx PZPZlf gsmt')
        if len(imgclass) > 0:
            img = imgclass[0].find('span')
        else:
            not_found_list.append([e, ""])
            continue
        save_list.append([e, img.get_text()])

    print("not_found :", not_found_list)
    driver.quit()
    return save_list

# def tanslate_en_to_ko(empty_list):
#     translator = Translator()
#     save_list = []
#     for e in empty_list:

#         translator.translate(e, src='en', dest='ko')
#         print(e)
#         save_list.append(e)
#     return save_list

def tanslate_en_to_ko(empty_list):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    driver = webdriver.Chrome('./chromedriver', chrome_options=options)
    driver.set_window_size(800, 800)
    driver.implicitly_wait(1)
    save_list = []
    empty_list += not_found_list
    not_found_list.clear()
    # 오류 하나 해결해야함 화살표
    print(empty_list)
    for e in empty_list:
        driver.get('https://translate.google.co.kr/?hl=ko')
        elem = driver.find_element_by_id('source')
        elem.send_keys(e[0])
        time.sleep(3)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        imgclass = soup.find_all(class_='tlid-translation translation')

        print(imgclass)
        if len(imgclass[0].find('span')) > 0:
            img = imgclass[0].find('span')
            save_list.append([e[0], img.get_text()])
        else:
            not_found_list.append(e)
            continue
        
    print("not_found2 :", not_found_list)
    driver.quit()
    print("save_list :", save_list)
    return save_list


empty_list = get_image()
print("첫번째 시작")
empty_list = get_image_kr(convert_en_to_ko(empty_list))
print("첫번째 끝남")
save_list = get_image_kr(tanslate_en_to_ko(empty_list))

if len(save_list) > 0:
    print("save_list : ", save_list)
    f = open("empty.txt", "w")
    sum_list = list(map(lambda x: x[0], save_list))

    f.write('\n'.join(sum_list)) #오류
    f.write('\n')
    if len(not_found_list) > 0:
        f.write('\n'.join(not_found_list))
    f.close()
else:
    if os.path.isfile("empty.txt"):
        os.remove("empty.txt")
