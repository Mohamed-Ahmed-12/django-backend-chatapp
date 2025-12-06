from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()
# Create your models here.
class Room(models.Model):
    name=models.CharField(max_length=255,blank=False , null=True , unique=True)
    created_at =  models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(User ,related_name='rooms')
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Chat Room'
        verbose_name_plural = 'Chat Rooms'
        
    def __str__(self):
        return self.name
    
    @property
    def group_chat(self):
        """
        bool function to check if room is group
        """
        return self.users.through.objects.filter(room=self).count() > 2
    
         
class TextMessage(models.Model):
    """
    Model to store individual text messages sent within a chat room.

    This model links a message to a specific room and sender, 
    and tracks creation/edit times.

    Attributes:
        room (ForeignKey): The Room the message belongs to. 
                        Messages are deleted if the Room is deleted (CASCADE).
        sender (ForeignKey): The User who sent the message. 
                            Set to NULL if the User is deleted (SET_NULL).
        text (CharField): The content of the text message (max 255 chars).
        created_at (DateTimeField): Automatically set timestamp of message creation.
        edited_at (DateTimeField): Automatically updated timestamp on message modification.
     """

    room = models.ForeignKey(Room , on_delete=models.CASCADE , related_name="messages")
    sender = models.ForeignKey(User , on_delete=models.SET_NULL , null=True)
    text = models.CharField(max_length=255,blank=False , null=False)
    created_at =  models.DateTimeField(auto_now_add=True)
    edited_at =  models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['room', 'created_at']),
        ]
        verbose_name = 'Text Message'
        verbose_name_plural = 'Text Messages'
    
    def clean(self):
        if self.text and len(self.text.strip()) == 0:
            raise ValidationError({'text': 'Message cannot be empty or just whitespace.'})
        if len(self.text) > 255:
            raise ValidationError({'text': 'Message cannot exceed 255 characters.'})
        