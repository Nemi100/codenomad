from django_cron import CronJobBase, Schedule
from .models import Subscription
from datetime import datetime
from django.core.mail import send_mail

class CheckSubscriptionsCronJob(CronJobBase):
    RUN_EVERY_MINS = 1440  # run every 24 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'subscribe.check_subscriptions_cron_job'  # a unique code

    def do(self):
        subscriptions = Subscription.objects.filter(is_trial=True, trial_ended=False, end_date__lte=datetime.now().date())
        for subscription in subscriptions:
            # Process payment logic here
            subscription.trial_ended = True
            subscription.save()
            send_mail(
                'Subscription Charge',
                'Your trial period has ended, and your subscription has been charged.',
                'noreply@codenomad.com',
                [subscription.email] if subscription.email else [subscription.user.email],
                fail_silently=False,
            )
