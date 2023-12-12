from django.shortcuts import render, redirect
from .forms import UpdateRecordForm, CreateRecordForm
from django.contrib.auth.decorators import login_required


from django.contrib.auth import logout as auth_logout
from . models import Record

from django.contrib import messages

#Home page

def home(request):

    return render(request, 'webapp/index.html')


# Dashboard

def dashboard(request):



    my_records = Record.objects.all()

    context = {'records': my_records}


    return render(request, 'webapp/dashboard.html', context=context)


def create_record(request):
    form = CreateRecordForm()

    if request.method == "POST":
        form = CreateRecordForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['Name']
            email = form.cleaned_data['Email']

            
            existing_record_name = Record.objects.filter(Name=name).first()
            existing_record_email = Record.objects.filter(Email=email).first()

            if existing_record_name:
                messages.warning(request, f"A record with the name '{name}' already exists.")
            elif existing_record_email:
                messages.warning(request, f"A record with the email '{email}' already exists.")
            else:

                form.save()
                messages.success(request, "Your record has been created!")
                return redirect("dashboard")

    context = {'form': form}
    return render(request, 'webapp/create-record.html', context=context)








def update_record(request, pk):

    record = Record.objects.get(id=pk)

    form = UpdateRecordForm(instance=record) 

    if request.method == "POST":

        form = UpdateRecordForm(request.POST, instance=record)

        if form.is_valid():

            form.save()

            messages.success(request, "Your record was updated!")

            return redirect ("dashboard")
        
    context = {'form':form}

    return render(request, 'webapp/update-record.html', context=context)



def singular_record(request, pk):

    all_records = Record.objects.get(id=pk)

    context = {'record':all_records}

    return render(request, 'webapp/view-record.html', context=context)





def delete_record(request, pk):

    record = Record.objects.get(id=pk)

    if request.method == "POST":
        record.delete()

        messages.success(request, "Your record has been deleted!")

        return redirect("dashboard")
    
    context = {'record': record}
    return render(request, 'webapp/delete-record.html', context)







def user_logout(request):

    auth_logout(request)

    messages.success(request, "you Logout successfully!")

    return redirect("my-login")