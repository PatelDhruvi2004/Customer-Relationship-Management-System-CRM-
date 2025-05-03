from django.shortcuts import get_object_or_404, render, redirect

from .models import *

from datetime import date

from django.db.models import Count

import json

from django.db.models.functions import TruncMonth

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.core.mail import EmailMessage


# Create your views here.


# - Homepage 

def Home(request):
    
    user_exists = False
    if request.user.is_authenticated:
        user_exists = User.objects.filter(id=request.user.id).exists()
    
    return render(request, 'index.html', {'user_exists': user_exists})


# - Register a user

def Register(request):
    if request.method == "POST":
        myuser = User()
        myuser.name = request.POST.get("uname")
        myuser.email = request.POST.get("uemail")
        myuser.password = request.POST.get("upwd1")
        cpass = request.POST.get("upwd2")
        
        if cpass == myuser.password:  
            already = User.objects.filter(email = request.POST['uemail'])
            if already:
                return render(request, "register.html")
            else: 
                myuser.save()
                return redirect("login")
        else:
            return render(request, "register.html")
    return render(request, 'register.html')

# - Login a user

def Login(request):
    
    if request.method == "POST":
        uname = request.POST.get("username")
        upass = request.POST.get("upassword")

        try:
            admin = User.objects.get(email=uname)  # Get the admin by email
            if upass ==  admin.password:  # Secure password verification
                request.session['admin_id'] = admin.id  # Store session data
                return redirect("dashboard")
            else:
                return render(request, "login.html", {"error": "Invalid credentials"})
        except User.DoesNotExist:
            return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, 'login.html')

# ------------------------------------------customer--------------------------------------------

# - customer list

def Customer_list(request):
    
    cust = Customer.objects.all()
    c={"cust":cust}
    
    return render(request, 'customer_list.html',c)
                  

# - create customer

def Create_customer(request):
    
    if request.method == "POST":
        cust = Customer()
        cust.first_name = request.POST.get("cfname")
        cust.last_name = request.POST.get("clname")
        cust.email = request.POST.get("cemail")
        cust.phone = request.POST.get("cphone")
        cust.address = request.POST.get("cadd")
        cust.city = request.POST.get("ccity")
        cust.country = request.POST.get("ccountry")
        cust.item = request.POST.get("citem")
        cust.date = request.POST.get("cdate") or date.today()
        cust.save()
        return redirect("customer_list")
        
    return render(request, 'create_customer.html')

# - view customer

def View_customer(request, id):
    cust_view = get_object_or_404(Customer, id=id)
    return render(request, 'view_customer.html', {'cust_view': cust_view})

# - Update customer

def Update_customer(request, id):
    cust_update = get_object_or_404(Customer, id=id)
    
    if request.method == "POST":
        cust_update.first_name = request.POST.get('first_name', cust_update.first_name)
        cust_update.last_name = request.POST.get('last_name', cust_update.last_name)
        cust_update.email = request.POST.get('email', cust_update.email)
        cust_update.phone = request.POST.get('phone', cust_update.phone)
        cust_update.address = request.POST.get('address', cust_update.address)
        cust_update.city = request.POST.get('city', cust_update.city)
        cust_update.country = request.POST.get('country', cust_update.country)
        cust_update.item = request.POST.get('item', cust_update.item)
        cust_update.save()
        
        return redirect('view_customer', id=cust_update.id)

    return render(request, 'update_customer.html', {'cust_update': cust_update})


# - Delete customer

def Delete_customer(request, id):
    cust_delete = get_object_or_404(Customer, id=id)
    cust_delete.delete()
    return redirect('customer_list')


# - customer report

