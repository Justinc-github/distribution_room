import logging
import random
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
import socket
from pyModbusTCP.client import ModbusClient
from django.shortcuts import render
from Statistics.models import value
import datetime

logger = logging.getLogger(__name__)


def my_job(request=None):  # 修改任务名称位置
    url = "749839wx55.goho.co"
    ip_address = socket.gethostbyname(url)
    ModbusBMS = ModbusClient(host=ip_address, port=42352, unit_id=1, auto_open=True, auto_close=False)
    data = ModbusBMS.read_holding_registers(0, 2)
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    print(data[0]/10)
    print(data[1]/10)
    data1 = data[1]/10.0
    data2 = data[0]/10.0
    data = value(tem=data1, humidity=data2, time=formatted_time)
    data_change = [data1, data2]
    data.save()
    print(data_change)
    return render(request, 'statistics.html', {
        'data_change': data_change,
    })


def delete_old_job_executions(max_age=3600):
    """
  此作业从数据库中删除早于“max_age”的APScheduler作业执行条目。
  它有助于防止数据库中塞满不再有用的旧历史记录。
  最长7天
  """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,  # 修改任务名称位置
            trigger=CronTrigger(second="*/5"),  # 时间
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")  # 修改任务名称位置

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                hour="00", minute="00"
            ),  # 每天的零点执行清理任务
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
