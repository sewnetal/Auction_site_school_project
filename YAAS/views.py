from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from datetime import datetime,timedelta
from YAAS.static import statues_dict
from django.contrib.auth.models import User
from YAAS.models import Auction
from django.utils import translation
from forms import Auction_form, Confirm_auction,Registration_form,Placebid,Edit_description
from django.utils.timezone import utc
from django.core.mail import send_mail



def home(request):
    auctions = Auction.objects.all().order_by('starting_date')
    return render_to_response('home.html',{'auctions':auctions},context_instance = RequestContext(request))

def auction_viw(request,pk):
    auction = Auction.objects.get(id = pk)
    return render_to_response('auction.html',{'auction': auction},context_instance = RequestContext(request))

@login_required(login_url='/login/?next=%s')
def myauctions(request):
    auctions = Auction.objects.all().order_by('starting_date')
    return render_to_response('myauctions.html',{'auctions': auctions,'user':request.user},context_instance = RequestContext(request))

def search(request):
    if request.POST:
        input_search = request.POST.get('search')
        result = Auction.objects.filter(title__icontains = input_search).order_by('min_price')
        if result:
            mesg = "search result for "
            return render_to_response('home.html',{'search': input_search,'mesg':mesg,'auctions':result},
                                      context_instance = RequestContext(request))
        else:
            input_search = request.POST.get('search')
            result = Auction.objects.filter(title__icontains = input_search).order_by('min_price')
            mesg = "NO result for "
            return render_to_response('home.html',{'search': input_search,'mesg':mesg,'auctions':result},
                                      context_instance = RequestContext(request))
    else:
        auctions = Auction.objects.all().order_by('min_price')
        return render_to_response('home.html',{'auctions':auctions},context_instance = RequestContext(request))

def register(request):
    if request.method == 'POST':
        form = Registration_form(request.POST)
        if form.is_valid():
            cd= form.cleaned_data
            username1 = cd['username']
            firstname = cd['firstname']
            lastname = cd['lastname']
            email = cd['email']
            password = request.POST.get('password1')
            new_user = User.objects.create_user(username = username1,last_name=lastname,first_name=firstname,email = email,password = password)
            new_user.save()
            mesg = 'your registration has been successful please login'
            return render_to_response("login.html",{'mesg':mesg},context_instance = RequestContext(request))

        else:
            form = Registration_form()
            return render_to_response("registration.html",{'form': form},context_instance = RequestContext(request))
    else:
        form = Registration_form()
        return render_to_response("registration.html",{'form': form},context_instance = RequestContext(request))

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        redirect = request.GET.get('next','/home/')
        user = auth.authenticate(username = username,password = password)
        if user is not None and user.is_active:
            auth.login(request,user)
            return HttpResponseRedirect(redirect)
        else:
            error_message = "please login"
            return render_to_response('login.html',{'error': error_message},context_instance = RequestContext(request))
    else:
        return render_to_response('login.html',{},context_instance = RequestContext(request))

def logout(request):
    if request.user.is_authenticated():
        auth.logout(request)
        redirect = request.GET.get('next','/home/')
        return HttpResponseRedirect(redirect)
    else:
        return render_to_response('home.html',{'auctions':Auction.objects.all()},context_instance = RequestContext(request))

