from celery.task import periodic_task
from YAAS.models import Auction
from django.utils.timezone import utc
from django.core.mail import send_mail
from YAAS.static import statues,statues_dict
from django.contrib.auth.models import User
from datetime import datetime,timedelta
import django

django.setup()

@periodic_task(run_every=timedelta(minutes=1))
def task1():
    auctions = Auction.objects.all()
    for auction in auctions:
        if auction.end_date - datetime.utcnow().replace(tzinfo=utc) <= timedelta(hours=0):
            if auction.status == "Active":
                auction.status = statues_dict['ended']
                if auction.current_bidder:
                    auction.auction_winner = auction.current_bidder
                    auction.save()
                    auction_winner = User.objects.get(username = auction.current_bidder)
                    auction_winner_email = auction_winner.email
                    mesg = "you have won this auction"
                    print "you have won this auction"
                    send_mail('You have won an auction',mesg,'sewnetal97@gmail.com',[auction_winner_email], fail_silently=False)
                else:
                    auction.save()
