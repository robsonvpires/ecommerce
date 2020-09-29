from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from urllib.parse import urlparse
import os.path

from .models import *
from .forms import *

def index(request):
    return render(request, "auctions/index.html",{
        'listing_pages': Listing.objects.filter(active=True).order_by('-id')
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request):
    
    if request.method == 'POST':
        new_listing = ListingForm(request.POST, request.FILES)

        if new_listing.is_valid():
            j = new_listing.save(commit=False)
            j.user = request.user
            j.save()
            return render(request, "auctions/index.html",{
                'listing_pages': Listing.objects.filter(active=True).order_by('-id')
            })
        
    else:
        return render(request, "auctions/create_listing.html", {
            "form": ListingForm()
        })

@login_required
def view_listing(request, listing_id):
    
    page = {
        'listing' : Listing.objects.get(id=listing_id),
        'comments' : Comment.objects.all().filter(listing_id=listing_id),
        'in_watchlist' : Watchlist.objects.all().filter(listing__id=listing_id, user__id=request.user.id),
        'new_bid': BidForm(),
        'new_comment' : CommentForm(),
    }
    
    if request.method == 'POST':
        if request.POST.get('form_type') == 'post_comment':
            new_comment = CommentForm(request.POST)

            if new_comment.is_valid():
                j = new_comment.save(commit=False)
                j.user = request.user
                j.listing = Listing.objects.get(id=listing_id)
                j.save()
            
                return render(request, 'auctions/view_listing.html', page)

        elif request.POST.get('form_type') == 'post_bid':
            new_bid = BidForm(request.POST)
            if new_bid.is_valid():
                old_bid = new_bid.cleaned_data.get('value')

                try:
                    highest_bid = Listing.objects.get(id=listing_id).bids.last().value
                except: 
                    highest_bid = 0

                if highest_bid >= old_bid or old_bid <= Listing.objects.get(id=listing_id).price:
                    page['new_bid'] = new_bid
                    new_bid.add_error('value', 'bid is not high enough')
                    
                    return render(request, 'auctions/view_listing.html', page)

                mod_listing = Listing.objects.get(id=listing_id)
                add_bid = Bid(user=request.user, value=old_bid)
                add_bid.save()
                mod_listing.bids.add(add_bid)
        
                return render(request, 'auctions/view_listing.html', page)

    else:
        return render(request, 'auctions/view_listing.html', page)

@login_required
def finish_listing(request, listing_id):

    if Listing.objects.get(id=listing_id).user != request.user:
        return render(request, 'auctions/index.html')
    else:
        listing_to_finish = Listing.objects.get(id=listing_id)   
        listing_to_finish.active = False
        listing_to_finish.save()
        return render(request, 'auctions/view_listing.html', {
            'listing': listing_to_finish 
        })

@login_required
def in_watchlist(request, listing_id):
    
    on_watch = Watchlist.objects.all().filter(
        listing__id = listing_id, 
        user__id = request.user.id
    )

    if on_watch:
       on_watch.delete()
    else:
        new_watchlist = Watchlist(
            listing=Listing.objects.get(id=listing_id), 
            user=request.user
        )
        new_watchlist.save() 

    if os.path.split(urlparse(request.META['HTTP_REFERER']).path)[1] != 'watchlist':
        return redirect(request.META['HTTP_REFERER'])
    else:
        return render(request, 'auctions/my_watchlist.html')
        

@login_required
def my_watchlist(request):

    return render(request, 'auctions/my_watchlist.html', {
        'watchlist': Watchlist.objects.filter(user=request.user).order_by('-id')
    })

@login_required
def my_listings(request):
   
    return render(request, 'auctions/my_listings.html', {
        'my_listings': Listing.objects.filter(user=request.user).order_by('-id')
    })