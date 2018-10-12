# Web-application-for-auction
1. List of implemented requirements </br>
UC1 Create a user account
UC2 Edit user account information
UC3 Create a new auction 
UC4 Edit an existing auction
UC5 Browse and search auctions 
UC6 Bid
UC7 Ban an auction
UC8 Resolve an auction
WS1 Webservice get request to browse auctions or show specific auction
Python 2.7 and Django 1.7 versions  
admin username "admin" and password "yaas2014"
session management 
UC8 Resolving bids must be initiated automatically
concurrency problems
The REST API 
url(r'^api/v1/search/$', search_api), 
url(r'^api/v1/search/(\w+)$', search_api), 
