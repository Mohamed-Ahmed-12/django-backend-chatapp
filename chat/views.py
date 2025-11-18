from rest_framework import viewsets
from .models import Room , TextMessage
from .serializers import RoomSerializer , TextMessageSerializer , RoomListSerializer
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from .pagination import MessagesPagination
from django.db.models import Max
from authen.models import PrimaryLanguage



class RoomViewset(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    
class TextMessageViewset(viewsets.ModelViewSet):
    queryset = TextMessage.objects.all()
    serializer_class = TextMessageSerializer
    pagination_class = MessagesPagination
    permission_classes = [IsAuthenticated,]
    
    @action(detail=False, methods=["get"], url_path="room/(?P<room_id>[^/.]+)")
    def get_room_messages(self, request, room_id=None):
        """
        Returns all messages for a given room ID.
        Example URL: /api/messages/room/1/
        """
        if not room_id:
            return Response(
                {"error": "room_id is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        room = Room.objects.filter(id=room_id).first()
        if not room:
            return Response(
                {"error": "Room not Found."},
                status=status.HTTP_404_NOT_FOUND
            )

        messages = TextMessage.objects.filter(room_id=room_id)

        paginator = self.pagination_class()
        paginated_messages = paginator.paginate_queryset(messages, request, view=self)

        message_serializer = self.get_serializer(paginated_messages, many=True)

        pagination_metadata = paginator.get_paginated_response(message_serializer.data).data
        
        del pagination_metadata['results']

        room_serializer = RoomSerializer(room)

        return Response({
            "room": room_serializer.data,
            "messages": message_serializer.data,
            "pagination": pagination_metadata
        }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_rooms(request, user_id):
    rooms = (
        Room.objects.filter(users__id=user_id)
        .annotate(latest_message_time=Max('messages__created_at'))
        .order_by('-latest_message_time')
        .prefetch_related('messages')
    )    
    serializer = RoomListSerializer(rooms, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_languages(request):
    """
    Return array of arrays of Supported languages in chat
    """
    data = PrimaryLanguage.choices
    return Response(data)