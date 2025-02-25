import json
from django.http import JsonResponse
from django.shortcuts import redirect, render

#profile display imports :
from django.shortcuts import render, get_object_or_404
from U_auth.models import *
from django.http import JsonResponse

#for  interest-request
from .models import InterestRequest,Shortlist
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q  # Import Q for complex queries
from django.contrib import messages
from U_auth.permissions import RedirectNotAuthenticatedUserMixin
from typing import Any
from django.views.generic import TemplateView
from django.contrib import messages
from django.urls import reverse, reverse_lazy



# class UserProfileView(TemplateView):
#     template_name = 'matrimony_profiles/users_pr_view.html'

#     def get_context_data(self, **kwargs) -> dict[str, Any]:
#         context = super().get_context_data(**kwargs)
#         user_id = self.kwargs.get('user_id', None)
#         if user_id:
#             user = costume_user.objects.get(id=user_id)
#             user_details = UserPersonalDetails.objects.get(user=user) 
#             additional_details = AdditionalDetails.objects.get(user=user)
#             pictures = Pictures.objects.filter(user=user_details)
#             context['user'] = user
#             context['user_details'] = user_details
#             context['additional_details'] = additional_details
#             context['pictures'] = pictures
#             context['user'] = user
#             return context

from .models import MatrimonyProfileViewCounter
from matrimony_subscriptions.models import MatrimonyPayment
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'matrimony_profiles/users_pr_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('user_id', None)
        
        if user_id:
            user = get_object_or_404(costume_user, id=user_id)
            user_details = get_object_or_404(UserPersonalDetails, user=user)
            additional_details = get_object_or_404(AdditionalDetails, user=user)
            pictures = Pictures.objects.filter(user=user_details)

            # Check if the logged-in user has a successful payment
            successful_payment = MatrimonyPayment.objects.filter(user=self.request.user, status='success').exists()

            # If the user has not made a successful payment
            if not successful_payment:
                # Check if they have viewed more than 5 profiles in total
                total_views = MatrimonyProfileViewCounter.objects.filter(viewer=self.request.user).count()

                # Check if the current profile was already viewed by the user
                already_viewed = MatrimonyProfileViewCounter.objects.filter(viewer=self.request.user, viewed_user=user).exists()

                if total_views >= 5 and not already_viewed and self.request.user != user:
                    context['show_subscription_modal'] = True  # Show the modal if they reached limit
                    return context

            # Log the profile view if the viewer is not viewing their own profile
            if self.request.user != user:
                # Create a new profile view record
                MatrimonyProfileViewCounter.objects.create(viewer=self.request.user, viewed_user=user)

            # Add user details to the context
            context['user'] = user
            context['user_details'] = user_details
            context['additional_details'] = additional_details
            context['pictures'] = pictures
            context['show_subscription_modal'] = False  # Don't show the modal if the user is viewing own profile
            
        return context


# #Interest request View
# class SendRequestView(RedirectNotAuthenticatedUserMixin, View):
#     def post(self, request, *args, **kwargs):
#         sender = request.user
#         receiver = get_object_or_404(costume_user, id=self.kwargs['pk'])
        
#         existing_request = InterestRequest.objects.filter(sender=sender, receiver=receiver).exists()
        
#         if existing_request:
#             messages.warning(request, "You have already sent a request to this user.")
#             return redirect(reverse('matrimony_profile:profile', kwargs={'user_id': receiver.id}))
#         else:
#             try:
#                 InterestRequest.objects.create(sender=sender, receiver=receiver)
#                 messages.success(request, "Interest request sent successfully!")
#                 return redirect(reverse_lazy('matrimony_profile:sented_request'))
#             except Exception as e:
#                 messages.error(request, f"Failed to send interest request: {str(e)}")
#                 return redirect(reverse('matrimony_profile:profile', kwargs={'user_id': receiver.id}))


from .models import MatrimonyFriendship

class SendRequestView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        sender = request.user
        receiver = get_object_or_404(costume_user, id=self.kwargs['pk'])

        # Check if there's any existing request between the two users
        existing_request = InterestRequest.objects.filter(
            Q(sender=sender, receiver=receiver) | 
            Q(sender=receiver, receiver=sender)
        ).exclude(status='rejected').exists()

        # Check if they are already friends
        are_friends = MatrimonyFriendship.objects.filter(
            Q(user1=sender, user2=receiver) |
            Q(user1=receiver, user2=sender)
        ).exists()

        if are_friends:
            messages.info(request, "You are already friends with this user.")
            return redirect(reverse('matrimony_profile:profile', kwargs={'user_id': receiver.id}))
        elif existing_request:
            messages.warning(request, "A request is already pending with this user.")
            return redirect(reverse('matrimony_profile:profile', kwargs={'user_id': receiver.id}))
        else:
            try:
                # Create a new interest request if none exist
                InterestRequest.objects.create(sender=sender, receiver=receiver)
                messages.success(request, "Interest request sent successfully!")
                return redirect(reverse_lazy('matrimony_profile:sented_request'))
            except Exception as e:
                messages.error(request, f"Failed to send interest request: {str(e)}")
                return redirect(reverse('matrimony_profile:profile', kwargs={'user_id': receiver.id}))


        
class SentedRequestView(RedirectNotAuthenticatedUserMixin,ListView):
    model = InterestRequest
    template_name = 'matrimony_profiles/send.html'
    context_object_name = 'sent_requests'
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = InterestRequest.objects.filter(sender=self.request.user, status="pending").order_by("-created_at")
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(receiver__username__icontains=search_query) |
                Q(receiver__first_name__icontains=search_query) |
                Q(receiver__user_details__bio__icontains=search_query)
            )
        return queryset
    
