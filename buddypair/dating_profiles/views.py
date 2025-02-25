import json
from django.http import JsonResponse
from django.shortcuts import redirect, render

#profile display imports :
from django.shortcuts import render, get_object_or_404
from U_auth.models import *
from django.http import JsonResponse

#for  interest-request
from .models import Dating_InterestRequest,Dating_Shortlist
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q  # Import Q for complex queries
from django.contrib import messages
from U_auth.permissions import RedirectNotAuthenticatedUserMixin
from typing import Any
from django.views.generic import TemplateView
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import DatingProfileView

# class UserProfileView(LoginRequiredMixin, TemplateView):
#     template_name = 'dating_profiles/users_pr_view.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user_id = self.kwargs.get('user_id')
#         if user_id:
#             user = get_object_or_404(costume_user, id=user_id)
#             user_details = get_object_or_404(UserPersonalDetails, user=user)
#             additional_details = get_object_or_404(AdditionalDetails, user=user)
#             pictures = Pictures.objects.filter(user=user_details)

#             # Log the profile view if the viewer is not viewing their own profile
#             if self.request.user != user:
#                 DatingProfileView.objects.get_or_create(viewer=self.request.user, viewed=user)

#             context['user'] = user
#             context['user_details'] = user_details
#             context['additional_details'] = additional_details
#             context['pictures'] = pictures
#         return context

# views.py
from django.utils.timezone import now
from datetime import timedelta
from .models import ProfileViewCounter

# class UserProfileView(LoginRequiredMixin, TemplateView):
#     template_name = 'dating_profiles/users_pr_view.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user_id = self.kwargs.get('user_id')
#         if user_id:
#             user = get_object_or_404(costume_user, id=user_id)
#             user_details = get_object_or_404(UserPersonalDetails, user=user)
#             additional_details = get_object_or_404(AdditionalDetails, user=user)
#             pictures = Pictures.objects.filter(user=user_details)

#             # Check if the logged-in user is subscribed
#             if not self.request.user.is_subscribed:
#                 # Check if they have viewed more than 5 profiles today
#                 today = now().date()
#                 views_today = ProfileViewCounter.objects.filter(
#                     viewer=self.request.user,
#                     view_date__date=today
#                 ).count()

#                 if views_today >= 5 and self.request.user != user:
#                     # Redirect to the subscription modal if they've viewed 5 profiles
#                     context['show_subscription_modal'] = True  # Flag to show the modal
#                     return context

#             # Log the profile view if the viewer is not viewing their own profile
#             if self.request.user != user:
#                 # Create a new profile view record
#                 ProfileViewCounter.objects.create(viewer=self.request.user, viewed_user=user)
#                 DatingProfileView.objects.get_or_create(viewer=self.request.user, viewed=user)

#             context['user'] = user
#             context['user_details'] = user_details
#             context['additional_details'] = additional_details
#             context['pictures'] = pictures
#             context['show_subscription_modal'] = False  # Don't show the modal
#         return context
from dating_subscription.models import Payment  # Adjust the import path based on your project structure
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'dating_profiles/users_pr_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('user_id')
        
        if user_id:
            user = get_object_or_404(costume_user, id=user_id)
            user_details = get_object_or_404(UserPersonalDetails, user=user)
            additional_details = get_object_or_404(AdditionalDetails, user=user)
            pictures = Pictures.objects.filter(user=user_details)

            # Check if the logged-in user has a successful payment
            successful_payment = Payment.objects.filter(user=self.request.user, status='success').exists()

            if not successful_payment:
                # Check if they have viewed more than 5 profiles in total
                total_views = ProfileViewCounter.objects.filter(viewer=self.request.user).count()

                # Check if the current profile has already been viewed
                already_viewed = ProfileViewCounter.objects.filter(viewer=self.request.user, viewed_user=user).exists()

                if total_views >= 5 and not already_viewed and self.request.user != user:
                    context['show_subscription_modal'] = True  # Show the modal if they reached limit
                    return context

            # Log the profile view if the viewer is not viewing their own profile
            if self.request.user != user:
                # Create a new profile view record
                ProfileViewCounter.objects.create(viewer=self.request.user, viewed_user=user)
                DatingProfileView.objects.get_or_create(viewer=self.request.user, viewed=user)

            # Add user details to the context
            context['user'] = user
            context['user_details'] = user_details
            context['additional_details'] = additional_details
            context['pictures'] = pictures
            context['show_subscription_modal'] = False  # Don't show the modal if the user is viewing their own profile
            
        return context


