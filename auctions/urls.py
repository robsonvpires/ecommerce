from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('new_listing', views.create_listing, name='create_listing'),
    path('<int:listing_id>', views.view_listing, name='view_listing'),
    path('<int:listing_id>/finish', views.finish_listing, name='finish_listing'),
    path('<int:listing_id>/in_watchlist', views.in_watchlist, name='in_watchlist'),
    path('watchlist', views.my_watchlist, name='my_watchlist'),
    path('listings', views.my_listings, name='my_listings'),
]
