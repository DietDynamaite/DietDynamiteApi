from celery import Celery
from time import sleep
import logging
logger = logging.getLogger(__name__)

app = Celery('tasks', 
            broker='amqp://diet:diet@localhost:5672//',
            backend='redis://localhost:6379/0') #get 을 사용하기 위해 필요
            # (결과 저장하지 않으므로 backend 없이 get 사용불가)

@app.task
def test2(text):
    sleep(3)
    print("hello", text)
    # reqeuest module import 시 에러가 발생하는에 (TLS 오류) 이유를 찾아야한다.
    logger.info("heeeeeeeelllllllooo")

    return "hello", text

