import csv
from django.utils.encoding import smart_str
from ..models import PersonalInfo
from ..forms import PersonalInfoForm

def write_personal_csv(response, request):
    writer = csv.writer(response, csv.excel)
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


def save_contact(csv_file, request):
    user = request.user.id
    header_list = csv_file.readline().decode("utf-8").rstrip().split(",")
    headers = {n: header_list.index(n) for n in header_list}

    file_data = csv_file.read().decode("utf-8")
    lines = file_data.split("\n")

    for line in lines:
        data_dict = {}
        field = line.split(",")
        data_dict['first_name'] = field[headers['FirstName']]
        data_dict['last_name'] = field[headers['LastName']]
        data_dict['contact_number'] = field[headers['ContactNo']]
        data_dict['address'] = field[headers['Address']]

        form = PersonalInfoForm(data_dict)
        if form.is_valid():
            data = form.save(commit=False)
            data.author_id = request.user.id
            data.save()
