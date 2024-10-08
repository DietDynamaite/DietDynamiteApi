from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOption
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from celery_config.entry_point import celery_app
import json
import requests
import time

IMAGE_BASE_URL = "https://place.map.kakao.com/m"
SPRING_API_URL = "http://localhost/rest/map"

### 정적 이미지 크롤링
# 페이지 생성후 이미지가 비동기 출력되어 나오지않음
def staticKakaoImageCrawling(mapId):
    request_header = {
        'User-Agent' : ('Mozilla/5.0 (Windows NT 10.0;Win64; x64)\
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98\
        Safari/537.36')
    }
    
    url = f"{IMAGE_BASE_URL}/{mapId}"
    
    res = requests.get(url, headers=request_header)
    
    if (res.status_code == 200):
        soup = BeautifulSoup(res.text, "html.parser")
        
        print(soup)
        
        imageEl = soup.select_one('a[data-viewid="basicInfoTopImage"]')
        imageSrc = imageEl.get("style")

        return imageSrc
    else :
        return -1

### 동적 이미지 크롤링 (일회성 클라이언트에게 이미지 크롤링 용도)
def dynamicKakaoImageCrawlingOnce(mapId):
    url = f"{IMAGE_BASE_URL}/{mapId}"
        
    # 크롬 드라이버 생성
    chrome_options = ChromeOption()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    
    # 페이지 접속
    driver.get(url)
    time.sleep(0.5)
    
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    
    # 이미지 요소 가져오기
    imageEl = soup.select_one('a[data-viewid="basicInfoTopImage"]')
    
    if (imageEl != None):
        #이미지 요소에서 style 속성 가져와 분해
        imageStyle = imageEl.get("style")
        start = imageStyle.index('url("//') + len('url("//')
        end = imageStyle.index('");', start)
        
        placeImg = imageStyle[start:end]
        
        return placeImg
    
    # 이미지 없으면 0 반환
    return "0"

### 동적 이미지 크롤링 (DB 저장 용도)
@celery_app.task(name="framework.crawler.kakaoMapImagesCrawler", queue='image_crawling_q', routing_key='default')
def dynamicKakaoImageCrawling(mapId, mapName):
    url = f"{IMAGE_BASE_URL}/{mapId}"
    
    # 페이지 로드 전략 None
    caps = DesiredCapabilities.CHROME
    caps["pageLoadStrategy"] = "none"
            
    # 크롬 드라이버 생성
    chrome_options = ChromeOption()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--headless') 
    chrome_options.add_argument('--ignore-ssl-errors=yes')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--disable-images')
    chrome_options.add_experimental_option("prefs", {'profile.managed_default_content_settings.images': 2})
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')

    # Add Image Loading inactive Flag to reduce loading time
    chrome_options.add_argument('--disable-images')
    chrome_options.add_experimental_option(
        "prefs", {'profile.managed_default_content_settings.images': 2})
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200'
    chrome_options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    
    # 페이지 접속
    driver.get(url)
    time.sleep(0.5)
    
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    
    imageEl = soup.select_one('a[data-viewid="basicInfoTopImage"]')
    
    if (imageEl != None):
        #이미지 요소에서 style 속성 가져와 분해
        imageStyle = imageEl.get("style")
        start = imageStyle.index('url("//') + len('url("//')
        end = imageStyle.index('");', start)
        
        imageSrc = imageStyle[start:end]
        
        # 이미지데이터 있을경우 placeImg 에 ImageSrc 를 가지고 Spring 에 요청 전송
        requestData = {
            "placeAPIid" : mapId,
            "placeImg" : imageSrc,
            "placeName" : mapName
        }
        requestUrl = f"{SPRING_API_URL}/places/updateImage"
        headers = {'Content-Type':'application/json; charset=utf-8'}
        requests.post(url=requestUrl, data=json.dumps(requestData), headers=headers)
        return
    
    # 이미지데이터 없을경우 placeImg 에 "0" 입력후 Spring 에 요청 전송
    else :
        requestData = {
            "placeAPIid" : mapId,
            "placeImg" : 0,
            "placeName" : mapName
        }
        requestUrl = f"{SPRING_API_URL}/places/updateImage"
        headers = {'Content-Type':'application/json; charset=utf-8'}
        requests.post(url=requestUrl, data=json.dumps(requestData), headers=headers)