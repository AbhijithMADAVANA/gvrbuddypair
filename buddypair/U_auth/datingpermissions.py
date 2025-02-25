from django.contrib import messages
import U_auth.permissions
import django.contrib
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from U_auth.models import (AdditionalDetails, costume_user, Job_Details, OTP, Relationship_Goals,
    UserPersonalDetails)

#...................................custom permission class...................................

'''Explanation:
1) test_func: This method checks if the user is authenticated. 
If they are, it returns False, preventing access to the view.

2) handle_no_permission: This method defines what happens if the test fails. 
In this case, it redirects the authenticated user to the home page (or any page you choose).

3) Usage in Views: The RedirectAuthenticatedUserMixin is applied to both the login and signup views, 
preventing logged-in users from accessing these pages.
'''

# class RedirectAuthenticatedUserMixin(UserPassesTestMixin):
#     def test_func(self):
#         # This will return False if the user is authenticated, blocking access to the view.
#         return not self.request.user.is_authenticated and self.request.is_completed 

#     def handle_no_permission(self):
#         # If the user is authenticated and tries to access the page like login or signup, redirect them
#         return redirect(reverse_lazy('home'))  # Redirect to home page or any other page

class RedirectAuthenticatedUserMixin(UserPassesTestMixin):
    def test_func(self):
        # Ensure the user is authenticated and has the `is_completed` attribute set to True
        user = self.request.user
        print(getattr(user, 'is_completed', False), user)
        return not (user.is_authenticated and getattr(user, 'is_completed', False))

    def handle_no_permission(self):
        # Return False (i.e., redirect) only if the user is authenticated and `is_completed` is True
        return redirect(reverse_lazy('matrimony_home:home'))  # Redirect to home page or any other page    

class RedirectNotAuthenticatedUserMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        # This will return True if the user is not authenticated, blocking access to the view.
        return (user.is_authenticated and getattr(user, 'is_completed', False))
    
    def handle_no_permission(self):
        # If the user is not authenticated and tries to access the authendication need pages like home or signup, redirect them
        print(self.request.user,"in per..")

        return redirect(reverse_lazy('u_auth:auth_page'))

class check_permissions:
    def __init__(self, get_response, user_email):
        self.get_response = get_response
        self.user_email = user_email
        self.user_obj = None
        self.model_dict = {}

        self.db_models_to_check = [(UserPersonalDetails, 'show_personaldetails_modal'), (Job_Details, 'show_jobdetails_modal'), (Relationship_Goals, 'show_relationmodel_modal'), (AdditionalDetails, 'show_additionaldetails_modal')]
        

    def check_user_authendicated(self):
        return self.get_response.user.is_authenticated


    def check_userverified(self):
        try:
            self.user_email = costume_user.objects.get(email=self.user_email)
            if self.user_email.is_verified:
                return True
            return False
        except OTP.DoesNotExist:
            return False

    def get_model(self):
        
        if not self.check_userverified():

            self.model_dict['status'] = False
            self.model_dict['model'] = 'OTP'
            self.model_dict['message'] = "User already exists. Please check your email for OTP."
            return self.model_dict
                
        for model in self.db_models_to_check:
                    
            if self.check_user_authendicated():
                # if not model[0].objects.filter(user=self.user_email).exists():
                if self.get_response.session.get('check_type', None):
                    self.model_dict['status'] = False
                    self.model_dict['show_relationship_model'] = True
                    return self.model_dict
                        
                if not model[0].objects.filter(user=self.user_email).exists():
                    self.model_dict['status'] = False
                    self.model_dict[model[1]] = True
                    return self.model_dict
            else:
                # messages.error(self.get_response, "user not audenticated...!!")
                self.model_dict['status'] = False
                self.model_dict['model'] = 'OTP'
                self.model_dict['message'] = 'Please verify your email first'
                return self.model_dict
                    

        # If all models exist
        return None
            
           