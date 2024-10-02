from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, UpdateView, FormView, TemplateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib import messages



# Create your views here.


# sent request.
class SentRequestView(LoginRequiredMixin, View):
    template_name = 'dating_rightmenu/sent_request.html'

    def get(self, request, *args, **kwargs):
        # Get the list of costume_users to whom the logged-in costume_user has sent connection requests
        sent_requests = ConnectionRequest.objects.filter(
            sender=request.costume_user,
            status=ConnectionRequest.SENDER
        ).select_related('receiver')

        # Prepare context data
        context = {
            'sent_requests': sent_requests
        }

        return render(request, self.template_name, context)


# accept request.
class AcceptRequestView(LoginRequiredMixin, View):
    template_name = 'dating_rightmenu/accept_request.html'  # Update with your correct template path

    def get(self, request, *args, **kwargs):
        # Filter the connection requests where the logged-in costume_user is the sender and the receiver has accepted
        accepted_requests = ConnectionRequest.objects.filter(
            sender=request.costume_user,
            status=ConnectionRequest.ACCEPTED
        ).select_related('receiver')

        context = {
            'accepted_requests': accepted_requests
        }

        return render(request, self.template_name, context)
    


# reject request.
class RejectRequestView(View):
    template_name = 'dating_rightmenu/reject_request.html'  # Correct path to your template

    def get(self, request, *args, **kwargs):
        declined_requests = ConnectionRequest.objects.filter(
            sender=request.costume_user,
            status=ConnectionRequest.DECLINED  # Adjust this to match your model's status for declined requests
        ).select_related('receiver')

        context = {
            'declined_requests': declined_requests
        }

        return render(request, self.template_name, context)


# recived request.
class ReceivedRequestView(View):
    template_name = 'dating_rightmenu/recived_request.html'  # Path to your template

    def get(self, request, *args, **kwargs):
        # Filter connection requests where the logged-in costume_user is the receiver
        received_requests = ConnectionRequest.objects.filter(
            receiver=request.costume_user,
            status=ConnectionRequest.SENDER  # Adjust this if needed based on your status field
        ).select_related('sender')  # To optimize database access for sender data

        context = {
            'received_requests': received_requests
        }

        return render(request, self.template_name, context)


# contacted.
class ContactedView(TemplateView):
    template_name = 'dating_rightmenu/contacted.html'


# viewed my profile.
class ViewedProfileView(TemplateView):
    template_name = 'dating_rightmenu/viewed_profile.html'



# send and cancel the friend request.   
class SendConnectionRequestView(View):
    def post(self, request, costume_user_id):
        receiver = get_object_or_404(costume_user, id=costume_user_id)

        # Check if a connection request already exists
        existing_request = ConnectionRequest.objects.filter(sender=request.costume_user, receiver=receiver).first()

        if existing_request:
            if existing_request.status == ConnectionRequest.ACCEPTED:
                messages.info(request, "You are already friends.")
            else:
                # Cancel the request if it already exists and is not accepted
                existing_request.delete()
                messages.success(request, "Connection request canceled.")
        else:
            # Create a new connection request if no request exists
            ConnectionRequest.objects.create(
                sender=request.costume_user,
                receiver=receiver,
                status=ConnectionRequest.SENDER
            )
            messages.success(request, "Connection request sent.")

        return redirect('rightmenubar:home')


# accept the request in received page.
class AcceptConnectionRequestView(View):
    def get(self, request, request_id):
        connection_request = get_object_or_404(ConnectionRequest, id=request_id, receiver=request.costume_user)
        connection_request.accept()
        messages.success(request, "Connection request accepted.")
        return redirect('rightmenubar:recived_request')


# decline the request in received page.
class DeclineConnectionRequestView(View):
    def get(self, request, request_id):
        connection_request = get_object_or_404(ConnectionRequest, id=request_id, receiver=request.costume_user)
        connection_request.decline()
        messages.success(request, "Connection request declined.")
        return redirect('rightmenubar:recived_request')
    

# shortlisted page.
class ShortListedView(LoginRequiredMixin, ListView):
    model = costume_user
    template_name = 'dating_rightmenu/shortlist.html'
    context_object_name = 'shortlisted_costume_users'

    def get_queryset(self):
        # Get all costume_users that the logged-in costume_user has shortlisted
        return self.request.costume_user.shortlisted.all()


# remove the shortlisted costume_user.
class RemoveShortlistedcostume_userView(LoginRequiredMixin, View):
    def post(self, request, pk):
        costume_user_to_remove = get_object_or_404(costume_user, pk=pk)
        request.costume_user.shortlisted_costume_users.remove(costume_user_to_remove)
        return redirect('rightmenubar:shortlist')
    

# # function for shortlist a costume_user.
# class Shortlistcostume_userView(LoginRequiredMixin, View):
#     def post(self, request, pk):
#         costume_user_to_shortlist = get_object_or_404(costume_user, pk=pk)
#         if costume_user_to_shortlist != request.costume_user:  # Ensure costume_users cannot shortlist themselves
#             request.costume_user.shortlisted_costume_users.add(costume_user_to_shortlist)
#         return redirect('dating:home')


# shortlisted by costume_users page.
class ShortListedByView(LoginRequiredMixin, View):
    template_name = 'dating_rightmenu/shortlisted_by.html'  # Make sure the template matches your template file name

    def get(self, request, *args, **kwargs):
        # Get all costume_users who have shortlisted the currently logged-in costume_user
        shortlisted_by_costume_users = costume_user.objects.filter(shortlisted_costume_users=request.costume_user)

        context = {
            'shortlisted_by_costume_users': shortlisted_by_costume_users,
        }

        return render(request, self.template_name, context)