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


# Create your views here.

# class UserProfileView(TemplateView):
#     template_name = 'dt/users_pr_view.html'

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

# views.py
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import DatingProfileView

class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'dt/users_pr_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('user_id')
        if user_id:
            user = get_object_or_404(costume_user, id=user_id)
            user_details = get_object_or_404(UserPersonalDetails, user=user)
            additional_details = get_object_or_404(AdditionalDetails, user=user)
            pictures = Pictures.objects.filter(user=user_details)

            # Log the profile view if the viewer is not viewing their own profile
            if self.request.user != user:
                DatingProfileView.objects.get_or_create(viewer=self.request.user, viewed=user)

            context['user'] = user
            context['user_details'] = user_details
            context['additional_details'] = additional_details
            context['pictures'] = pictures
        return context

# views.py
from django.views.generic import ListView

class ProfileViewersListView(LoginRequiredMixin, ListView):
    model = DatingProfileView
    template_name = 'dt/profile_viewer.html'
    context_object_name = 'viewers'

    def get_queryset(self):
        # Get the logged-in user
        user = self.request.user
        # Return all ProfileView entries where the logged-in user is the viewed profile
        return DatingProfileView.objects.filter(viewed=user).order_by('-timestamp')


# #Interest request View
# class SendRequestView(RedirectNotAuthenticatedUserMixin, View):
#     def post(self, request, *args, **kwargs):
#         sender = request.user
#         receiver = get_object_or_404(costume_user, id=self.kwargs['pk'])
        
#         existing_request = Dating_InterestRequest.objects.filter(sender=sender, receiver=receiver).exists()
        
#         if existing_request:
#             messages.warning(request, "You have already sent a request to this user.")
#             return redirect(reverse('dating_profiles:profile', kwargs={'user_id': receiver.id}))
#         else:
#             try:
#                 Dating_InterestRequest.objects.create(sender=sender, receiver=receiver)
#                 messages.success(request, "Interest request sent successfully!")
#                 return redirect(reverse_lazy('dating_profiles:sented_request'))
#             except Exception as e:
#                 messages.error(request, f"Failed to send interest request: {str(e)}")
#                 return redirect(reverse('dating_profiles:profile', kwargs={'user_id': receiver.id}))
            
        
# class SendRequestView(RedirectNotAuthenticatedUserMixin, View):
#     def post(self, request, *args, **kwargs):
#         sender = request.user
#         receiver = get_object_or_404(costume_user, id=self.kwargs['pk'])
        
#         existing_request = Dating_InterestRequest.objects.filter(sender=sender, receiver=receiver).exists()
        
#         if existing_request:
#             messages.warning(request, "You have already sent a request to this user.")
#             return redirect(reverse('dating_profiles:profile', kwargs={'user_id': receiver.id}))
#         else:
#             try:
#                 Dating_InterestRequest.objects.create(sender=sender, receiver=receiver)
#                 messages.success(request, "Interest request sent successfully!")
#                 return redirect(reverse_lazy('dating_profiles:sented_request'))
#             except Exception as e:
#                 messages.error(request, f"Failed to send interest request: {str(e)}")
#                 return redirect(reverse('dating_profiles:profile', kwargs={'user_id': receiver.id}))


# class SendRequestView(RedirectNotAuthenticatedUserMixin, View):
#     def post(self, request, *args, **kwargs):
#         sender = request.user
#         receiver = get_object_or_404(costume_user, id=self.kwargs['pk'])
        
#         existing_request = Dating_InterestRequest.objects.filter(sender=sender, receiver=receiver).exists()
        
#         if existing_request:
#             messages.warning(request, "You have already sent a request to this user.")
#             resolved_url = reverse('dating_profiles:profile', kwargs={'user_id': receiver.id})
#             print(f"Resolved URL: {resolved_url}")  # Debug statement
#             return redirect(resolved_url)
#         else:
#             try:
#                 Dating_InterestRequest.objects.create(sender=sender, receiver=receiver)
#                 messages.success(request, "Interest request sent successfully!")
#                 resolved_url = reverse_lazy('dating_profiles:sented_request')
#                 print(f"Resolved URL: {resolved_url}")  # Debug statement
#                 return redirect(resolved_url)
#             except Exception as e:
#                 messages.error(request, f"Failed to send interest request: {str(e)}")
#                 resolved_url = reverse('dating_profiles:profile', kwargs={'user_id': receiver.id})
#                 print(f"Resolved URL: {resolved_url}")  # Debug statement
#                 return redirect(resolved_url)

# class SendRequestView(RedirectNotAuthenticatedUserMixin, View):
#     def post(self, request, *args, **kwargs):
#         sender = request.user
#         receiver = get_object_or_404(costume_user, id=self.kwargs['pk'])
        
