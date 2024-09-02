from celery import Celery

# 실행할 task (Celery Task 가 정의된 파일) 목록 정의
task_list = list()
task_list.append('framework.celeryTest.task')
task_list.append('framework.crawler.kakaoMapImagesCrawler')

# Task 를 포함하는 Celery 생성
celery_app = Celery(include=task_list)

# Celery Config 추가
celery_app.config_from_object('celery_config.role.default_role')