class ReceivedRequestView(RedirectNotAuthenticatedUserMixin,ListView):
    model = InterestRequest
    template_name = 'matrimony_profiles/received.html'
    context_object_name = 'received_requests'
    
    def get_queryset(self):
        queryset = InterestRequest.objects.filter(receiver=self.request.user, status="pending").order_by("-created_at")
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(sender__username__icontains=search_query) |
                Q(sender__first_name__icontains=search_query) |
                Q(sender__user_details__bio__icontains=search_query)
            )
        return queryset

# class HandleRequestView(RedirectNotAuthenticatedUserMixin, View):
#     def post(self, request, *args, **kwargs):
#         interest_request = get_object_or_404(InterestRequest, id=self.kwargs['pk'], receiver=request.user)
#         action = self.kwargs.get('action')  # This fetches the value of 'action' from the URL ('accept' or 'reject').
        
#         if action == 'accept':  # If 'action' is 'accept'
#             interest_request.status = 'accepted'  # Set the request's status to 'accepted'
#             messages.success(request, "Interest request has accepted successfully!")
#         elif action == 'reject':  # Otherwise, if 'action' is 'reject'
#             interest_request.status = 'rejected'  # Set the request's status to 'rejected'
#             messages.success(request, "Interest request has rejected successfully!")

#         interest_request.save()
#         return redirect(reverse_lazy('matrimony_profile:received_request'))


class HandleRequestView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        interest_request = get_object_or_404(InterestRequest, id=self.kwargs['pk'], receiver=request.user)
        action = self.kwargs.get('action')  # This fetches the value of 'action' from the URL ('accept' or 'reject').

        if action == 'accept':
            interest_request.status = 'accepted'
            interest_request.save()  # Save the request status first
            messages.success(request, "Interest request has been accepted successfully!")

            # Check if a friendship already exists before creating a new one
            if not MatrimonyFriendship.objects.filter(
                    Q(user1=interest_request.sender, user2=interest_request.receiver) |
                    Q(user1=interest_request.receiver, user2=interest_request.sender)
            ).exists():
                # Create a friendship if none exists
                MatrimonyFriendship.objects.create(
                    user1=min(interest_request.sender, interest_request.receiver, key=lambda x: x.id),
                    user2=max(interest_request.sender, interest_request.receiver, key=lambda x: x.id)
                )
        elif action == 'reject':
            interest_request.status = 'rejected'
            interest_request.save()
            messages.success(request, "Interest request has been rejected successfully!")

        return redirect(reverse_lazy('matrimony_profile:received_request'))


class AcceptedRequestView(RedirectNotAuthenticatedUserMixin, ListView):
    model = InterestRequest
    template_name = 'matrimony_profiles/accept.html'
    context_object_name = 'accepted_requests'
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = InterestRequest.objects.filter(
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
    model = InterestRequest
    template_name = 'matrimony_profiles/reject.html'
    context_object_name = 'rejected_requests'
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = InterestRequest.objects.filter(
            Q(sender=self.request.user, status='rejected')|
            Q(receiver=self.request.user, status='rejected')
        )
        search_query = self.request.GET.get('search')
        print(search_query)
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
    
class DeleteRequestView(RedirectNotAuthenticatedUserMixin,View):
    def post (self, request, *args, **kwargs):
        interest_request = get_object_or_404(InterestRequest, sender= request.user, id=self.kwargs['pk'])
        try:
            interest_request.delete()
            messages.success(request,"Interest request deleted successfully!")
        except Exception as e:
            messages.error(request, f"Failed to delete interest request: {str(e)}")
        return redirect(reverse('matrimony_profile:sented_request'))

class ShortlistView(LoginRequiredMixin, ListView):
    model = Shortlist
    template_name = 'matrimony_profiles/shortlist.html'
    context_object_name = 'shortlist'
    ordering = ["-created at"]

    def get_queryset(self):
        return Shortlist.objects.filter(user=self.request.user)

class AddToShortlistView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        shortlisted_user = get_object_or_404(costume_user, id=self.kwargs['user_id'])
        user = request.user

        # Check if the user is already in the shortlist
        if Shortlist.objects.filter(user=user, shortlisted_user=shortlisted_user).exists():
            messages.warning(request, "You have already shortlisted this user.")
            return redirect(reverse('matrimony_profile:profile', kwargs={'user_id': shortlisted_user.id}))
        else:
            Shortlist.objects.create(user=user, shortlisted_user=shortlisted_user)
            messages.success(request, "User successfully added to your shortlist.")
            return redirect(reverse('matrimony_profile:shortlist'))

       
class RemoveFromShortlistView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        shortlist_entry = get_object_or_404(Shortlist, user=request.user, shortlisted_user_id=self.kwargs['user_id'])

        # try:
        shortlist_entry.delete()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'User removed from your shortlist.'})
        else:
            messages.success(request, "User removed from your shortlist.")
            return redirect(reverse('matrimony_profile:shortlist'))
        # except Exception as e:
        #     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        #         return JsonResponse({'status': 'error', 'message': f'Error removing user: {str(e)}'})
        #     else:
        #         messages.error(request, f"Error removing user: {str(e)}")
      
        return redirect(reverse('matrimony_profile:shortlist'))

class ShortlistByView(LoginRequiredMixin, ListView):
    model = Shortlist
    template_name = 'matrimony_profiles/shortlisted_by.html'
    context_object_name = 'shortlist_by'
    ordering = ["-created at"]

    def get_queryset(self):
        return Shortlist.objects.filter(shortlisted_user=self.request.user)
