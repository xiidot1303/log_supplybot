from django.db.models.signals import post_save
from django.dispatch import receiver
from app.models import Statement
from asgiref.sync import async_to_sync
from bot.services.notification_service import new_statement_info_to_managers_notify_job
from bot.control.updater import application

@receiver(post_save, sender=Statement)
def statement_created(sender, instance, created, **kwargs):
    if True:
        instance: Statement
        # send notification to all managers about new statement is created
        application.job_queue.run_once(
            new_statement_info_to_managers_notify_job, 0, instance
        )