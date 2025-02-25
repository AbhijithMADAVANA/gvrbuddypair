# views.py
import django.contrib
from typing import Any
from urllib import request

from django.http import HttpRequest, JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
import razorpay
from django.conf import settings
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from .forms import MatrimonyPaymentForm
from django.contrib import messages
from .models import MatrimonyPayment,MatrimonySubscription
from django.urls import reverse
from django.template.loader import get_template, render_to_string
# from xhtml2pdf import pisa
# from weasyprint import HTML
import tempfile

from matrimony_admin.models import Subscription, SubscriptionINFO

from U_auth.permissions import RedirectNotAuthenticatedUserMixin
from http import HTTPStatus



'''In paymentview have logical issue in plan_type '''


class PaymentView(RedirectNotAuthenticatedUserMixin, FormView):
    template_name = 'matrimony_subscription/Addcard.html'
    form_class = MatrimonyPaymentForm
    success_url = reverse_lazy('payment-success')

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        session_plan = request.session.get('selected_plan', None)
        
        if session_plan:
            context = {
                'plan': session_plan['plan_type'],  
                'amount': session_plan['amount']  
            }
            return self.render_to_response(context)
        else:
            messages.error(request, "No plan selected.")
            return redirect('matrimony_subscription:subscribe')

    def form_valid(self, form):
        amount = int(form.cleaned_data['amount'] * 100)

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        try:
            # Create a new order on Razorpay
            razorpay_order = client.order.create({
                'amount': amount,  # Amount in paise
                'currency': 'INR',
                'payment_capture': '1'  # Auto-capture payment
            })
            print(razorpay_order, "Order created successfully")  # Debug print

            payment = MatrimonyPayment.objects.create(
                user=self.request.user,
                payment_type='razorpay',
                subscription_plan=MatrimonySubscription.objects.get(plan_type=self.request.session['selected_plan']['plan_type']),
                razorpay_order_id=razorpay_order['id'],
                amount=form.cleaned_data['amount'],  # Amount in INR for record
                status='created'
            )

            # Pass the payment details to the frontend
            context = {
                'razorpay_key_id': settings.RAZORPAY_KEY_ID,
                'razorpay_order_id': razorpay_order['id'],
                'amount': amount,  # Amount in paise
                'currency': 'INR',
                'callback_url': self.request.build_absolute_uri(reverse_lazy('matrimony_subscription:payment-callback'))
            }
            return JsonResponse(context)

        except Exception as e:
            print(f"Error creating Razorpay order: {e}")
            return JsonResponse({'error': str(e)}, status=500)



class PaymentCallbackView(RedirectNotAuthenticatedUserMixin, TemplateView):
    template_name = 'matrimony_subscription/Addcard.html'

    def post(self, request, *args, **kwargs):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        # Extract Razorpay payment details from the request
        razorpay_payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        razorpay_signature = request.POST.get('razorpay_signature', '')

        # Verify the payment signature
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }

        payment = MatrimonyPayment.objects.get(razorpay_order_id=razorpay_order_id)

        try:
            # Verify the payment signature
            client.utility.verify_payment_signature(params_dict)
            payment.razorpay_payment_id = razorpay_payment_id
            payment.razorpay_signature = razorpay_signature
            payment.status = 'success'
            payment.save()
            context = {'status': 'Payment Successful'}
            print("Payment success")
        except Exception as e:
            payment.status = 'failed'
            payment.save()
            context = {'status': 'Payment Failed', 'exception': str(e)}
            print("Payment failed")

        return self.render_to_response(self.get_context_data(context))


from weasyprint import HTML
import tempfile

class PaymentDetails(RedirectNotAuthenticatedUserMixin, TemplateView):
    template_name = 'matrimony_subscription/payment_details.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs) 
        # Fetch payment details for the user
        context["payment_details"] = MatrimonyPayment.objects.filter(user=self.request.user).order_by('-created_at')
        return context

    def get(self, request, *args, **kwargs):
        # Check if 'pay_id' is in the URL for PDF download
        pay_id = kwargs.get('pay_id', None)
        
        if pay_id:
            # Fetch specific payment
            payment_details = get_object_or_404(MatrimonyPayment, id=pay_id, user=request.user)

            # Render the HTML template
            html_string = render_to_string('matrimony_subscription/invoice_template.html', {'payment_details': payment_details})

            # Create a temporary file to store the PDF
            with tempfile.NamedTemporaryFile(delete=True) as output_file:
                # Generate the PDF using WeasyPrint
                HTML(string=html_string).write_pdf(output_file.name)

                # Return the PDF as a downloadable response
                response = HttpResponse(output_file.read(), content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
                return response
        
        # Render the payment details template if no 'pay_id' is provided
        return super().get(request, *args, **kwargs)


class SubscriptionView(TemplateView):
    template_name = 'matrimony_subscription/Subscribe.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subscription_details = MatrimonySubscription.objects.filter(status='active').order_by('-created_at')
        context['subscription_details'] = subscription_details
        return context

    def post(self, request, *args, **kwargs):
        plan_type = request.POST.get('plan_type')  # Get the selected plan type
        if plan_type:
            try:
                subscription = MatrimonySubscription.objects.get(plan_type=plan_type)
                # Store the selected plan in session
                request.session['selected_plan'] = {
                    'plan_type': subscription.plan_type,
                    'amount': float(subscription.price),
                    'day_limit': subscription.day_limit
                }
            except MatrimonySubscription.DoesNotExist:
                messages.error(request, "The selected plan does not exist.")
                return redirect('matrimony_subscription:subscribe')

        return redirect('matrimony_subscription:payment')

    
class AddPaymentView(TemplateView):
    template_name='matrimony_subscription/AddPayment.html'


class Invoice(TemplateView):
    template_name = 'matrimony_subscription/invoice_template.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        pay_id = self.request.GET.get('pay_id', None)
        
        try:
            if pay_id:
                payment_details = get_object_or_404(MatrimonyPayment, id=pay_id, user=self.request.user)
            else:
                payment_details = MatrimonyPayment.objects.filter(user=self.request.user).latest('created_at')

            context['payment_details'] = payment_details
        
        except MatrimonyPayment.DoesNotExist:
            context['error'] = "No payment found for this user."

        return context
