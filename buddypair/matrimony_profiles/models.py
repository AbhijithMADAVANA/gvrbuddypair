from django.db import models
from U_auth.models import UserPersonalDetails, costume_user
# Create your models here.


# ..............Target user profile flow model here.............................

class InterestRequest(models.Model):
    sender=models.ForeignKey(costume_user, related_name="sent_requests", on_delete=models.CASCADE)
    receiver=models.ForeignKey(costume_user, related_name="received_requests", on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ], default='pending')

    def __str__(self):
        return f"From {self.sender} to {self.receiver}: {self.status}"
    
class Shortlist(models.Model):
    user = models.ForeignKey(costume_user, related_name='shortlists', on_delete=models.CASCADE)  # The user who shortlists
    shortlisted_user = models.ForeignKey(costume_user, related_name='shortlisted_by', on_delete=models.CASCADE)  # The shortlisted user
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} shortlisted {self.shortlisted_user.username}"


class MatrimonyFriendship(models.Model):
    user1 = models.ForeignKey(costume_user, related_name="friendships_initiated_matrimony", on_delete=models.CASCADE)
    user2 = models.ForeignKey(costume_user, related_name="friendships_received_matrimony", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"Friendship between {self.user1} and {self.user2}"



from django.utils import timezone

class MatrimonyProfileViewCounter(models.Model):
    viewer = models.ForeignKey(costume_user, on_delete=models.CASCADE, related_name='matrimony_profile_views')
    viewed_user = models.ForeignKey(costume_user, on_delete=models.CASCADE, related_name='matrimony_viewed_profiles')
    view_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.viewer.username} viewed {self.viewed_user.username} on {self.view_date}"