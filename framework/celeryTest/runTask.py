from framework.celeryTest.task import test2
from time import sleep

if __name__ == '__main__':
    asyncResult = test2.delay("imgscrcccccc")