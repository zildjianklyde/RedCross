from django_cron import CronJobBase, Schedule
from django.utils import timezone
from .models import Donor
from django.core.mail import send_mail
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

class NotifyEligibleDonors(CronJobBase):
    RUN_AT_TIMES = ['00:00']  # Run daily at midnight
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'blood_donation.notify_eligible_donors'

    def do(self):
        try:
            #  (90 days ago)
            eligibility_date = timezone.now().date() - timedelta(days=90)
            
            # Find donors who donated more than 3 months ago or never donated
            eligible_donors = Donor.objects.filter(
                models.Q(last_donation_date__lte=eligibility_date) |
                models.Q(last_donation_date__isnull=True)
            )
            
            for donor in eligible_donors:
                self.send_notification(donor)
                logger.info(f"Sent notification to {donor.user.email}")
                
            return f"Sent {eligible_donors.count()} notifications"
            
        except Exception as e:
            logger.error(f"Error in cron job: {str(e)}")
            raise

    def send_notification(self, donor):
        subject = "Blood Donation Reminder"
        message = f"""Dear {donor.user.get_full_name() or donor.user.username},
        
Our records show you're eligible to donate blood again. 
Please visit our nearest donation center.

Thank you for saving lives!
- Red Cross Team"""
        
        send_mail(
            subject,
            message,
            None,  
            [donor.user.email],
            fail_silently=False,
        )