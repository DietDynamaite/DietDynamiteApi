from celery_config import queue_config

# Message Broker
BROKER_URL = 'amqp://diet:diet@localhost:5672//'

# Backend
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# Serializer
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']

# Timezone
CELERY_TIMEZONE = 'Asia/Seoul'
CELERY_ENABLE_UTC = True

# Exchange, Queue, Routing
CELERY_QUEUES = queue_config.CELERY_QUEUES

CELERY_DEFAULT_QUEUE = 'celery_testing_q'
CELERY_DEFAULT_EXCHANGE = 'celery_testing_q'
CELERY_DEFAULT_ROUTING_KEY = 'default'
CELERY_TASK_RESULT_EXPIRES = 3600
CELERYD_TASK_TIME_LIMIT = 600

CELERY_CHORD_PROPAGATES = True

CELERY_RESULT_EXCHANGE = 'celery_testing_q'
CELERY_RESULT_EXCHANGE_TYPE = 'direct'
CELERY_RESULT_PERSISTENT = False
CELERYD_PREFETCH_MULTIPLIER = 1

# concurrency
CELERYD_CONCURRENCY = 4
