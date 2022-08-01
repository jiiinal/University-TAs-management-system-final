import json
import requests
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponse, HttpResponseRedirect,
                              get_object_or_404, redirect, render)
from django.templatetags.static import static
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
from .models import *
import csv


def add_student(request):

    if request.method=="POST":
        file_csv = request.FILES['file_csv']
        #print(file_csv)
        #file=open(file_csv.file)
        #csvreader=csv.reader(file)
        for row in file_csv:
            row=str(row)
            row=row.split(",")
            row[-1]=row[-1].split('\\')[0]
            row = list(filter(None, row))
            #print(row)
            tmp, created = student.objects.get_or_create(
                mail=row[0][2:],
                pwd=row[1],
                name=row[2],
                batch=row[3],
                sid=int(row[4]))
            tmp.save()
            #print(len(row))

            for j in range(5,len(row)):
                print(row[j].split('\\')[0])
                obj=course.objects.get(courseid=row[j].split('\\')[0],program_year=row[3])
                #print(row[j])
                tmp.cid.add(obj)
                tmp.save()

        #students=student.objects.all()
        #for i in students:
        #    print(i.cid.all())
        return redirect(reverse('cohome'))
    else:
        return render(request,'addstudent.html')

def update_student(request,pk):
    key=get_object_or_404(student,id=pk)
    form = addstudent(request.POST or None,instance=key)
    context ={'form':form}
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request,'Student Updated Sucessfully')
            return redirect(reverse('gostudent'))
        else:
            messages.error(request, "Cannot Update: ")
    return render(request,'updatestudent.html',context)

def delete_student(request,pk):
    key=get_object_or_404(student,id=pk)
    if request.method == 'POST':
        key.delete()
        return redirect(reverse('gostudent'))
    return render(request,'deletestudent.html')


def add_course(request):
    c_form = addcourse()
    context = {'form': c_form, 'page_title': 'Add Course'}
    if request.method == 'POST':
        c_form = addcourse(request.POST)
        if c_form.is_valid():
            c_form.save(commit=False)
            c_form.save()
            messages.success(request,'Course Added Sucessfully')
            return redirect(reverse('gocourse'))
        else:
            messages.error(request, "Cannot Add: ")
    return render(request, 'addcourse.html', context)

def update_course(request,id):
    key=get_object_or_404(course,id=id)
    form = addcourse(request.POST or None,instance=key)
    context ={'form':form}
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request,'Course Updated Sucessfully')
            return redirect(reverse('gocourse'))
        else:
            messages.error(request, "Cannot Update: ")
    return render(request,'updatecourse.html',context)

def delete_course(request,id):
    key=get_object_or_404(course,id=id)
    if request.method == 'POST':
        key.delete()
        return redirect(reverse('gocourse'))
    return render(request,'deletecourse.html')

def add_faculty(request):
    faculty_form = addfaculty(request.POST or None)
    context = {'form': faculty_form, 'page_title': 'Add Faculty'}
    if request.method == 'POST':
        if faculty_form.is_valid():
            faculty_form.save()
            messages.success(request,'Faculty Added Sucessfully')
            return redirect(reverse('gofaculty'))
        else:
            messages.error(request, "Cannot Add: ")
    return render(request, 'addfaculty.html', context)

def update_faculty(request,pk):
    key=get_object_or_404(faculty,id=pk)
    form = addfaculty(request.POST or None,instance=key)
    context ={'form':form}
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request,'Faculty Updated Sucessfully')
            return redirect(reverse('gofaculty'))
        else:
            messages.error(request, "Cannot Update: ")
    return render(request,'updatefaculty.html',context)

def delete_faculty(request,pk):
    key=get_object_or_404(faculty,id=pk)
    if request.method == 'POST':
        key.delete()
        return redirect(reverse('gofaculty'))
    return render(request,'deletefaculty.html')

def add_ta(request):
    ta_form = addta(request.POST or None)
    context = {'form': ta_form, 'page_title': 'Add TA'}
    if request.method == 'POST':
        if ta_form.is_valid():
            ta_form.save()
            messages.success(request,'TA Added Sucessfully')
            return redirect(reverse('gota'))
        else:
            messages.error(request, "Cannot Add: ")
    return render(request, 'addta.html', context)

def update_ta(request,pk):
    key=get_object_or_404(ta,id=pk)
    form = addta(request.POST or None,instance=key)
    context ={'form':form}
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request,'TA Updated Sucessfully')
            return redirect(reverse('gota'))
        else:
            messages.error(request, "Cannot Update: ")
    return render(request,'updateta.html',context)

