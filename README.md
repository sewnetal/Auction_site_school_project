# Web-application-for-auction
1. List of implemented requirements </br>
UC1 Create a user account</br>
UC2 Edit user account information</br>
UC3 Create a new auction </br>
UC4 Edit an existing auction</br>
UC5 Browse and search auctions </br>
UC6 Bid</br>
UC7 Ban an auction</br>
UC8 Resolve an auction</br>
WS1 Webservice get request to browse auctions or show specific auction</br>
Python 2.7 and Django 1.7 versions  </br>
admin username "admin" and password "yaas2014"</br>
session management </br>
UC8 Resolving bids must be initiated automatically</br>
concurrency problems</br>
The REST API 
url(r'^api/v1/search/$', search_api), </br>
url(r'^api/v1/search/(\w+)$', search_api), 
