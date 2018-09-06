from django.test import TestCase
from django.contrib.auth.models import User
from datetime import datetime
from YAAS.models import Auction


class YAASTests(TestCase):

    def createauctiontest(self):

        User.objects.create_user(username='test',password='12345',last_name='lastname',first_name='firstname',email = 'sewnetal@yahoo.com')

        self.client.login(username='test',password='12345')
        response =self.client.get('/createauction/',follow = True)
        self.assertEqual(response.status_code,200)

        print "Before creating an auction test:",Auction.objects.count()
        response = self.client.post('/saveauction/',{'option':'Yes','a_title':'newtitle','a_description':'didcribe','a_price':'100','a_category':'mobile','a_enddate':'2014-11-03 12:00',})
        self.assertTemplateUsed(response,'done.html')
        print "After creating an auction:",Auction.objects.count()

    def bid_test(self):
        auction_bidder =User.objects.create_user(username='test',password='12345',last_name='lastname',first_name='firstname',email = 'sewnetal@yahoo.com')
        auction_seller =User.objects.create_user(username='sewnet',password='12345',last_name='lastname',first_name='firstname',email = 'sewnetal@yahoo.com')
        auction_bidder.save()
        auction_seller.save()
        print "Number of users After creating seller and bidder in a test:",User.objects.count()

        self.client.login(username='test',password='12345')
        print "Before creating an auction:",Auction.objects.count()

        auction = Auction.objects.create(id= 5,seller = 'sewnet',end_date = '2014-11-10 12:00',min_price = 10.0,category = 'mobile', description = 'adskjadh', status = 'Active' )
        auction.save()

        print "After creating an auction:",Auction.objects.count()
        response =self.client.post('/savenewbid/5',{'option':'Yes','new_bid': 20})
        self.assertTemplateUsed(response,'home.html')





