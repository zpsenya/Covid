from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.core.mail import EmailMultiAlternatives, EmailMessage
from .forms import *

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

from application.forms import RegisterUserForm, LoginUserForm, AddClientForm
from application.models import Clients


def send_email(request, pk):

    email = Clients.objects.get(pk=pk).email
    mail = EmailMultiAlternatives(subject='Covid Test', body='Your result in attachment',
                                  from_email='zpsenya1@ukr.net', to=[f'{email}'])
    detail = Clients.objects.get(pk=pk)
    data = {
        "Name": detail.name,
        "Surname": detail.surname,
        "Status": detail.is_corona,
        "Email": detail.email,
        "Doctor_ID": detail.id_doctor,
        "Time_Sample": detail.time_of_analyse,
    }
    pdf = render_to_pdf('pdf_template.html', data)
    mail.attach(f'Result_{data["Name"]}_{data["Surname"]}_{datetime.datetime.now()}.pdf', pdf.content)
    mail.send()
    return redirect('clients')


def clients(request):
    doctor_id = request.user
    detail = Clients.objects.filter(id_doctor=doctor_id.id)
    context = {
        "users": doctor_id,
        "clients": detail,
    }

    return render(request, "clients.html", context)


def client_detail(request, pk):
    detail = Clients.objects.get(pk=pk)
    context = {
        'detail': detail,
    }
    return render(request, 'client_detail.html', context)


def client_edit(request, pk):
    detail = Clients.objects.get(pk=pk)

    if request.method == 'POST':
        form = AddClientForm(request.POST, instance=detail)
        if form.is_valid():
            try:
                form.save()
                return redirect('clients')
            except:
                form.add_error(None, 'Errors with add client')

    context = {
        'detail': detail,
        'form': AddClientForm(instance=detail),
    }
    return render(request, 'client_edit.html', context)


def client_delete(request, pk):
    detail = Clients.objects.get(pk=pk)
    detail.delete()
    return redirect('clients')


def index(request):
    return render(request, 'index.html')


def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def user(request):
    return render(request, 'user.html')


def create_client(request):
    if request.method == 'POST':
        form = AddClientForm(request.POST)
        if form.is_valid():
            try:
                Clients.objects.create(**form.cleaned_data)
                return redirect('home')
            except:
                form.add_error(None, 'Errors with add client')

    else:
        form = AddClientForm()
    return render(request, 'create_client.html', {'form': form})


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        doctor = form.save()
        login(self.request, doctor)
        return redirect('home')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'


def logout_user(request):
    logout(request)
    return redirect('login')


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')


class ViewPDF(View):

    def get(self, request, pk, *args, **kwargs):
        detail = Clients.objects.get(pk=pk)
        data = {
            "Name": detail.name,
            "Surname": detail.surname,
            "Status": detail.is_corona,
            "Email": detail.email,
            "Doctor_ID": detail.id_doctor,
            "Time_Sample": detail.time_of_analyse,
        }
        pdf = render_to_pdf('pdf_template.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


class DownloaderPDF(View):
    def get(self, request, pk, *args, **kwargs):
        detail = Clients.objects.get(pk=pk)
        data = {
            "Name": detail.name,
            "Surname": detail.surname,
            "Status": detail.is_corona,
            "Email": detail.email,
            "Doctor_ID": detail.id_doctor,
            "Time_Sample": detail.time_of_analyse,
        }
        pdf = render_to_pdf('pdf_template.html', data)

        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f'Result_{data["Name"]}_{data["Surname"]}_{datetime.datetime.now()}'
        content = f"attachment; filename={filename}"
        response['Content-Disposition'] = content
        return response
