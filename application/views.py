
from io import BytesIO

from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from xhtml2pdf import pisa

from .forms import *
from .utils import qr_code_generation


def client_send_email_view(request, pk):

    email = Client.objects.get(pk=pk).email
    mail = EmailMultiAlternatives(subject='Covid Test', body='Your result in attachment',
                                  from_email='zpsenya1@ukr.net', to=[f'{email}'])
    detail = Client.objects.get(pk=pk)
    data = {
        "Name": detail.name,
        "Surname": detail.surname,
        "Status": detail.is_corona,
        "Email": detail.email,
        "Doctor_ID": detail.doctor_id,
        "Time_Sample": detail.time_of_analyse,
        "QR_Code": qr_code_generation(detail.name, detail.surname)
    }
    pdf = render_to_pdf('pdf_template.html', data)
    mail.attach(f'Result_{data["Name"]}_{data["Surname"]}_{datetime.datetime.now()}.pdf', pdf.content)
    mail.send()
    return redirect('clients')


def client_list_page_view(request):
    doctor_id = request.user
    detail = Client.objects.filter(doctor_id=doctor_id.id)
    context = {
        "users": doctor_id,
        "clients": detail,
    }

    return render(request, "clients.html", context)


def client_detail_page_view(request, pk):
    detail = Client.objects.get(pk=pk)
    context = {
        'detail': detail,
    }
    return render(request, 'client_detail.html', context)


def client_edit(request, pk):
    detail = Client.objects.get(pk=pk)

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


def client_delete_view(request, pk):
    detail = Client.objects.get(pk=pk)
    detail.delete()
    return redirect('clients')


def index(request):
    return render(request, 'index.html')


def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def user_page_view(request):
    return render(request, 'user.html')


def client_create_form_view(request):

    if request.method == 'POST':
        form = AddClientForm(request.POST)
        if form.is_valid():
            try:
                Client.objects.create(**form.cleaned_data)
                return redirect('home')
            except:
                form.add_error(None, 'Errors with add client')

    else:
        form = AddClientForm()

    context = {
        'form': form,
    }
    return render(request, 'create_client.html', context)


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


def user_logout_view(request):
    logout(request)
    return redirect('login')


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')


class ViewPDF(View):
    @staticmethod
    def get(request, pk, *args, **kwargs):
        detail = Client.objects.get(pk=pk)
        data = {
            "Name": detail.name,
            "Surname": detail.surname,
            "Status": detail.is_corona,
            "Email": detail.email,
            "Doctor_ID": detail.doctor_id,
            "Time_Sample": detail.time_of_analyse,
            "QR_Code": qr_code_generation(detail.name, detail.surname)
        }
        pdf = render_to_pdf('pdf_template.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


class DownloadPDF(View):
    @staticmethod
    def get(request, pk, *args, **kwargs):
        detail = Client.objects.get(pk=pk)
        data = {
            "Name": detail.name,
            "Surname": detail.surname,
            "Status": detail.is_corona,
            "Email": detail.email,
            "Doctor_ID": detail.doctor_id,
            "Time_Sample": detail.time_of_analyse,
            "QR_Code": qr_code_generation(detail.name, detail.surname)
        }
        pdf = render_to_pdf('pdf_template.html', data)

        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f'Result_{data["Name"]}_{data["Surname"]}_{datetime.datetime.now()}'
        content = f"attachment; filename={filename}"
        response['Content-Disposition'] = content
        return response



