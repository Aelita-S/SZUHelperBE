import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from spider.tasks import DocumentTask
from user.tasks import SubscribeMsgSendTask

scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)

logger = logging.getLogger(__name__)


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            DocumentTask.run,
            trigger=IntervalTrigger(hours=1),  # 每隔一小时爬取一次
            id="document_task",
            max_instances=1,
            coalesce=False,
            replace_existing=True,
        )

        logger.info("Added job 'DocumentTask'.")

        scheduler.add_job(
            SubscribeMsgSendTask.run,
            trigger=CronTrigger(hour=18),  # 每天本地下午六点执行
            id="subscribe power",
            max_instances=1,
            coalesce=False,
            replace_existing=True,
        )

        logger.info("Added job 'SubscribeMsgSendTask'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )

        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
