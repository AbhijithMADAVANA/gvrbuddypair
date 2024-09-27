from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

from django.shortcuts import render,redirect
from django.views.generic import TemplateView,ListView
from django.urls import reverse_lazy
from . models import UserPreference
from U_auth.models import costume_user

from django.shortcuts import render,redirect
from django.views.generic import TemplateView,ListView
from U_auth.permissions import RedirectAuthenticatedUserMixin, RedirectNotAuthenticatedUserMixin
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from U_auth.models import *
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
import math
from matrimony_Home.find_distance import find_distance,sort_users_by_distance

# Create your views here.

# class HomeView(ListView):
#     model=costume_user
#     template_name = "home.html"
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user = self.request.user
        
#         context['profiles'] = costume_user.objects.filter(location=user.location.id)[1:3]
#         context['designation_profiles'] = costume_user.objects.filter(designation=user.designation)[1:3]
#         context['qualification_profiles'] = costume_user.objects.filter(qualification=user.qualification)[1:3]
        
#         return context

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

# class HomeView(RedirectNotAuthenticatedUserMixin, SuccessMessageMixin, ListView):
#     model = UserPersonalDetails
#     template_name = 'home.html'
#     context_object_name = 'users'
#     success_message = "This is a success message."

#     def get_queryset(self):
#         user = self.request.user
#         queryset = super().get_queryset()
#         filter_value = self.request.GET.get('filter', 'all')  # Default to 'all' if no filter is provided
#         loged_user = get_object_or_404(UserPersonalDetails, user=user)

#         # Return all users if the filter is 'all' or if no filter is applied
#         if filter_value == 'all':
#             queryset = queryset.all()

#         # Apply filters based on the filter_value if not 'all'
#         elif filter_value == 'Location':
#             queryset = queryset.filter(user__user_details__user_location=loged_user.user_location)
#         elif filter_value == 'Designation':
#             job_details = Job_Details.objects.filter(user=loged_user.user).first()
#             if job_details:
#                 queryset = queryset.filter(user__job_details__designation=job_details.designation)
#         elif filter_value == 'Qualification':
#             user_qualifications = loged_user.qualifications.all()
#             queryset = queryset.filter(qualifications__in=user_qualifications)

#         # Exclude users based on gender preference
#         if loged_user.gender == 'M':
#             queryset = queryset.exclude(Q(user__user_details__gender='M') | Q(user__user_details__gender='O'))
#         elif loged_user.gender == 'F':
#             queryset = queryset.exclude(Q(user__user_details__gender='F') | Q(user__user_details__gender='O'))
#         elif loged_user.gender == 'O':
#             queryset = queryset.all()

#         # Exclude the logged-in user from the queryset
#         queryset = queryset.exclude(user=user)

#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user = self.request.user
#         try:
#             user_details = UserPersonalDetails.objects.get(user=user)
#             context['user_details'] = user_details
#         except UserPersonalDetails.DoesNotExist:
#             context['user_details'] = None
#         return context
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.db.models import Q

class HomeView(RedirectNotAuthenticatedUserMixin, SuccessMessageMixin, ListView):
    model = UserPersonalDetails
    template_name = 'home.html'
    context_object_name = 'users'
    success_message = "This is a success message."

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        filter_value = self.request.GET.get('filter', 'all')  # Default to 'all' if no filter is provided
        logged_user = get_object_or_404(UserPersonalDetails, user=user)

        # Only include users who have a short video
        queryset = queryset.filter(short_video__isnull=False)  # Filter users with short video

        # Apply additional filters based on filter_value (optional)
        if filter_value == 'Location':
            queryset = queryset.filter(user_location=logged_user.user_location)
        elif filter_value == 'Designation':
            job_details = Job_Details.objects.filter(user=logged_user.user).first()
            if job_details:
                queryset = queryset.filter(user__job_details__designation=job_details.designation)
        elif filter_value == 'Qualification':
            user_qualifications = logged_user.qualifications.all()
            queryset = queryset.filter(qualifications__in=user_qualifications)

        # Get logged-in user's interest
        user_interest = UserInterest.objects.filter(user=user).first()
        logged_user_gender = logged_user.gender

        # Apply interest-based filtering if the user has set preferences
        if user_interest:
            if logged_user_gender == 'M':
                # Logged user is male
                if user_interest.interested_in == 'B':
                    # Show both male and female
                    queryset = queryset.filter(gender__in=['M', 'F'])
                elif user_interest.interested_in == 'M':
                    # Show only male
                    queryset = queryset.filter(gender='M')
                elif user_interest.interested_in == 'W':
                    # Show only female
                    queryset = queryset.filter(gender='F')
            elif logged_user_gender == 'F':
                # Logged user is female
                if user_interest.interested_in == 'B':
                    # Show both male and female
                    queryset = queryset.filter(gender__in=['M', 'F'])
                elif user_interest.interested_in == 'M':
                    # Show only male
                    queryset = queryset.filter(gender='M')
                elif user_interest.interested_in == 'W':
                    # Show only female
                    queryset = queryset.filter(gender='F')
            elif logged_user_gender == 'O':
                # Logged user is non-binary/other
                if user_interest.interested_in == 'B':
                    # Show both male and female
                    queryset = queryset.filter(gender__in=['M', 'F'])
                elif user_interest.interested_in == 'M':
                    # Show only male
                    queryset = queryset.filter(gender='M')
                elif user_interest.interested_in == 'W':
                    # Show only female
                    queryset = queryset.filter(gender='F')

        # Exclude the logged-in user from the queryset
        queryset = queryset.exclude(user=user)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        try:
            user_details = UserPersonalDetails.objects.get(user=user)
            context['user_details'] = user_details  # Pass logged-in user details
        except UserPersonalDetails.DoesNotExist:
            context['user_details'] = None

        # Pass only users with short videos for the "story" section
        context['other_users'] = self.get_queryset()  # Pass filtered users
        return context