def profile(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s'%request.path)
    else:
        return render_to_response('profile.html',
                                  {'user':request.user,'firstname': request.user.first_name,'lastname':request.user.last_name,'email': request.user.email,
                                   'password':request.user.password},context_instance = RequestContext(request))
@login_required(login_url='/login/?next=%s')
def saveprofile(request,pk):
    if request.POST:
        fn = request.POST.get('firstname','')
        ln = request.POST.get('lastname','')
        email = request.POST.get('email','')
        password = request.POST.get('password','')
        password2 = request.POST.get('password2','')
        if password and password2 == password:
            usr = User.objects.get(id = pk)
            usr.first_name = fn
            usr.last_name = ln
            usr.email = email
            usr.set_password(password)
            usr.save()
            mesg = "Your profile has been edited successfully"
            return render_to_response('home.html',{'mesg':mesg,'auctions':Auction.objects.all()},context_instance = RequestContext(request))
        else:
            mesg = "passwords doesn't mach!"
            return render_to_response('editprofile.html',{'mesg':mesg,'user': request.user}, context_instance = RequestContext(request))
    else:
        auctions = Auction.objects.all().order_by('starting_date')
        return render_to_response('editprofile.html',{'user':request.user,'auctions':auctions},context_instance = RequestContext(request))

@login_required(login_url='/login/?next=%s')
def create_auction(request):
    if request.POST:
        form = Auction_form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            auction_title = cd ['title']
            auction_description = request.POST.get('description','')
            auction_price = cd['min_price']
            auction_category = cd['category']
            auction_enddate = cd['end_date'].strftime("%Y-%m-%d %H:%M")
            form = Confirm_auction()

            return render_to_response('confirmation.html',{'form': form,'a_title':auction_title,
                                                           'a_description': auction_description,'a_price':auction_price,
                                                           'a_category':auction_category,'a_enddate':auction_enddate},
                                                            context_instance = RequestContext(request))
        else:
            form = Auction_form()
            error_message = "Invalid input"

            return render_to_response('create_auction.html',{'form':form,'error':error_message},context_instance = RequestContext(request))
    else:
        form = Auction_form()
        return render_to_response('create_auction.html',{'form':form},context_instance = RequestContext(request))


@login_required(login_url='/login/?next=%s')
def save_auction_conf(request):
    option  = request.POST.get('option',' ')
    if option == 'Yes':
        auction_title = request.POST.get('a_title','')
        auction_description = request.POST.get('a_description','')
        auction_price = request.POST.get('a_price')
        auction_category = request.POST.get('a_category', '')
        auction_enddate = request.POST.get('a_enddate', '')
        input_time = datetime.strptime(auction_enddate,'%Y-%m-%d %H:%M')
        check_input_time = input_time - datetime.now()
        if check_input_time <= timedelta(hours=72) and check_input_time > timedelta(hours=0):
            auction = Auction(seller = request.user.username ,title=auction_title,description = auction_description,min_price =auction_price,
                              starting_date = datetime.now(),category = auction_category,end_date = auction_enddate,
                              status = statues_dict['active'])
            auction.save()
            mesg = "Your auction has been created successfully"
            send_mail('Auction Created',mesg,'sewnetal@yahoo.com',[request.user.email], fail_silently=False)

            return render_to_response('done.html',{'mesg':mesg},context_instance=RequestContext(request))
        else:
            error_message = "End data of the auction must be less than 72 hours"
            form = Auction_form()
            return render_to_response('create_auction.html',{'error': error_message,'form':form},context_instance = RequestContext(request))
    else:
        error_message = "Auction is not saved"
        form = Auction_form()
        return render_to_response('create_auction.html',{'error': error_message,'form':form},context_instance = RequestContext(request))

@login_required(login_url='/login/?next=%s')
def edit_auction(request,pk):
    if request.POST:
        queryset = Auction.objects.get(id = pk)
        form =Edit_description(request.POST,instance = queryset)
        if form.is_valid():
            form.save()
            mesg = "Auction edit successful"
            auction = Auction.objects.get(id = pk)
            return render_to_response('auction.html',{'mesg':mesg,'auction':auction,'user':request.user},context_instance = RequestContext(request))
        else:
            mesg = "Invalid input"
            queryset = Auction.objects.get(id = pk)
            form = Edit_description(instance = queryset)
            return render_to_response('editauction.html',{'form':form,'error':mesg},context_instance = RequestContext(request))
    else:
        queryset = Auction.objects.get(id = pk)
        form = Edit_description(instance = queryset)
        return render_to_response('editauction.html',{'form':form},context_instance = RequestContext(request))
@login_required(login_url='/login/?next=%s')
def ban(request,pk):
    if request.POST:
        user = request.user
        if user.is_superuser:
            auction = Auction.objects.get(id = pk)
            option  = request.POST.get('option',' ')
            if option == "Yes":
                auction.status = statues_dict['banned']
                auction.save()
                mesg = "The Auction is banne"
                return render_to_response('done.html',{'mesg':mesg},context_instance=RequestContext(request))
            else:
                auction = Auction.objects.get(id = pk)
                return render_to_response('auction.html',{'auction':auction,'user':user},context_instance = RequestContext(request))
        else:
            mesg = "You dont have permision to ban an auction"
            auction = Auction.objects.get(id = pk)
            return render_to_response('auction.html',{'auction':auction,'user':user,'mesg':mesg},context_instance = RequestContext(request))
    else:
        auction = Auction.objects.get(id = pk)
        form = Confirm_auction()
        return render_to_response('ban.html',{'auction':auction,'form':form},context_instance = RequestContext(request))
def place_bid(request,pk):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s'%request.path)
    else:
        if request.POST:
            form = Placebid(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                auction_price = cd['min_price']
                form = Confirm_auction()

                return render_to_response('confirmnewbid.html',{'form':form,'new_bid':auction_price,'auction':Auction.objects.get(id =pk)},
                                          context_instance = RequestContext(request))
            else:
                form = Placebid()
                error_message = "Invalid input"

                return render_to_response('placebid.html',{'form':form,'error':error_message,'auction':Auction.objects.get(id =pk)},
                                          context_instance = RequestContext(request))

        else:
            form =Placebid()
            return render_to_response('placebid.html',{'form':form,'auction':Auction.objects.get(id =pk)},
                                      context_instance = RequestContext(request))

def savenewbid(request,pk):
    option  = request.POST.get('option',)
    if option == 'Yes':
        auction = Auction.objects.get(id = pk)
        if auction.end_date - datetime.utcnow().replace(tzinfo=utc) > timedelta(hours=0) and auction.status != statues_dict['banned']:
            auction = Auction.objects.get(id = pk)
            older_price = auction.min_price
            new_bid = request.POST.get('new_bid')
            if float(new_bid) > older_price and float(new_bid) - older_price > 0.01:
                auction = Auction.objects.get(id = pk)
                auction.min_price=float(new_bid)
                user = request.user.username
                if auction.current_bidder == user:
                    mesg = "Error! You are currently the highst bidder of this auction!"
                    return render_to_response('done.html',{'mesg':mesg},context_instance=RequestContext(request))
                elif auction.seller == user:
                    mesg = "Error! You are not allowed to bid on your own auction!"
                    return render_to_response('done.html',{'mesg':mesg},context_instance=RequestContext(request))
                else:
                    auction_owner = User.objects.get(username= auction.seller)
                    auction_owner_email = auction_owner.email
                    auction.current_bidder = user
                    auction.save()
                    mesg = "You have placed your bid successfully,you are currently the highest bidder this item"
                    emailmesg = "You have placed your bid successfully,you are currently the highest bidder this item"
                    emailmesg2 = "You have new bidder for your item"
                    send_mail('Bid confirmation',emailmesg,'sewnetal97@gmail.com',[request.user.email], fail_silently=False)
                    send_mail('new Bidder confirmation',emailmesg2,'sewnetal97@gmail.com',[auction_owner_email], fail_silently=False)
                    if auction.end_date - datetime.utcnow().replace(tzinfo=utc) < timedelta(minutes=5):
                        auction.end_date = auction.end_date + timedelta(minutes=5)
                        mesg = "You have placed your bid successfully,you are currently the highest bidder this item and the auction due is increased by 5 min"
                        auction.save()
                    if auction.current_bidder:
                        auction_highest_bidder = User.objects.get(username= auction.current_bidder)
                        auction_highest_bidder_email = auction_highest_bidder.email
                        emailmesg3 = "You are no more the highest bidder of auction title"
                        send_mail('Bid confirmation',emailmesg3,'sewnetal97@gmail.com',[auction_highest_bidder_email], fail_silently=False)
                    return render_to_response('home.html',{'mesg':mesg,'auctions': Auction.objects.all()},
                                          context_instance=RequestContext(request))

            else:
                error_message = "You must bid more that the current bid"
                form = Placebid()
                return render_to_response('placebid.html',{'error': error_message,'form':form,'auction':Auction.objects.get(id =pk)},
                                          context_instance = RequestContext(request))
        else:
            error_message = "This auction is not active at the moment"
            auction = Auction.objects.get(id = pk)
            auction.status = statues_dict['ended']
            auction.auction_winner = auction.current_bidder
            auction.save()
            return render_to_response('done.html',{'mesg': error_message},context_instance = RequestContext(request))

    else:
        mesg = "bid is not saved"
        return render_to_response('placebid.html',{'mesg': mesg,'auctions':Auction.objects.all()},
                                  context_instance = RequestContext)



