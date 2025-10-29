from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions, serializers, status, pagination, filters
from rest_framework.response import Response

from .models import Event, RSVP, Review  # models live in useraccount.models
from .serializers import EventSerializer, RSVPSerializer, ReviewSerializer
from .permissions import IsOrganizerOrReadOnly, IsAuthenticatedForCreate


# Pagination
class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100





# ViewSets
class EventViewSet(viewsets.ModelViewSet):
    """
    list: returns public events (paginated). If authenticated, also returns events where user is organizer or invited.
    create: authenticated users only (organizer set to request.user).
    retrieve: returns event detail if visible.
    update/destroy: only organizer allowed.
    """
    serializer_class = EventSerializer
    #permission_classes = []
    permission_classes = [permissions.IsAuthenticated, IsOrganizerOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'location', 'organizer__name']
    ordering_fields = ['start_time', 'created_at']

    def get_queryset(self):
        user = self.request.user
        if user and user.is_authenticated:
            return Event.objects.filter(
                Q(is_public=True) |
                Q(organizer=user) 
                
            ).distinct()
        return Event.objects.filter(is_public=True)

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)


class RSVPViewSet(viewsets.GenericViewSet):
    """
    Create and update RSVP for an event.
    Routes expected:
      POST /events/{event_pk}/rsvp/
      PATCH /events/{event_pk}/rsvp/{pk}/
    """
    serializer_class = RSVPSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = RSVP.objects.all()

    def create(self, request, event_pk=None):
        if event_pk is None:
            return Response({'detail': 'event_pk is required in URL.'}, status=status.HTTP_400_BAD_REQUEST)
        event = get_object_or_404(Event, pk=event_pk)
        if not event.is_user_allowed(request.user):
            return Response({'detail': 'Not allowed to RSVP for this event.'}, status=status.HTTP_403_FORBIDDEN)

        # ensure single RSVP per user/event
        rsvp, created = RSVP.objects.get_or_create(event=event, user=request.user,
                                                   defaults={'status': request.data.get('status', RSVP.STATUS_GOING)})
        if not created:
            # update status if provided
            status_val = request.data.get('status')
            if status_val:
                rsvp.status = status_val
                rsvp.save()
        serializer = RSVPSerializer(rsvp)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    def partial_update(self, request, pk=None, event_pk=None):
        if event_pk is None:
            return Response({'detail': 'event_pk is required in URL.'}, status=status.HTTP_400_BAD_REQUEST)
        rsvp = get_object_or_404(RSVP, pk=pk, event__pk=event_pk)
        if rsvp.user != request.user:
            return Response({'detail': 'You may only update your own RSVP.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = RSVPSerializer(rsvp, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    List and create reviews for an event.
    Routes expected:
      GET /events/{event_pk}/reviews/
      POST /events/{event_pk}/reviews/
    """
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        event_pk = self.kwargs.get('event_pk')
        if not event_pk:
            return Review.objects.none()
        # only reviews for given event
        return Review.objects.filter(event__pk=event_pk)

    def perform_create(self, serializer):
        event_pk = self.kwargs.get('event_pk')
        event = get_object_or_404(Event, pk=event_pk)
        user = self.request.user
        if not event.is_user_allowed(user):
            raise permissions.PermissionDenied('You are not allowed to review this event.')
        serializer.save(event=event, user=user)
