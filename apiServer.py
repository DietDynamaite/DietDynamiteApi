from flask import Flask
from flask import request
from framework.crawler.kakaoMapImagesCrawler import *

app = Flask(__name__)

#TEST
# http://192.168.10.16:7000/api/crawling/kakaoImage?mapId=26307587
@app.route('/api/crawling/kakaoImage')
def kakoImageCrawler () :
    if (request.method == "GET"):
        mapId = request.args.get("mapId") #쿼리스트링
        # imageSrc = staticKakaoImageCrawling(mapId)
        imageSrc = dynamicKakaoImageCrawling(mapId)
        
        result = {
            "id" : mapId
        }
        
        if (imageSrc != -1):
            result["src"] = imageSrc        
        else:
            result["src"] = "없음"
        return result
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000)