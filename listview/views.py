from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.db.models import Q
from listview.models import Customer, Base_Email, Login_Details
from django.views import View
import json
from linkedin_api import Linkedin, linkedin
from requests.cookies import cookiejar_from_dict
import smtplib
from email.message import EmailMessage
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from users.models import CustomUser
import csv
from multiprocessing.pool import ThreadPool
import os


# Create your views here.
@login_required
def index(request):
  if request.method == "POST":
    name = request.POST['name']
    try:
      # request.POST['linkedin']:
      linkedin = request.POST['linkedin']
    except:
      linkedin = ""
    try:
      # request.POST['email']:
      email = request.POST['email']
    except:
      email = ""
    try:
      # request.POST['phone']:
      phone = request.POST['phone']
    except:
      phone = ""
    try:
      # request.POST['company']:
      company = request.POST['company']
    except:
      company = ""
    try:
      # request.POST["designation"]:
      designation = request.POST["designation"]
    except:
      designation = ""
    try:
      # request.POST["designation"]:
      current_role = request.POST["current-role"]
    except:
      current_role = ""
    try:
      # request.POST["nature-of-work"]:
      nature_of_work = request.POST.getlist("nature-of-work")
      nature_of_work_string = ', '.join(nature_of_work)
    except:
      nature_of_work_string = ""
    try:
      # request.POST['rating']:
      rating = request.POST['rating']
    except:
      rating = ""
    try:
      # request.POST['connection']:
      connection = request.POST['connection']
    except:
      connection = ""
    try:
      # request.POST['status']:
      status = request.POST['status']
    except:
      status = ""
    try:
      # request.POST['category']:
      category = request.POST.getlist('category')
      category_string = ', '.join(category)
    except:
      category_string = ""
    try:
      # request.POST['connect_type']:
      connect_type = request.POST.getlist('connect_type')
      connect_type_string = ', '.join(connect_type)
    except:
      connect_type_string = ""
    try:
      # request.POST["linkedin-summary"]:
      linkedin_summary = request.POST["linkedin-summary"]
    except:
      linkedin_summary = ""
    print(category)
    ins = Customer(linkedin=linkedin, name=name, company=company, linkedin_title=designation, current_role=current_role, nature_of_work=nature_of_work_string, email=email, phone=phone, category=category_string, rating=rating, connection=connection, status=status, connect_type=connect_type_string, linkedin_summary=linkedin_summary)
    ins.save()
    # return redirect('/')

  allData = Customer.objects.all()
  b_mails = Base_Email.objects.all()
  if request.method == "GET":
    st = request.GET.get("search-name")
    if st!=None:
      allData = Customer.objects.filter(Q(name__icontains = st)|Q(linkedin_title__icontains = st)|Q(linkedin_summary__icontains = st)|Q(company__icontains = st))

  context = {'datas': allData, 'emails': b_mails}
  return render(request, 'listview/base.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='/', redirect_field_name=None)
def exportcsv(request):
  # if request.method == "POST":
  #   print(request.POST)
  #   user_ids = request.POST.getlist('user_ids[]')
  #   print(user_ids)
  #   if(user_ids == []):
  #     return redirect('/')
  #   customers = Customer.objects.filter(id__in = user_ids)
  # else:
  customers = Customer.objects.all()
  print(customers)
  response = HttpResponse(content_type='text/csv')
  response['Content-Disposition'] = 'attachment; filename="customers.csv"'
  writer = csv.writer(response)
  writer.writerow(['Linkedin', 'Name', 'Company', 'Linkedin Title', 'Current Role', 'Nature of work', 'Linkedin Summary', 'E-mail', 'Phone', 'Date', 'Category', 'Rating', 'Connection', 'Status', 'Connect Type'])
  cust = customers.values_list('linkedin', 'name', 'company', 'linkedin_title', 'current_role', 'nature_of_work', 'linkedin_summary', 'email', 'phone', 'date', 'category', 'rating', 'connection', 'status', 'connect_type')
  for i in cust:
    writer.writerow(i)
  print('idk')
  return response



@user_passes_test(lambda u: u.is_superuser, login_url='/', redirect_field_name=None)
@login_required
def example(request):
  return HttpResponse('Welcome to Example.')


@user_passes_test(lambda u: u.is_superuser, login_url='/', redirect_field_name=None)
@login_required
def createUser(request):
  print('route working')
  if request.method == 'POST':
    print(request.POST)
    name = request.POST["name"]
    email = request.POST["email"]
    password = request.POST["password"]
    access_level = request.POST["access-level"]
    new_user = CustomUser.objects.create_user(email=email, username=name, password=password)
    if access_level == 'Admin':
      new_user.is_superuser = 1
      new_user.is_staff = 1
    else:
      new_user.is_superuser = 0
      new_user.is_staff = 0

    new_user.save()
    print('new user created')
  return redirect('/')


def signup(request):
  return HttpResponse("This is signup")





class Delete(View):
  @method_decorator(login_required)
  @method_decorator(user_passes_test(lambda u: u.is_superuser, login_url='/', redirect_field_name=None))
  def post(self, request):
    if request.method == "POST":
      data = request.POST
      print('inside delete')
      record = Customer.objects.get(id=data['name'])
      record.delete()
    return redirect('/')



class Update(View):
  @method_decorator(login_required)
  @method_decorator(user_passes_test(lambda u: u.is_superuser, login_url='/', redirect_field_name=None))
  def post(self, request, id):
    pi = Customer.objects.get(pk=id)
    Customer.objects.filter(pk=id).update(name='some value')
    return HttpResponseRedirect('/')


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='/', redirect_field_name=None)
def delete_user(request):
  if request.method == "POST":
    data = request.POST
    user = CustomUser.objects.get(email=data["name"])
    user.delete()
  return redirect('/users/')


