
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django.conf import settings



if settings.SCHEDULER:
    scheduler = BackgroundScheduler()


def start():
    if settings.scheduler:
        try:
            scheduler.add_jobstore(MemoryJobStore())
            scheduler.start()

            __checkout_test_requests()
        except KeyboardInterrupt:
            scheduler.shutdown()


@scheduler.scheduled_job(trigger=IntervalTrigger(seconds=5), timezone=settings.TIME_ZONE, id='checkout_test_requests_id', max_instances=1)
def __checkout_test_requests():
    pass

    # User.objects.all().delete()







