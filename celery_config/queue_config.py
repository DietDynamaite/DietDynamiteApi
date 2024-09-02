from kombu import Exchange, Queue

# RabbitMQ에서 생성할 큐 정의
CELERY_QUEUES = (
    Queue("image_crawling_q", Exchange('image_crawling_q', type="direct"), routing_key="default"),
    Queue("celery_testing_q", Exchange('celery_testing_q', type="direct"), routing_key="default")
)