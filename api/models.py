from django.db import models
import string
import random

def generate_unique_code():
    length = 6

    while True:
        random_code = ''.join(random.choices(string.ascii_uppercase, k=length))
        if Room.objects.filter(code=random_code).count() == 0:
            break

    return random_code     

# Create your models here.
class Room(models.Model):
    # Unique code to identify a room
    code = models.CharField(max_length=8, default="", unique=True)

    # Each room has a host
    host = models.CharField(max_length=50, unique=True)
    
    # Permission for guest to pause or play the music
    guest_can_pause = models.BooleanField(null=False, default=False)

    # Number of votes need to skip a current song --> set to 1 vote
    votes_to_skip = models.IntegerField(null=False, default=1)

    # Time create the room
    created_at = models.DateTimeField(auto_now_add=True)
