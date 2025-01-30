from django_cron import CronJobBase, Schedule
from .models import Donor
from django.core.mail import send_mail

class NotifyEligibleDonors(CronJobBase):
    RUN_EVERY_MINS = 4320  # Every 3 months

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'blood_donation.notify_eligible_donors'

    def do(self):
        donors = Donor.objects.filter(is_eligible=True)
        for donor in donors:
            send_mail(
                'You are eligible to donate blood!',
                'Dear {}, you are eligible to donate blood again. Please visit our center.'.format(donor.user.get_full_name()),
                'no-reply@redcross.com',
                [donor.user.email],
                fail_silently=False,
            )