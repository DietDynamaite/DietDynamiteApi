from celery_config.entry_point import celery_app
from time import sleep
import logging
import requests



@celery_app.task(name="framework.celeryTest.task", queue='celery_testing_q', routing_key='default')
def test2(placeImg):
    BASE_URL = "http://localhost/rest/map"
    placeId = "aa"
    url = f"{BASE_URL}/test?placeId={placeId}&placeImg={placeImg}"
    
    requests.get(url)
    print(url)
    
    return url