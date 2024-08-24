from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import get_user_model, login
from django.contrib import messages
import ghasedakpack

from random import randint

sms = ghasedakpack.Ghasedak('') # فراموش نکنید که از کلید اِی پی آی خودتون در سایت قاصدک استفاده کنید
YOUR_TEMPLATE_NAME_ON_GHASEDAK = '' # فراموش نکنید که اسم تمپلیت خودتون رو بنویسید داخل این استرینگ
good_line_number_for_sending_otp = '30005088'


class ShowHomepage(generic.TemplateView):
    template_name = 'index.html'


class Login(generic.TemplateView):
    otp = ''
    phone_number = ''

    def get(self, request, *args, **kwargs):
        Login.phone_number = request.GET.get('phone_number')
        context = {
            'method': 'get',
        }
        Login.otp = str(randint(100000, 999999))
        answer = sms.verification({'receptor': Login.phone_number, 'linenumber': good_line_number_for_sending_otp,'type': '1', 'template': YOUR_TEMPLATE_NAME_ON_GHASEDAK, 'param1': Login.otp})
        if answer==True:
            return render(request, 'login.html', context)
        else:
            messages.error(request, "مشکلی رخ داده.")
            return redirect('homepage')
    

    def post(self, request, *args, **kwargs):
        sent_otp = request.POST.get('sent_otp')
        if sent_otp==Login.otp:
            user = get_user_model().objects.filter(username=Login.phone_number).first()
            if user:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            else:
                new_user = get_user_model().objects.create(username=Login.phone_number)
                login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('homepage')
        else:
            print('problem')
        context = {
            'method': 'post',
        }
        return render(request, 'login.html', context)
