import csv
from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import PersonalInfo
from .forms import PersonalInfoForm

# Create your views here.

@login_required
def home(request):
    return render(request, 'address/home.html')

@login_required
def address(request):
    user = request.user.id
    address_list = PersonalInfo.objects.filter(author__exact=user)
    print (address_list)
    return render(request, 'address/address_book.html', {'address_list': address_list})

@login_required
def add_contact(request):
    if request.method == "POST":
        form = PersonalInfoForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.author_id = request.user.id
            data.save()
        return redirect('address')
    else:
        form = PersonalInfoForm()
    return render(request, 'address/add_address.html', {'form' : form})

@login_required
def edit_contact(request, pk):
    address = get_object_or_404(PersonalInfo, pk=pk)
    if request.method == "POST":
        form = PersonalInfoForm(request.POST, instance=address)
        if form.is_valid():
            data = form.save(commit=False)
            data.author_id = request.user.id
            data.save()
        return redirect('address')
    else:
        form = PersonalInfoForm(instance=address)
    return render(request, 'address/add_address.html', {'form' : form})

@login_required
def delete_contact(request, pk):
    address = PersonalInfo.objects.filter(pk__exact=pk)
    if request.method == "POST":
        address.delete() 
        return redirect('address')
    else:
        return render(request, 'address/delete_address.html', {'address_list': address})

def registration(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('address')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def upload_contact(request):
    if request.method == "POST":
        user = request.user.id
        headers = []
        csv_file = request.FILES["csv_file"]
        file_data_header = csv_file.readline().decode("utf-8")
        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")
        for line in lines:
            data_dict = {}
            field = line.split(",")
            data_dict['first_name'] = field[0]
            data_dict['last_name'] = field[1]
            data_dict['contact_number'] = field[2]
            data_dict['address'] = field[3]
            form = PersonalInfoForm(data_dict)
            if form.is_valid():
                data = form.save(commit=False)
                data.author_id = request.user.id
                data.save()
    return render(request, 'address/upload_address.html')


def export_contact(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=mycontact.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) 
    writer.writerow([
        smart_str(u"First Name"),
        smart_str(u"Last Name"),
        smart_str(u"Address"),
        smart_str(u"Contact Number"),
    ])

    user = request.user.id
    address_list = PersonalInfo.objects.filter(author__exact=user)

    for address in address_list:
        writer.writerow([
            smart_str(address.first_name),
            smart_str(address.last_name),
            smart_str(address.address),
            smart_str(address.contact_number),
        ])
    return response
