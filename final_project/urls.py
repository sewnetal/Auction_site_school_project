from django.conf.urls import *
from django.contrib import admin
from YAAS.views import *
from YAAS.API import *


admin.autodiscover()
urlpatterns = patterns('',
                        url(r'^home/$', home),
                        (r'^auction/(?P<pk>\d+)$',auction_viw),
                        (r'^myauctions/$', myauctions),
                        (r'^createuser/$', register),
                        (r'^search/$', search),
                        (r'^profile/$', profile),
                        (r'^saveprofile/(?P<pk>\d+)$', saveprofile),
                        (r'^login/$', login),
                        (r'^logout/$', logout),
                        (r'^createauction/$', create_auction),
                        (r'^editauction/(?P<pk>\d+)$', edit_auction),
                        (r'^ban/(?P<pk>\d+)$',ban),
                        (r'^saveauction/$', save_auction_conf),
                        (r'^placebid/(?P<pk>\d+)$', place_bid),
                        (r'^savenewbid/(?P<pk>\d+)$', savenewbid),
                        (r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                        (r'^admin/', include(admin.site.urls)),



                        (r'^api/v1/search/(\w+)$', search_api),
                        (r'^api/v1/search/$', search_api),
                        (r'^api/v1/browse/(?P<pk>\d+)$', browse_api),
                        (r'^api/v1/bid/(?P<pk>\d+)/(?P<price>\d+)$',bid_api),

)