#         # Check for existing request only with "pending" or "accepted" status
#         existing_request = Dating_InterestRequest.objects.filter(
#             sender=sender, receiver=receiver
#         ).exclude(status='rejected').exists()
        
#         if existing_request:
#             messages.warning(request, "You have already sent a request to this user.")
#             resolved_url = reverse('dating_profiles:profile', kwargs={'user_id': receiver.id})
#             return redirect(resolved_url)
#         else:
#             try:
#                 Dating_InterestRequest.objects.create(sender=sender, receiver=receiver)
#                 messages.success(request, "Interest request sent successfully!")
#                 resolved_url = reverse_lazy('dating_profiles:sented_request')
#                 return redirect(resolved_url)
#             except Exception as e:
#                 messages.error(request, f"Failed to send interest request: {str(e)}")
#                 resolved_url = reverse('dating_profiles:profile', kwargs={'user_id': receiver.id})
#                 return redirect(resolved_url)

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
    template_name = 'dt/send.html'
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
    template_name = 'dt/received.html'
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


# class HandleRequestView(RedirectNotAuthenticatedUserMixin, View):
#     def post(self, request, *args, **kwargs):
#         interest_request = get_object_or_404(Dating_InterestRequest, id=self.kwargs['pk'], receiver=request.user)
#         action = self.kwargs.get('action')  # This fetches the value of 'action' from the URL ('accept' or 'reject').
        
#         if action == 'accept':  # If 'action' is 'accept'
#             interest_request.status = 'accepted'  # Set the request's status to 'accepted'
#             messages.success(request, "Interest request has been accepted successfully!")
#         elif action == 'reject':  # Otherwise, if 'action' is 'reject'
#             interest_request.status = 'rejected'  # Set the request's status to 'rejected'
#             messages.success(request, "Interest request has been rejected successfully!")

#         interest_request.save()
#         return redirect(reverse_lazy('dating_profiles:received_request'))


# class HandleRequestView(RedirectNotAuthenticatedUserMixin, View):
#     def post(self, request, *args, **kwargs):
#         interest_request = get_object_or_404(Dating_InterestRequest, id=self.kwargs['pk'], receiver=request.user)
#         action = self.kwargs.get('action')  # This fetches the value of 'action' from the URL ('accept' or 'reject').
        
#         if action == 'accept':  # If 'action' is 'accept'
#             interest_request.status = 'accepted'  # Set the request's status to 'accepted'
#             messages.success(request, "Interest request has accepted successfully!")
#         elif action == 'reject':  # Otherwise, if 'action' is 'reject'
#             interest_request.status = 'rejected'  # Set the request's status to 'rejected'
#             messages.success(request, "Interest request has rejected successfully!")

#         interest_request.save()
#         return redirect(reverse_lazy('dating_profiles:received_request'))

# class AcceptedRequestView(RedirectNotAuthenticatedUserMixin, ListView):
#     model = Dating_InterestRequest
#     template_name = 'dt/accept.html'
#     context_object_name = 'accepted_requests'
#     ordering = ["-created_at"]

#     def get_queryset(self):
#         queryset = Dating_InterestRequest.objects.filter(
#             Q(sender=self.request.user, status='accepted')|
#             Q(receiver=self.request.user, status='accepted')
#         )
#         search_query = self.request.GET.get('search')
#         if search_query:
#             queryset = queryset.filter(
#                 Q(sender__username__icontains=search_query) |
#                 Q(sender__first_name__icontains=search_query) |
#                 Q(sender__user_details__bio__icontains=search_query) |
#                 Q(receiver__username__icontains=search_query) |
#                 Q(receiver__first_name__icontains=search_query) |
#                 Q(receiver__user_details__bio__icontains=search_query)
#             )
#         return queryset.distinct()

class AcceptedRequestView(RedirectNotAuthenticatedUserMixin, ListView):
    model = Dating_InterestRequest
    template_name = 'dt/accept.html'  # Ensure dating-specific template
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



# class RejectedRequestView(RedirectNotAuthenticatedUserMixin, ListView):
#     model = Dating_InterestRequest
#     template_name = 'dt/reject.html'
#     context_object_name = 'rejected_requests'
#     ordering = ["-created_at"]

#     def get_queryset(self):
#         queryset = Dating_InterestRequest.objects.filter(
#             Q(sender=self.request.user, status='rejected')|
#             Q(receiver=self.request.user, status='rejected')
#         )
#         search_query = self.request.GET.get('search')
#         print(search_query)
#         if search_query:
#             queryset = queryset.filter(
#                 Q(sender__username__icontains=search_query) |
#                 Q(sender__first_name__icontains=search_query) |
#                 Q(sender__user_details__bio__icontains=search_query) |
#                 Q(receiver__username__icontains=search_query) |
#                 Q(receiver__first_name__icontains=search_query) |
#                 Q(receiver__user_details__bio__icontains=search_query)
#             )
#         return queryset

