from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.base import View
from django.views.generic import TemplateView
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from .forms import PasswordResetForm, PasswordResetVerifiedForm

from authemail import wrapper

from accounts.models import MyUser
from accounts.serializers import MyUserSerializer




class UserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer

   # @action(detail=False, methods=['post'], url_path='register')
         
         
class SignUpVerifyFE(View):
    def get(self, request, format=None):
        code = request.GET.get('code', '')
        
        account = wrapper.Authemail()
        response = account.signup_verify(code=code)
        
        if 'detail' in response:
            return HttpResponseRedirect(reverse('signup_not_verified_page'))
    
        return HttpResponseRedirect(reverse('signup_verified_page'))
    

class SignUpVerifiedFE(TemplateView):
    template_name = 'signup_succ.html'


class SignUpNotVerifiedFE(TemplateView):
    template_name = 'signup_no_succ.html'    
    
class PasswordResetVerifyFE(View):
    def get(self, request, format=None):
        code = request.GET.get('code', '')

        account = wrapper.Authemail()
        response = account.password_reset_verify(code=code)

        # Handle other error responses from API
        if 'detail' in response:
            return HttpResponseRedirect(
                reverse('password_reset_not_verified_page'))

        request.session['password_reset_code'] = code

        return HttpResponseRedirect(reverse('password_reset_verified_page'))
    
class PasswordResetVerifiedFE(FormView):
    template_name = 'password_reset_verified.html'
    form_class = PasswordResetVerifiedForm
    success_url = reverse_lazy('password_reset_success_page')

    def form_valid(self, form):
        code = self.request.session['password_reset_code']
        password = form.cleaned_data['password']

        account = wrapper.Authemail()
        response = account.password_reset_verified(code=code, password=password)

        # Handle other error responses from API
        if 'detail' in response:
            form.add_error(None, response['detail'])
            return self.form_invalid(form)

        return super(PasswordResetVerifiedFE, self).form_valid(form)
    
class PasswordResetNotVerifiedFE(TemplateView):
    template_name = 'pwreset_no_succ.html'
    
    
class PasswordResetSuccessFrontEnd(TemplateView):
    template_name = 'password_reset_success.html'