def Customer_report(request):
    
    direct_customers = Customer.objects.filter(from_lead=False).count()
    lead_customers = Customer.objects.filter(from_lead=True).count()
    
    # Group customers by country
    country_data = (
        Customer.objects.values('country')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    country_labels = [data['country'] for data in country_data]
    country_values = [data['count'] for data in country_data]

    # Get customer joining trends (Month-wise)
    month_data = (
        Customer.objects.annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    month_labels = [entry['month'].strftime('%b %Y') for entry in month_data]
    month_counts = [entry['count'] for entry in month_data]

    # Fetch last 10 created customers
    last_customers = Customer.objects.order_by('-date')[:10]

    context = {
        'country_labels': json.dumps(country_labels),
        'country_values': json.dumps(country_values),
        'month_labels': json.dumps(month_labels),
        'month_data': json.dumps(month_counts),
        'last_customers': last_customers,
        'direct_customers': direct_customers,
        'lead_customers': lead_customers,
    }

    return render(request, 'customer_report.html', context)


# ------------------------------------------lead--------------------------------------------

# - lead list

def Lead_list(request):
    
    lead = Lead.objects.all()
    l={"lead":lead}
    
    return render(request, 'lead_list.html',l)

# - create lead

def Create_lead(request):
    users = User.objects.all()
    
    if request.method == "POST":
        lead = Lead()
        lead.first_name = request.POST.get("lfname")
        lead.last_name = request.POST.get("llname")
        lead.email = request.POST.get("lemail")
        lead.phone = request.POST.get("lphone")
        lead.address = request.POST.get("ladd")
        lead.city = request.POST.get("lcity")
        lead.country = request.POST.get("lcountry")
        lead.item = request.POST.get("litem")
        lead.source = request.POST.get("source")
        lead.status = request.POST.get("status")
        lead.lead_owner = User.objects.get(id = request.POST.get("lead_owner"))
        lead.lead_date = request.POST.get("ldate") or date.today()
        lead.save()
        return redirect("lead_list")
    
    return render(request, 'create_lead.html',{"users":users})

# - view lead

def View_lead(request, id):
    lead_view = get_object_or_404(Lead, id=id)
    return render(request, 'view_lead.html', {'lead_view': lead_view})

# - Update lead

def Update_lead(request, id):
    users = User.objects.all()
    lead_update = get_object_or_404(Lead, id=id)
    
    if request.method == "POST":
        lead_update.first_name = request.POST.get('first_name', lead_update.first_name)
        lead_update.last_name = request.POST.get('last_name', lead_update.last_name)
        lead_update.email = request.POST.get('email', lead_update.email)
        lead_update.phone = request.POST.get('phone', lead_update.phone)
        lead_update.address = request.POST.get('address', lead_update.address)
        lead_update.city = request.POST.get('city', lead_update.city)
        lead_update.country = request.POST.get('country', lead_update.country)
        lead_update.item = request.POST.get('item', lead_update.item)
        lead_update.source = request.POST.get('source', lead_update.source)
        lead_update.status = request.POST.get('status', lead_update.status)
        lead_update.lead_owner = User.objects.get(id = request.POST.get("lead_owner"))
       
        lead_update.save()
        
        return redirect('view_lead', id=lead_update.id)

    return render(request, 'update_lead.html', {'lead_update': lead_update, 'users':users})


# - Delete lead

def Delete_lead(request, id):
    lead_delete = get_object_or_404(Lead, id=id)
    lead_delete.delete()
    return redirect('lead_list')


# - Convert lead to customer

def Convert_lead_to_customer(request, id):
    # Get the lead object
    lead = get_object_or_404(Lead, id=id)

    # Create a new Customer object with lead data
    customer = Customer(
        first_name=lead.first_name,
        last_name=lead.last_name,
        email=lead.email,
        phone=lead.phone,
        address=lead.address,
        city=lead.city,
        country=lead.country,
        item=lead.item,
        date=date.today(),
        from_lead=True  # Mark as converted from a lead
    )
    
    # Save the new customer in the database
    customer.save()

    # Delete the lead after conversion
    lead.delete()

    # Redirect to customer list
    return redirect('customer_list')


# -  lead report 

def Lead_report(request):
    total_leads = Lead.objects.count()
    converted_leads = Customer.objects.count()
    conversion_rate = round((converted_leads / total_leads) * 100, 2) if total_leads > 0 else 0

    # Lead Status Breakdown
    lead_status_counts = Lead.objects.values('status').annotate(count=Count('status'))
    lead_status_labels = [entry['status'] for entry in lead_status_counts]
    lead_status_data = [entry['count'] for entry in lead_status_counts]

    # Lead Source Analysis
    lead_source_counts = Lead.objects.values('source').annotate(count=Count('source'))
    lead_source_labels = [entry['source'] for entry in lead_source_counts]
    lead_source_data = [entry['count'] for entry in lead_source_counts]

    # Get last 10 created leads
    latest_leads = Lead.objects.order_by('-id')[:10]

    context = {
        'conversion_rate': conversion_rate,
        'lead_status_labels': lead_status_labels,
        'lead_status_data': lead_status_data,
        'lead_source_labels': lead_source_labels,
        'lead_source_data': lead_source_data,
        'latest_leads': latest_leads,
    }

    return render(request, 'lead_report.html', context)


# ------------------------------------------settinds--------------------------------------------

def Create_Email_group(request):
    # Fetch all leads and customers
    leads = Lead.objects.all()
    customers = Customer.objects.all()

    # Get filter values from request
    type_filter = request.GET.get('type', 'all')
    status_filter = request.GET.get('status', 'all')

    # Apply type filter
    if type_filter == 'customer':
        leads = Lead.objects.none()
    elif type_filter == 'lead':
        customers = Customer.objects.none()

    # Apply status filter
    if status_filter != 'all':
        leads = leads.filter(status=status_filter)

    # Combine leads and customers into a list
    email_list = [
        {'name': f"{lead.first_name} {lead.last_name}", 'type': 'Lead', 'status': lead.status, 'email': lead.email}
        for lead in leads
    ] + [
        {'name': f"{customer.first_name} {customer.last_name}", 'type': 'Customer', 'status': 'Customer', 'email': customer.email}
        for customer in customers
    ]

    # Sort by name (ascending order)
    email_list = sorted(email_list, key=lambda x: x['name'])
    
    if request.method == "POST":
        group_name = request.POST.get("group_name")
        purpose = request.POST.get("purpose")
        selected_members_json = request.POST.get("selected_members", "[]")

        # Convert JSON string back to a Python list
        selected_members = json.loads(selected_members_json)

        # Save the email group
        email_group = EmailGroup.objects.create(group_name=group_name, purpose=purpose)

        # Save selected members
        for member in selected_members:
            EmailGroupMember.objects.create(
                email_group=email_group,
                name=member["name"],
                type=member["type"],
                status=member["status"],
                email=member["email"]
            )

        return redirect("email_group_list")  # Redirect to group list page

    # If GET request, fetch all leads and customers
    leads = Lead.objects.all()
    customers = Customer.objects.all()

    email_list = [
        {'name': f"{lead.first_name} {lead.last_name}", 'type': 'Lead', 'status': lead.status, 'email': lead.email}
        for lead in leads
    ] + [
        {'name': f"{customer.first_name} {customer.last_name}", 'type': 'Customer', 'status': 'Customer', 'email': customer.email}
        for customer in customers
    ]

    return render(request, "create_email_group.html", {"email_list": email_list})


def Email_group_list(request):
    email_groups = EmailGroup.objects.all().order_by('-created_at')  # Get all groups sorted by latest created
    return render(request, 'email_group_list.html', {'email_groups': email_groups})

def View_email_group(request, group_id):
    # Ensure the email group exists
    email_group = get_object_or_404(EmailGroup, id=group_id)

    # Fetch members of the email group
    members = EmailGroupMember.objects.filter(email_group=email_group)

    # Render the template with data
    return render(request, "view_email_group.html", {"email_group": email_group, "members": members})



def Letterhead(request):
    if request.method == 'POST':
        from_email = request.POST.get('from_email')
        to_email_group_id = request.POST.get('to_email')  # Get selected email group
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        attachments = request.FILES.getlist('attachments')  # Get multiple files

        try:
            # Fetch all email addresses from the selected group
            email_group = EmailGroup.objects.get(id=to_email_group_id)
            recipients = list(email_group.members.values_list('email', flat=True))

            # Create email message
            email = EmailMessage(subject, body, from_email, recipients)

            # Attach files
            for attachment in attachments:
                email.attach(attachment.name, attachment.read(), attachment.content_type)

            email.send()
            
             # Save email history in the database
            email_history = EmailHistory.objects.create(
                group=email_group,
                subject=subject,
            )

            messages.success(request, "Email sent successfully!")  # Success message
            return redirect('letterhead')  # Redirect to refresh the form

        except Exception as e:
            messages.error(request, f"Error sending email: {str(e)}")  # Error message
            return redirect('letterhead')

    email_groups = EmailGroup.objects.all()
    return render(request, 'letterhead.html', {'email_groups': email_groups})



def Email_history(request):
    email_groups = EmailGroup.objects.all()  # Fetch all email groups for filter dropdown
    selected_group = request.GET.get('group_name', 'all')  # Get the selected group from request

    # Fetch email history based on the selected group
    if selected_group != 'all':
        email_history = EmailHistory.objects.filter(group__group_name=selected_group)
    else:
        email_history = EmailHistory.objects.all()

    context = {
        'email_groups': email_groups,  # For the filter dropdown
        'email_history': email_history,  # Filtered email history
        'selected_group': selected_group  # Preserve the selected filter
    }
    return render(request, 'email_history.html', context)

# ------------------------------------------dashboard--------------------------------------------

# - dashboard

def Dashboard(request):
     # Total counts
    total_customers = Customer.objects.count()
    total_leads = Lead.objects.count()

    # Incoming Leads - Grouped by Month
    lead_data = (
        Lead.objects.annotate(month=TruncMonth("lead_date"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )
    lead_months = [entry["month"].strftime("%Y-%m") for entry in lead_data]
    lead_counts = [entry["count"] for entry in lead_data]

    # Opportunity Trends - Only Leads with Status 'Opportunity' (Grouped by Month)
    opportunity_data = (
        Lead.objects.filter(status="Opportunity")
        .annotate(month=TruncMonth("lead_date"))  # Use lead_date for month tracking
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )
    opportunity_months = [entry["month"].strftime("%Y-%m") for entry in opportunity_data]
    opportunity_counts = [entry["count"] for entry in opportunity_data]

   # Item Demand - Count occurrences of each item in the Customer model
    item_demand_data = (
        Customer.objects.values("item")
        .annotate(count=Count("id"))
        .order_by("-count")  # Sort by highest demand
    )
    item_names = [entry["item"] for entry in item_demand_data]
    item_counts = [entry["count"] for entry in item_demand_data]

    context = {
        "total_customers": total_customers,
        "total_leads": total_leads,
        "lead_months": json.dumps(lead_months),
        "lead_counts": json.dumps(lead_counts),
        "opportunity_months": json.dumps(opportunity_months),
        "opportunity_counts": json.dumps(opportunity_counts),
        "item_names": json.dumps(item_names),
        "item_counts": json.dumps(item_counts),
    }

    return render(request, "dashboard.html", context)


# - User logout

def Logout(request):
    
    return redirect("login")