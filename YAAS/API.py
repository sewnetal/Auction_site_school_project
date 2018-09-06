from django.http import HttpResponse,HttpResponseNotFound
from rest_framework import serializers
from rest_framework.parsers import JSONParser
import json
from rest_framework.decorators import api_view, renderer_classes, authentication_classes, permission_classes
from YAAS.models import Auction
from rest_framework.renderers import JSONRenderer
from YAAS.serializer import AuctionSerializer, BidSerializer
from datetime import datetime,timedelta
from django.utils.timezone import utc
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt

class JSONResponse(HttpResponse):

    def __init__(self,data,**kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

def search_api(request,search_input=''):
    if request.method == "GET":
        auction = Auction.objects.filter(title__icontains = search_input,status = 'Active').order_by('min_price')
        if search_input =='':
            auction = Auction.objects.filter(status= 'Active')
            serializer = AuctionSerializer(auction, many=True)
            return JSONResponse(serializer.data)

        else:
             serializer = AuctionSerializer(auction, many=True)
             return JSONResponse(serializer.data)
def browse_api(request,pk):
    auction = Auction.objects.get(id = pk)
    if request.method == "GET":

        if auction:
            auction = Auction.objects.filter(id = pk,status = 'Active')
            serializer = AuctionSerializer(auction,many= True)
            return JSONResponse(serializer.data)
        else:
             serializer = AuctionSerializer(auction, many=True)
             return JSONResponse(serializer.data)
@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def bid_api(request, pk,price):
        try:
            auction = Auction.objects.get(id = pk)
        except auction.DoesNotExist:
            return HttpResponseNotFound('<h1>Error 404\n</h1><h3>No auction found.</h3>', status=404)
        if request.method == "POST":
            data = JSONParser().parse(request)
            serializer = BidSerializer(data=price)
            if serializer.is_valid():
                auction = Auction.objects.get(id = pk)
                if auction.status != "Active":
                    response_data = {}
                    response_data['result'] = 'This Auction is not Active at the moment.'
                    response_data['message'] = 'Error 404'
                    return HttpResponse(json.dumps(response_data), content_type="application/json", status=404)
                if auction.seller == request.user:
                    response_data = {}
                    response_data['result'] = 'You are not allowed to bid on your own auction.'
                    response_data['message'] = 'Error 404'
                    return HttpResponse(json.dumps(response_data), content_type="application/json", status=404)
                if auction.min_price > price or price - auction.min_price < 0.01:
                    response_data = {}
                    response_data['result'] = 'Your bid must be higher than the current price at least by 0,01.'
                    response_data['message'] = 'Error 404'
                    return HttpResponse(json.dumps(response_data), content_type="application/json", status=404)
                if auction.current_bidder == request.user:
                    response_data = {}
                    response_data['result'] = 'You are Already the highest bidder of this auction.'
                    response_data['message'] = 'Error 404'
                    return HttpResponse(json.dumps(response_data), content_type="application/json", status=404)
                if auction.end_date - datetime.utcnow().replace(tzinfo=utc) > timedelta(hours=0):
                    auction.min_price = serializer
                    auction.save()
        else:
            response_data = {}
            response_data['result'] = 'No POST method'
            response_data['message'] = 'Error 404'
            auction = Auction.objects.get(id = pk)
            serializer = BidSerializer(auction)
            return Response(serializer.data,content_type="application/json")
class AuthView(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Auction.objects.get(pk=pk)
        except Auction.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        auction = self.get_object(pk)
        serializer = BidSerializer(auction)
        return Response(serializer.data)


