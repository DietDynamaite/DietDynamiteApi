from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOption
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time

BASE_URL = "https://place.map.kakao.com/m"

def staticKakaoImageCrawling(mapId):
    request_header = {
        'User-Agent' : ('Mozilla/5.0 (Windows NT 10.0;Win64; x64)\
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98\
        Safari/537.36')
    }
    
    url = f"{BASE_URL}/{mapId}"
    
    res = requests.get(url, headers=request_header)
    
    if (res.status_code == 200):
        soup = BeautifulSoup(res.text, "html.parser")
        
        print(soup)
        
        imageEl = soup.select_one('a[data-viewid="basicInfoTopImage"]')
        imageSrc = imageEl.get("style")

        return imageSrc
    else :
        return -1

def dynamicKakaoImageCrawling(mapId):
    url = f"{BASE_URL}/{mapId}"
        
    # 크롬 드라이버 생성
    chrome_options = ChromeOption()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    
    # 페이지 접속
    driver.get(url)
    time.sleep(0.5)
    
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    
    imageEl = soup.select_one('a[data-viewid="basicInfoTopImage"]')
    
    if (imageEl != None):
        imageStyle = imageEl.get("style")
        
        start = imageStyle.index('url("//') + len('url("//')
        end = imageStyle.index('");', start)
        
        url = imageStyle[start:end]
        
        return url
    
    return "이미지가 없습니다"