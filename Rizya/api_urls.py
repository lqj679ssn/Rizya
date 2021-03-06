from django.urls import path, include

urlpatterns = [
    path('base/', include('Base.urls')),
    path('3-party/', include('Base.urls_3party')),
    path('user/', include('User.urls')),
    path('space/', include('Space.urls')),
    path('album/', include('Album.urls')),
    path('event/', include('Event.urls')),
    path('milestone/', include('Milestone.urls')),
    path('image/', include('Image.urls')),
]