@login_required
def massmail(request):
    if request.method == 'POST':
        sender = request.POST["sender"]
        # sender = 'frazorf302@gmail.com'
        recipients = request.POST["recipient"]
        sender_details = Base_Email.objects.get(b_email = sender)
        msg = EmailMessage()
        msg['Subject'] = request.POST["subject"]
        msg['From'] = sender_details.b_email
        # msg['Bcc'] = ', '.join(recipients) # all the contacts separated by a comma
        msg['Bcc'] = recipients
        msg.set_content(request.POST["body"])
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_details.b_email, sender_details.b_pass)
            smtp.send_message(msg)
        print(sender_details.b_name)
    return redirect('/')


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='/', redirect_field_name=None)
def users(request):
    param = request.GET.get('search-user')
    if param is not None:
      allUsers = CustomUser.objects.filter(username__icontains=param)
    else:
      allUsers = CustomUser.objects.all()
    context = {'users': allUsers}
    return render(request, 'listview/users.html', context)


@login_required
def autofill(request):
  if request.method == 'GET':
    print('received data')
    print(request.GET['input_value'])
    post_data = request.GET['input_value']
    user_id = post_data.split('/')[4]
    scraped_details = get_linkedin_data(user_id)
    jsonified_details = json.dumps(scraped_details)
    print(jsonified_details)
    return HttpResponse(jsonified_details, content_type="text/json")
    # return redirect('/')
  return HttpResponse('Error!')



def get_linkedin_data(user_id):
    # Authenticate using any Linkedin account credentials
    cookies = cookiejar_from_dict(
        {
            "liap": "true",
            "li_at": 'AQEDATiU6vsCs2AqAAABfY6ajFQAAAF9sqcQVE4AOmhPSIJiVzoQODl2-6GPb_Evoww4DnE3VJVuR-MW5Hn36YpsBNBegEQInAAJnYaQEj52bLjzOYlY-jOtHgBGWdu791dFnSaHpC2TmkbXDIdLX8Mu',
            "JSESSIONID": "ajax:1921697886900276652",
        }
    )
    # api = Linkedin("ab1jidge@gmail.com", "Asj@1998")
    api = Linkedin("", "", cookies=cookies)
    # GET a profile
    profile = api.get_profile(user_id)
    # Extract details
    data = {}
    # data['name'] = profile['firstName'] +' '+ profile['lastName']
    # data['headline'] = profile['headline']
    # data['location'] = profile['geoLocationName']

    try:
      data['summary'] = profile['summary']

    except:
      data['summary'] = ''

    try:
        data['name'] = profile['firstName'] +' '+ profile['lastName']
    except:
        data['name'] = ""

    try:
        data['headline'] = profile['headline']
    except:
        data['headline'] = ""

    try:
        data['location'] = profile['geoLocationName']
    except:
        data['location'] = ""


    experiences = profile['experience']
    experience_data = []
    for experience in experiences:
        temp_dict = {}
        if 'locationName' in experience:
            temp_dict['locationName'] = experience['locationName'],
        else:
            print('locationName not found')
        if 'companyName' in experience:
            temp_dict['companyName'] = experience['companyName'],
        else:
            print('companyName not found')
        if 'title' in experience:
            temp_dict['title'] = experience['title'],
        else:
            print('title not found')
        experience_data.append(temp_dict)
    try:
        data['current_company'] = experience_data[0]['companyName'][0]
        data['current_role'] = experience_data[0]['title'][0]
    except:
        data['current_company'] = ''
        data['current_role'] = ''
    return(data)