def delete_ta(request,pk):
    key=get_object_or_404(ta,id=pk)
    if request.method == 'POST':
        key.delete()
        return redirect(reverse('gota'))
    return render(request,'deleteta.html')

def assignta(request,id):
    key=get_object_or_404(ta,id=id)
    form = allocateta(request.POST or None,instance=key)
    context={'form':form}

    if request.method=='POST':
        if form.is_valid():
                #request.POST['status']='Assigned'
                key=get_object_or_404(ta,id=id)
                ob1=form.cleaned_data.get('cid')

                list=ta.objects.filter(cid=ob1,status='Assigned').count()
                if list< ob1.number_of_TA:
                    form.save()
                    key.cid=ob1

                    key.status='Assigned'
                    key.save()
                    messages.success(request,'TA assigned sucessfully.')
                    return redirect(reverse('gota'))
                else :
                    messages.error(request,'Cannot assigned more than threshold')
                    return redirect(reverse('talist'))
    return render(request,'assignta.html',context)

def reassigntas(request,id):
    key=get_object_or_404(ta,id=id)
    form = allocateta(request.POST or None,instance=key)
    context={'form':form}

    if request.method=='POST':
        if form.is_valid():
                context={'form':form}
                #request.POST['status']='Assigned'
                key=get_object_or_404(ta,id=id)
                ob=form.cleaned_data.get('cid')
                list=ta.objects.filter(cid=ob,status='Assigned').count()
                #k=course.objects.get(courseid=ob.courseid)
                if list< ob.number_of_TA:
                    form.save()
                    key.cid=ob
                    key.save()
                    messages.success(request,'TA re-assigned sucessfully.')
                    return redirect(reverse('gota'))
                else :
                    messages.error(request,'Cannot assigned more than threshold')
                    return redirect(reverse('talist2'))
    return render(request,'reassignta.html',context)

def cohome(request):
    context = {
        'page_title': "Co-ordinator Dashboard",
    }
    return render(request, 'cohome.html', context)

def vstudent(request):
    context={}
    dataset=student.objects.all()
    context['odd_rec']=student.objects.none()
    context['even_rec']=student.objects.none()
    for index,data in enumerate(dataset):
        if index%2==0:
            context['even_rec']|={data}
        else:
            context['odd_rec']|={data}
    return render(request, 'student.html', context)

def vcourse(request):
    context={}
    dataset=course.objects.all()
    context['odd_rec']=course.objects.none()
    context['even_rec']=course.objects.none()
    for index,data in enumerate(dataset):
        if index%2==0:
            context['even_rec']|={data}
        else:
            context['odd_rec']|={data}

    return render(request, 'course.html', context)

def vta(request):
    context={}
    dataset=ta.objects.all()
    context['odd_rec']=ta.objects.none()
    context['even_rec']=ta.objects.none()
    for index,data in enumerate(dataset):
        if index%2==0:
            context['even_rec']|={data}
        else:
            context['odd_rec']|={data}
    return render(request, 'ta.html', context)

def vfaculty(request):
    context={}
    dataset=faculty.objects.all()
    context['odd_rec']=faculty.objects.none()
    context['even_rec']=faculty.objects.none()
    for index,data in enumerate(dataset):
        if index%2==0:
            context['even_rec']|={data}
        else:
            context['odd_rec']|={data}
    return render(request, 'faculty.html', context)

def talist(request):
    context={}
    dataset=ta.objects.filter(status='Not Assigned')
    context['odd_rec']=ta.objects.none()
    context['even_rec']=ta.objects.none()
    for index,data in enumerate(dataset):
        if index%2==0:
            context['even_rec']|={data}
        else:
            context['odd_rec']|={data}
    return render(request, 'talist.html', context)

def talist2(request):
    context={}
    dataset=ta.objects.filter(status='Assigned')
    context['odd_rec']=ta.objects.none()
    context['even_rec']=ta.objects.none()
    for index,data in enumerate(dataset):
        if index%2==0:
            context['even_rec']|={data}
        else:
            context['odd_rec']|={data}
    return render(request, 'talist2.html', context)


def declare(request):
    return render(request,'announce.html')

def makeannounce(request):
    ob1=ta.objects.all()
    ob2=faculty.objects.all()
    for ob in ob1:
        ob.an=True
        ob.save()
    for ob in ob2:
        ob.an=True
        ob.save()
    return render(request,'cohome.html')

def copref(request):
    ob=preferences.objects.all()
    context={'pref':ob}
    return render(request,'copref.html',context)
