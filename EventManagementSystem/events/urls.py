from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import EventViewSet, RSVPViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')

urlpatterns = [
    # registered event routes: /events/ (list, create), /events/{pk}/ (retrieve, update, destroy)
    path('', include(router.urls)),

    # RSVP routes (nested under event)
    # POST   /events/{event_pk}/rsvp/           -> RSVPViewSet.create
    # PATCH  /events/{event_pk}/rsvp/{pk}/      -> RSVPViewSet.partial_update
    path('events/<uuid:event_pk>/rsvp/', RSVPViewSet.as_view({'post': 'create'}), name='event-rsvp-create'),
    path('events/<uuid:event_pk>/rsvp/<uuid:pk>/', RSVPViewSet.as_view({'patch': 'partial_update'}), name='event-rsvp-update'),

    # Review routes (nested under event)
    # GET    /events/{event_pk}/reviews/        -> ReviewViewSet.list
    # POST   /events/{event_pk}/reviews/        -> ReviewViewSet.create
    # GET    /events/{event_pk}/reviews/{pk}/   -> ReviewViewSet.retrieve
    # PUT/PATCH/DELETE for individual reviews
    path('events/<uuid:event_pk>/reviews/', ReviewViewSet.as_view({'get': 'list', 'post': 'create'}), name='event-reviews'),
    path('events/<uuid:event_pk>/reviews/<uuid:pk>/', ReviewViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='event-review-detail'),
]
