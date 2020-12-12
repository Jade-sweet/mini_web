import os

import celery
import pymysql
from celery.schedules import crontab

from test_app import settings

pymysql.install_as_MySQLdb()

# 加载环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_app.settings')

# 创建Celery对象，指定模块名、消息代理（消息队列）和持久化方式
app = celery.Celery('test_app',
                    broker='redis://:tang.618@120.27.10.104:6379/1',
                    # broker='amqp://tang:tang.618@120.27.10.104:5672/vhost1',
                    # 想要保存到数据库，需要安装django-celery-results,并在设置APP中加入django_celery_results
                    # backend='django-db')
                    backend='redis://:tang.618@120.27.10.104:6379/2')

# 直接通过代码修改Celery相关配置
app.conf.update(
    # 或者在setting中加内容
    # accept_content=['json', 'pickle', 'msgpack'],
    # task_seializer='pickle',
    # result_serializer='pickle',
    timezone=settings.TIME_ZONE,
    enable_utc=True,
    # 定时任务（计划任务）相当于是消息的生产者
    # 如果只有生产者没有消费者那么消息就会在消息队列中积压
    # 将来实际部署项目的时候生产者、消费者、消息队列可能都是不同节点
    # celery -A zufang beat -l debug ---> 消息的生产者
    # celery -A zufang worker -l debug ---> 消息的消费者

    beat_schedule={
        'task1': {
            'task': 'common.tasks.remove_expired_record',
            'schedule': crontab('*', '*', '*', '*', '*'),
            'args': ()
        },
    },
)
# 读取配置文件
app.config_from_object('django.conf:settings')
# 自动从所有注册的应用中发现异步任务/定时任务
app.autodiscover_tasks(('common', ))
# 另一种写法，自动从所有注册的应用中发现异步任务/定时任务
# app.autodiscover_tasks(('common', ))


