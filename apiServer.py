from flask import Flask, request
from framework.crawler.kakaoMapImagesCrawler import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app)   #CORS 오류 처리

# TEST URL 정보 (동적 크롤링 일회성 클라이언트 반환용)
# http://192.168.10.16:7000/api/crawling/kakoImageOnce?mapId=26307587
@app.route('/api/crawling/kakaoImageOnce')
def kakoImageCrawlerOnce () :
    if (request.method == "GET"):
        mapId = request.args.get("mapId") #쿼리스트링
        imageSrc = dynamicKakaoImageCrawlingOnce(mapId)
        
        result = {
            "id" : mapId
        }
        
        if (imageSrc != -1):
            result["src"] = imageSrc        
        else:
            result["src"] = "없음"
        return result

# TEST URL 정보 (병렬처리 동적 크롤링 DB 저장용)
# http://localhost:7000/api/crawling/kakaoImage?mapId=26307587&mapName=aaaaa
@app.route('/api/crawling/kakaoImage')
def kakoImageCrawler () :
    if (request.method == "GET"):
        mapId = request.args.get("mapId") #쿼리스트링
        mapName = request.args.get("mapName") #쿼리스트링
        dynamicKakaoImageCrawling.delay(mapId, mapName)
    
    result = {
        "response" : "전달완료"
    }
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000)