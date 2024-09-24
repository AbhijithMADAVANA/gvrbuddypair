from django.db import models
from U_auth.models import *

# # Create your models here.


# class ConnectionRequest(models.Model):
#     SENDER = 'sent'
#     ACCEPTED = 'accepted'
#     DECLINED = 'declined'

#     STATUS_CHOICES = [
#         (SENDER, 'Sent'),
#         (ACCEPTED, 'Accepted'),
#         (DECLINED, 'Declined'),
#     ]

#     sender = models.ForeignKey(costume_user, related_name='sent_requests', on_delete=models.CASCADE)
#     receiver = models.ForeignKey(, related_name='received_requests', on_delete=models.CASCADE)
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=SENDER)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('sender', 'receiver')

#     def accept(self):
#         self.status = self.ACCEPTED
#         self.save()

#     def decline(self):
#         self.status = self.DECLINED
#         self.save()
    
#     def cancel(self):
#         if self.status == self.SENDER:
#             self.delete()  # Removes the connection request


#     def __str__(self):
#         return f"{self.sender} to {self.receiver} - {self.status}"



class ConnectionRequest(models.Model):
    SENDER = 'sent'
    ACCEPTED = 'accepted'
    DECLINED = 'declined'

    STATUS_CHOICES = [
        (SENDER, 'Sent'),
        (ACCEPTED, 'Accepted'),
        (DECLINED, 'Declined'),
    ]

    sender = models.ForeignKey(costume_user, related_name='dating_sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(costume_user, related_name='dating_received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=SENDER)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'receiver')

    def accept(self):
        self.status = self.ACCEPTED
        self.save()

    def decline(self):
        self.status = self.DECLINED
        self.save()

    def cancel(self):
        if self.status == self.SENDER:
            self.delete()  # Removes the connection request

    def __str__(self):
        return f"{self.sender} to {self.receiver} - {self.status}"
