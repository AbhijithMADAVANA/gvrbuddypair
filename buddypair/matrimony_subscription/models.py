# models.py
from django.db import models
from U_auth.models import costume_user
from matrimony_admin.models import Subscription
from datetime import timedelta
from django.utils.text import slugify


from django.db import models

class MatrimonySubscription(models.Model):
    PLAN_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('premium', 'Premium (Yearly)'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    slug = models.SlugField(unique=True, blank=True, null=True)
    plan_type = models.CharField(max_length=100, choices=PLAN_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    day_limit = models.IntegerField(default=1)  # Number of days for the plan
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    info = models.TextField(blank=True, null=True)  # Information about the plan

    class Meta:
        verbose_name = "MatrimonySubscription"
        verbose_name_plural = "MatrimonySubscriptions"

    def __str__(self):
        return f"{self.plan_type} - {self.price}"

    # Save slug automatically
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.plan_type)
        super().save(*args, **kwargs)


class Payment(models.Model):
    PAYMENT_TYPE = [
        ('upi', 'upi'),
        ('PayPal', 'PayPal'),
        ('card', 'card'),
        ('razorpay', 'razorpay')
    ]
    user = models.ForeignKey(costume_user, on_delete=models.CASCADE, related_name="userpayment_details")
    slug_name = models.SlugField(unique=True, blank=True, null=True)  # New slug field
    subscription_plan = models.ForeignKey(MatrimonySubscription, related_name="sub_plan", on_delete=models.CASCADE)
    payment_type = models.CharField(choices=PAYMENT_TYPE, max_length=50)
    razorpay_order_id = models.CharField(max_length=100,null=True)
    razorpay_payment_id = models.CharField(max_length=100,null=True)
    razorpay_signature = models.CharField(max_length=255,null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"sub_paln_{self.user.username}"
    

    def save(self, *args, **kwargs):
        if not self.slug_name:
            self.slug_name = slugify(self.subscription_plan.plan_type)

        super().save(*args, **kwargs)


# class RazorpayDetails(models.Model):
#     payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="payment_details")
#     razorpay_order_id = models.CharField(max_length=100,null=True)
#     razorpay_payment_id = models.CharField(max_length=100,null=True)
#     razorpay_signature = models.CharField(max_length=255,null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

# class CardDetails(models.Model):
#     payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="payment_details")
#     card_number = models.CharField(max_length=50)
#     expiry_date = models.CharField(max_length=50)
#     cvv = models.CharField(max_length=50)
#     created_at = models.DateTimeField(auto_now_add=True)

# class UPIDetails(models.Model):
#     payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="payment_details")
#     upi_id = models.CharField(max_length=50)
#     upi_name = models.CharField(max_length=50)
#     created_at = models.DateTimeField(auto_now_add=True)