from django.views.generic import ListView

class ProfileViewersListView(LoginRequiredMixin, ListView):
    model = DatingProfileView
    template_name = 'dating_profiles/profile_viewer.html'
    context_object_name = 'viewers'

    def get_queryset(self):
        # Get the logged-in user
        user = self.request.user
        # Return all ProfileView entries where the logged-in user is the viewed profile
        return DatingProfileView.objects.filter(viewed=user).order_by('-timestamp')


from .models import Friendship
class SendRequestView(RedirectNotAuthenticatedUserMixin, View):
    def post(self, request, *args, **kwargs):
        sender = request.user
        receiver = get_object_or_404(costume_user, id=self.kwargs['pk'])
        
        # Check if there's an existing request between the two users, regardless of who sent it
        existing_request = Dating_InterestRequest.objects.filter(
            models.Q(sender=sender, receiver=receiver) | 
            models.Q(sender=receiver, receiver=sender)
        ).exclude(status='rejected').exists()
        
        # Check if they are already friends
        are_friends = Friendship.objects.filter(
            models.Q(user1=sender, user2=receiver) |
            models.Q(user1=receiver, user2=sender)
        ).exists()
        
        if are_friends:
            # If they are already friends, show the message
            messages.info(request, "You are already friends with this user.")
            resolved_url = reverse('dating_profiles:profile', kwargs={'user_id': receiver.id})
            return redirect(resolved_url)
        elif existing_request:
            # If a request exists, but not friends yet, show this message
            messages.warning(request, "You have already sent a request to this user.")
            resolved_url = reverse('dating_profiles:profile', kwargs={'user_id': receiver.id})
            return redirect(resolved_url)
        else:
            try:
                # Create a new interest request
                Dating_InterestRequest.objects.create(sender=sender, receiver=receiver)
                messages.success(request, "Interest request sent successfully!")
                resolved_url = reverse_lazy('dating_profiles:sented_request')
                return redirect(resolved_url)
            except Exception as e:
                # Handle any errors during request creation
                messages.error(request, f"Failed to send interest request: {str(e)}")
                resolved_url = reverse('dating_profiles:profile', kwargs={'user_id': receiver.id})
                return redirect(resolved_url)




class SentedRequestView(RedirectNotAuthenticatedUserMixin,ListView):
    model = Dating_InterestRequest
    template_name = 'dating_profiles/send.html'
    context_object_name = 'sent_requests'
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = Dating_InterestRequest.objects.filter(sender=self.request.user, status="pending").order_by("-created_at")
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(receiver__username__icontains=search_query) |
                Q(receiver__first_name__icontains=search_query) |
                Q(receiver__user_details__bio__icontains=search_query)
            )
        return queryset
    
class ReceivedRequestView(RedirectNotAuthenticatedUserMixin,ListView):
    model = Dating_InterestRequest
    template_name = 'dating_profiles/received.html'
    context_object_name = 'received_requests'
    
    def get_queryset(self):
        queryset = Dating_InterestRequest.objects.filter(receiver=self.request.user, status="pending").order_by("-created_at")
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(sender__username__icontains=search_query) |
                Q(sender__first_name__icontains=search_query) |
                Q(sender__user_details__bio__icontains=search_query)
            )
        return queryset

class HandleRequestView(RedirectNotAuthenticatedUserMixin, View):
    def post(self, request, *args, **kwargs):
        interest_request = get_object_or_404(Dating_InterestRequest, id=self.kwargs['pk'], receiver=request.user)
        action = self.kwargs.get('action')  # This fetches the value of 'action' from the URL ('accept' or 'reject').
        
        if action == 'accept':  # If 'action' is 'accept'
            interest_request.status = 'accepted'  # Set the request's status to 'accepted'
            messages.success(request, "Interest request has been accepted successfully!")
            
            # Create a friendship
            Friendship.objects.get_or_create(
                user1=min(interest_request.sender, interest_request.receiver, key=lambda x: x.id),
                user2=max(interest_request.sender, interest_request.receiver, key=lambda x: x.id)
            )
        elif action == 'reject':  # Otherwise, if 'action' is 'reject'
            interest_request.status = 'rejected'  # Set the request's status to 'rejected'
            messages.success(request, "Interest request has been rejected successfully!")

        interest_request.save()
        return redirect(reverse_lazy('dating_profiles:received_request'))