@login_required
def update_linkedin_data(request):
  if request.method == 'POST':
    incoming_data = request.POST.getlist('linkedin_input[]')
    print(incoming_data)

    # ['6', 'https://www.linkedin.com/in/rasesh-seth/', 'Rasesh', 'Nextyn', "Nextyn (We're Hiring!)", 'Director - Business Development']
    # each user has length = 6
    user_data = []
    for i in range(0, len(incoming_data), 6):
      user = incoming_data[i:i + 6]
      print('user: ', user)
      user_dict = {
        'user_id': user[0],
        'linkedin_id': user[1],
        'name': user[2],
        'current_company': user[3],
        'headline': user[4],
        'current_role': user[5]
      }
      user_data.append(user_dict)
      # print(incoming_data[i:i + 6])

    pool = ThreadPool(25)
    updated_data = pool.map(get_linkedin_updates, user_data)

    # Extract Logs
    update_logs = []
    for updated_user in updated_data:
        if updated_user['change_flag'] == True:
            for log in updated_user['logs']:
                update_logs.append(log)


    print(update_logs)

  # return update_logs
  return HttpResponse(json.dumps({'log_data': update_logs}),content_type='application/json; charset=utf8')




def get_linkedin_updates(user):
    print(user)
    cookies = cookiejar_from_dict(
        {
            "liap": "true",
            "li_at": 'AQEDATiU6vsCs2AqAAABfY6ajFQAAAF9sqcQVE4AOmhPSIJiVzoQODl2-6GPb_Evoww4DnE3VJVuR-MW5Hn36YpsBNBegEQInAAJnYaQEj52bLjzOYlY-jOtHgBGWdu791dFnSaHpC2TmkbXDIdLX8Mu',
            "JSESSIONID": "ajax:1921697886900276652",
        }
    )
    # api = Linkedin("ab1jidge@gmail.com", "Asj@1998")
    api = Linkedin("", "", cookies=cookies)
    profile_data = api.get_profile(user['linkedin_id'].split('/')[4])
    # print(profile_data)

    experiences = profile_data['experience']
    experience_data = []

    user['change_flag'] = False
    user['logs'] = []

    for experience in experiences:
        temp_dict = {}
        if 'locationName' in experience:
            temp_dict['locationName'] = experience['locationName'],
        else:
            print('locationName not found')

        if 'companyName' in experience:
            temp_dict['companyName'] = experience['companyName'],
        else:
            print('companyName not found')

        if 'title' in experience:
            temp_dict['title'] = experience['title'],
        else:
            print('title not found')
        experience_data.append(temp_dict)


    try:
       summary = profile_data['summary']
    except:
        summary = ''

    try:
        if profile_data['headline'] != user['headline']:
            # user['logs'] = user['logs'] + '\n '+ user['name'] + ' headline changed from '+ user['headline'] +' to '+ profile_data['headline']
            user['logs'].append(user['name'] + ' headline changed from '+ user['headline'] +' to '+ profile_data['headline'])
            user['headline'] = profile_data['headline']
            # update headline in database
            user['change_flag'] = True
    except Exception as e:
        print(e)
        user['headline'] = ""

    try:
        if experience_data[0]['companyName'][0] != user['current_company']:
            # user['logs'] = user['logs'] + '\n '+ user['name'] + ' current company changed from '+ user['current_company'] +' to '+ experience_data[0]['companyName'][0]
            user['logs'].append(user['name'] + ' current company changed from '+ user['current_company'] +' to '+ experience_data[0]['companyName'][0])
            user['current_company'] = experience_data[0]['companyName'][0]
            # update headline in database
            user['change_flag'] = True
    except Exception as e:
        print(e)
        user['current_company'] = ''

    try:
        if experience_data[0]['title'][0] != user['current_role']:
            # user['logs'] = user['logs'] + '\n '+ user['name'] + ' current company changed from '+ user['current_role'] +' to '+ experience_data[0]['title'][0]
            user['logs'].append(user['name'] + ' title changed from '+ user['current_role'] +' to '+ experience_data[0]['title'][0])
            user['current_role'] = experience_data[0]['title'][0]
            # update headline in database
            user['change_flag'] = True
    except Exception as e:
        print(e)
        user['current_role'] = ''

    # Update Database
    if user['change_flag'] == True:
      Customer.objects.filter(pk=user['user_id']).update(company = user['current_company'],linkedin_title=user['headline'],current_role=user['current_role'],linkedin_summary=summary)

    # print(user)
    return user