class RejectedRequestView(RedirectNotAuthenticatedUserMixin, ListView):
    model = Dating_InterestRequest
    template_name = 'dt/reject.html'  # Ensure dating-specific template
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

    
# class DeleteRequestView(RedirectNotAuthenticatedUserMixin,View):
#     def post (self, request, *args, **kwargs):
#         interest_request = get_object_or_404(Dating_InterestRequest, sender= request.user, id=self.kwargs['pk'])
#         try:
#             interest_request.delete()
#             messages.success(request,"Interest request deleted successfully!")
#         except Exception as e:
#             messages.error(request, f"Failed to delete interest request: {str(e)}")
#         return redirect(reverse('dating_profiles:sented_request'))

class DeleteRequestView(RedirectNotAuthenticatedUserMixin, View):
    def post(self, request, *args, **kwargs):
        interest_request = get_object_or_404(Dating_InterestRequest, sender=request.user, id=self.kwargs['pk'])
        try:
            interest_request.delete()
            messages.success(request, "Interest request deleted successfully!")
        except Exception as e:
            messages.error(request, f"Failed to delete interest request: {str(e)}")
        return redirect(reverse('dating_profiles:sented_request'))


# class ShortlistView(LoginRequiredMixin, ListView):
#     model = Dating_Shortlist
#     template_name = 'dt/shortlist.html'
#     context_object_name = 'shortlist'
#     ordering = ["-created at"]

#     def get_queryset(self):
#         return Dating_Shortlist.objects.filter(user=self.request.user)

class ShortlistView(LoginRequiredMixin, ListView):
    model = Dating_Shortlist
    template_name = 'dt/shortlist.html'  # Ensure dating-specific template
    context_object_name = 'shortlist'
    ordering = ["-created_at"]

    def get_queryset(self):
        return Dating_Shortlist.objects.filter(user=self.request.user)


# class AddToShortlistView(LoginRequiredMixin, View):
#     def post(self, request, *args, **kwargs):
#         shortlisted_user = get_object_or_404(costume_user, id=self.kwargs['user_id'])
#         user = request.user

#         # Check if the user is already in the shortlist
#         if Dating_Shortlist.objects.filter(user=user, shortlisted_user=shortlisted_user).exists():
#             messages.warning(request, "You have already shortlisted this user.")
#             return redirect(reverse('dating_profiles:profile', kwargs={'user_id': shortlisted_user.id}))
#         else:
#             Dating_Shortlist.objects.create(user=user, shortlisted_user=shortlisted_user)
#             messages.success(request, "User successfully added to your shortlist.")
#             return redirect(reverse('dating_profiles:shortlist'))

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


       
# class RemoveFromShortlistView(LoginRequiredMixin, View):
#     def post(self, request, *args, **kwargs):
#         shortlist_entry = get_object_or_404(Dating_Shortlist, user=request.user, shortlisted_user_id=self.kwargs['user_id'])

#         # try:
#         shortlist_entry.delete()

#         if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#             return JsonResponse({'status': 'success', 'message': 'User removed from your shortlist.'})
#         else:
#             messages.success(request, "User removed from your shortlist.")
#             return redirect(reverse('dating_profiles:shortlist'))
#         # except Exception as e:
#         #     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         #         return JsonResponse({'status': 'error', 'message': f'Error removing user: {str(e)}'})
#         #     else:
#         #         messages.error(request, f"Error removing user: {str(e)}")
      
#         return redirect(reverse('dating_profiles:shortlist'))


class RemoveFromShortlistView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        shortlist_entry = get_object_or_404(Dating_Shortlist, user=request.user, shortlisted_user_id=self.kwargs['user_id'])

        shortlist_entry.delete()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'User removed from your shortlist.'})
        else:
            messages.success(request, "User removed from your shortlist.")
            return redirect(reverse('dating_profiles:shortlist'))


# class ShortlistByView(LoginRequiredMixin, ListView):
#     model = Dating_Shortlist
#     template_name = 'dt/shortlisted_by.html'
#     context_object_name = 'shortlist_by'
#     ordering = ["-created at"]

#     def get_queryset(self):
#         return Dating_Shortlist.objects.filter(shortlisted_user=self.request.user)


class ShortlistByView(LoginRequiredMixin, ListView):
    model = Dating_Shortlist
    template_name = 'dt/shortlisted_by.html'  # Ensure dating-specific template
    context_object_name = 'shortlist_by'
    ordering = ["-created_at"]

    def get_queryset(self):
        return Dating_Shortlist.objects.filter(shortlisted_user=self.request.user)