# class HomeView(RedirectNotAuthenticatedUserMixin, SuccessMessageMixin, ListView):
#     model = UserPersonalDetails
#     template_name = 'home.html'
#     context_object_name = 'users'
#     success_message = "This is a success message."

#     def get_queryset(self):
#         user = self.request.user
#         queryset = super().get_queryset()
#         filter_value = self.request.GET.get('filter', 'all')  # Default to 'all' if no filter is provided
#         loged_user = get_object_or_404(UserPersonalDetails, user=user)

#         # Only include users who have a short video
#         queryset = queryset.filter(short_video__isnull=False)  # Filter users with short video

#         # Additional filters based on filter_value (optional)
#         if filter_value == 'Location':
#             queryset = queryset.filter(user__user_details__user_location=loged_user.user_location)
#         elif filter_value == 'Designation':
#             job_details = Job_Details.objects.filter(user=loged_user.user).first()
#             if job_details:
#                 queryset = queryset.filter(user__job_details__designation=job_details.designation)
#         elif filter_value == 'Qualification':
#             user_qualifications = loged_user.qualifications.all()
#             queryset = queryset.filter(qualifications__in=user_qualifications)

#         # Exclude users based on gender preference
#         if loged_user.gender == 'M':
#             queryset = queryset.exclude(Q(user__user_details__gender='M') | Q(user__user_details__gender='O'))
#         elif loged_user.gender == 'F':
#             queryset = queryset.exclude(Q(user__user_details__gender='F') | Q(user__user_details__gender='O'))
#         elif loged_user.gender == 'O':
#             queryset = queryset.all()

#         # Exclude the logged-in user from the queryset
#         queryset = queryset.exclude(user=user)

#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user = self.request.user
#         try:
#             user_details = UserPersonalDetails.objects.get(user=user)
#             context['user_details'] = user_details  # Pass logged-in user details
#         except UserPersonalDetails.DoesNotExist:
#             context['user_details'] = None

#         # Pass only users with short videos for the "story" section
#         context['other_users'] = self.get_queryset()  # Pass filtered users
#         return context



class UserDashboardView(TemplateView):
    template_name = 'shared/slidbars.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Fetch user personal details
        user_personal_details = UserPersonalDetails.objects.get(user=user)

        context['logged_in_user'] = user
        context['user_details'] = user_personal_details
        return context
    
class EntryView(TemplateView):
    # template_name="shared/sidebars.html"
    template_name = "entry.html"
    success_url = reverse_lazy('userhome:home1')
    def post(self, request, *args, **kwargs):
        print(request.POST)
        # Get or create the UserPreference instance for the logged-in user
        user_pref, created = UserPreference.objects.get_or_create(user=request.user)
        
        # Check which button was clicked and update preferred gender
        if 'women' in request.POST:
            user_pref.preferred_gender = 'F'
        elif 'men' in request.POST:
            user_pref.preferred_gender = 'M'
        elif 'both' in request.POST:
            user_pref.preferred_gender = 'B'
        
        # Save the updated preference
        user_pref.save()
        
        # Redirect to a success or the same page to prevent resubmission
        return redirect(self.success_url) 
       

class SharedSlidbar(TemplateView):
    template_name="shared/sidebars.html"

