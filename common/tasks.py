from datetime import timedelta

from django.utils import timezone
from pymysql import DatabaseError

from common.models import SpiderHistory
from test_app import app


@app.task
def remove_expired_record():
    print(1111111111111111111)
    check_time = timezone.now() - timedelta(days=7)
    try:
        SpiderHistory.objects.filter(recorddate__lte=check_time).delete()
        return True
    except DatabaseError:
        return False