class AcceptedRequestView(RedirectNotAuthenticatedUserMixin, ListView):
    model = Dating_InterestRequest
    template_name = 'dating_profiles/accept.html'  # Ensure dating-specific template
    context_object_name = 'accepted_requests'
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = Dating_InterestRequest.objects.filter(
            Q(sender=self.request.user, status='accepted')|
            Q(receiver=self.request.user, status='accepted')
        )
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(sender__username__icontains=search_query) |
                Q(sender__first_name__icontains=search_query) |
                Q(sender__user_details__bio__icontains=search_query) |
                Q(receiver__username__icontains=search_query) |
                Q(receiver__first_name__icontains=search_query) |
                Q(receiver__user_details__bio__icontains=search_query)
            )
        return queryset.distinct()


class RejectedRequestView(RedirectNotAuthenticatedUserMixin, ListView):
    model = Dating_InterestRequest
    template_name = 'dating_profiles/reject.html'  # Ensure dating-specific template
    context_object_name = 'rejected_requests'
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = Dating_InterestRequest.objects.filter(
            Q(sender=self.request.user, status='rejected')|
            Q(receiver=self.request.user, status='rejected')
        )
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(sender__username__icontains=search_query) |
                Q(sender__first_name__icontains=search_query) |
                Q(sender__user_details__bio__icontains=search_query) |
                Q(receiver__username__icontains=search_query) |
                Q(receiver__first_name__icontains=search_query) |
                Q(receiver__user_details__bio__icontains=search_query)
            )
        return queryset


class DeleteRequestView(RedirectNotAuthenticatedUserMixin, View):
    def post(self, request, *args, **kwargs):
        interest_request = get_object_or_404(Dating_InterestRequest, sender=request.user, id=self.kwargs['pk'])
        try:
            interest_request.delete()
            messages.success(request, "Interest request deleted successfully!")
        except Exception as e:
            messages.error(request, f"Failed to delete interest request: {str(e)}")
        return redirect(reverse('dating_profiles:sented_request'))


class ShortlistView(LoginRequiredMixin, ListView):
    model = Dating_Shortlist
    template_name = 'dating_profiles/shortlist.html'  # Ensure dating-specific template
    context_object_name = 'shortlist'
    ordering = ["-created_at"]

    def get_queryset(self):
        return Dating_Shortlist.objects.filter(user=self.request.user)

class AddToShortlistView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        shortlisted_user = get_object_or_404(costume_user, id=self.kwargs['user_id'])
        user = request.user

        # Check if the user is already in the shortlist
        if Dating_Shortlist.objects.filter(user=user, shortlisted_user=shortlisted_user).exists():
            messages.warning(request, "You have already shortlisted this user.")
            return redirect(reverse('dating_profiles:profile', kwargs={'user_id': shortlisted_user.id}))
        else:
            Dating_Shortlist.objects.create(user=user, shortlisted_user=shortlisted_user)
            messages.success(request, "User successfully added to your shortlist.")
            return redirect(reverse('dating_profiles:shortlist'))


class RemoveFromShortlistView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        shortlist_entry = get_object_or_404(Dating_Shortlist, user=request.user, shortlisted_user_id=self.kwargs['user_id'])

        shortlist_entry.delete()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'User removed from your shortlist.'})
        else:
            messages.success(request, "User removed from your shortlist.")
            return redirect(reverse('dating_profiles:shortlist'))


class ShortlistByView(LoginRequiredMixin, ListView):
    model = Dating_Shortlist
    template_name = 'dating_profiles/shortlisted_by.html'  # Ensure dating-specific template
    context_object_name = 'shortlist_by'
    ordering = ["-created_at"]

    def get_queryset(self):
        return Dating_Shortlist.objects.filter(shortlisted_user=self.request.user)