@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='/', redirect_field_name=None)
def editRecord(request):
  print('edit record working')
  if request.method == 'POST':
    print(request.POST)
    id = request.POST["edit-id"]
    customer = Customer.objects.get(pk=id)
    linkedin = request.POST["edit-linkedin"]
    customer.linkedin = linkedin
    name = request.POST["edit-name"]
    customer.name = name
    email = request.POST["edit-email"]
    customer.email = email
    phone = request.POST["edit-phone"]
    customer.phone = phone
    company = request.POST["edit-company"]
    customer.company = company
    designation = request.POST["edit-designation"]
    customer.linkedin_title = designation
    current_role = request.POST["edit-current-role"]
    customer.current_role = current_role
    nature_of_work = request.POST.getlist("edit-nature-of-work")
    if nature_of_work != []:
      nature_of_work_string = ', '.join(nature_of_work)
      customer.nature_of_work = nature_of_work_string
    rating = request.POST["edit-rating"]
    customer.rating = rating
    connected_by = request.POST["edit-connected-by"]
    customer.connection = connected_by
    try:
      business_status = request.POST["edit-business-status"]
      customer.status = business_status
    except:
      pass
    category = request.POST.getlist("edit-category")
    if category != []:
      category_string = ', '.join(category)
      customer.category = category_string
    connect_type = request.POST.getlist("edit-connect-type")
    if connect_type != []:
      connect_type_string = ', '.join(connect_type)
      customer.connect_type = connect_type_string
    linkedin_summary = request.POST["edit-linkedin-summary"]
    customer.linkedin_summary = linkedin_summary

    customer.save()
  # Customer.objects.filter(pk=id).update(id = id, linkedin = linkedin, name = name, company = company,linkedin_title=designation,current_role=current_role,nature_of_work=nature_of_work_string,email = email,phone = phone,connection = connected_by,rating = rating, connect_type = connect_type_string, category=category_string, status=business_status, linkedin_summary=linkedin_summary)
  # print('-------------------')

  return redirect('/')


@login_required
def autocomplete(request):
  query_original = request.GET.get('term')
  qs = Customer.objects.filter(name__icontains = query_original)
  titles = []
  titles += [ x.name for x in qs ]
  # return render(request, 'listview/base.html')
  return JsonResponse(titles, safe = False)


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='/', redirect_field_name=None)
def autocomplete_user(request):
  query_original = request.GET.get('term')
  print(query_original)
  qs = CustomUser.objects.filter(username__icontains = query_original)
  titles = []
  titles += [ x.username for x in qs ]
  # return render(request, 'listview/base.html')
  return JsonResponse(titles, safe = False)



@login_required
def filter(request):
  if request.method == "POST":
    print(request.POST)
    category = request.POST.getlist("category")
    rating = request.POST["rating"]
    connected_by = request.POST["connected_by"]
    b_status = request.POST.getlist("b_status")
    connect_type = request.POST.getlist('connect_type')
    nature_of_work = request.POST.getlist('nature-of-work')

    query_condition = Q(rating__gte=rating)

    if connected_by:
      query_condition &= Q(connection__icontains=connected_by)

    if b_status:
      query_condition &= Q(status__in=b_status)

    if category:
      category_condition = Q(category__icontains=category[0])
      for i in category[1:]:
        category_condition |= Q(category__icontains=i)
      query_condition &= category_condition

    if nature_of_work:
      nature_of_work_condition = Q(nature_of_work__icontains=nature_of_work[0])
      for i in nature_of_work[1:]:
        nature_of_work_condition |= Q(nature_of_work__icontains=i)
      query_condition &= nature_of_work_condition

    if connect_type:
      connect_type_condition = Q(connect_type__icontains=connect_type[0])
      for i in connect_type[1:]:
        connect_type_condition |= Q(connect_type__icontains=i)
      query_condition &= connect_type_condition


    print(query_condition)
    filtered = Customer.objects.filter(query_condition)
    b_mail_data = Base_Email.objects.all()
    print(filtered)
    print(category)
    print(rating)
    print(connected_by)
    print(b_status)
    print(connect_type)
  context = {'datas': filtered, 'emails': b_mail_data}
  return render(request, 'listview/base.html', context)