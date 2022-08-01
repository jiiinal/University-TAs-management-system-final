from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import CreateView
from Main import models
from Main import forms
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import auth
from .models import *
from audioop import reverse
from .forms import addfaculty

# Create your views here.

def base(request):
    return render(request,'home.html')

def home(request):
    return render(request,'basic.html')

def adminlogin(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        try:
            user = coordinator.objects.get(mail=username,pwd=password)
            context={'admin':user}
            messages.success(request,"Successfully logged in")
            return render(request, 'cohome.html', context)
        except :
            user=None
            messages.info(request,"Invalid details")
            return redirect('adminlogin')

    return render(request, 'adminlogin.html')

def tas(request):
    if request.method=="POST":
        signupname = request.POST.get('signupname')
        signuppwd = request.POST.get('signuppwd')
        signupmail = request.POST.get('signupmail')
        signupyear = request.POST.get('signupyear')
        tas = ta(name=signupname,pwd=signuppwd, mail=signupmail, year=signupyear)
        tas.save()
        messages.success(request, 'Profile details updated.')
        return redirect('base')
    return render(request, 'tas.html')

def facultysignup(request):
    faculty_form = addfaculty(request.POST or None)
    context = {'form': faculty_form}
    if request.method == 'POST':
        if faculty_form.is_valid():
            faculty_form.save()
            return redirect('facultylogin')
        else:
            return redirect('facultysignup')

    return render(request, 'facultysignup.html', context)

def talogin(request):
    if request.method=="POST":
        loginemail = request.POST['loginemail']
        loginpwd = request.POST['loginpwd']

        try:
            user = ta.objects.get(mail=loginemail,pwd=loginpwd)
            context={'taid':user.id}
            messages.success(request,"success")
            if user.an ==True:
                user.an=False
                user.save()
                messages.success(request,"Process Completed")
            return render(request, 'TAhome.html', context)
        except :
            user=None
            messages.info(request,"Invalid details")
            return redirect('tas')

    return render(request, 'talogin.html')

def facultylogin(request):
    if request.method=="POST":
        facultymail = request.POST.get('facultymail')
        facultypwd = request.POST.get('facultypwd')

        try:
            user = faculty.objects.get(mail=facultymail, pwd=facultypwd)
            context= {'facid': user.id}
            messages.success(request,"success")
            if user.an ==True:
                user.an=False
                user.save()
                messages.success(request,"Process Completed")
            #return render(request, 'facultyHome.html')
            return render(request, 'facultyHome.html', context)
        except :
            user=None
            messages.info(request,"Invalid details!!!!!")
            return redirect('base')

    return render(request, 'facultylogin.html')

def studentlogin(request):
    if request.method=="POST":
        studentemail = request.POST['studentemail']
        studentpwd = request.POST['studentpwd']
        print(studentemail)

        try:
            user = student.objects.get(mail=studentemail,pwd=studentpwd)
            context={'sid':user.id}
            messages.success(request,"success")
            return render(request, 'StudentHome.html', context)

        except:
            user=None
            messages.info(request,"Invalid details")
            return redirect('studentlogin')

    return render(request, 'studentlogin.html')

def talogout(request):
    return HttpResponse('logout')

def TAhome(request, id):
    user = ta.objects.get(id=id)
    context={'taid': user.id, 'obj': user}
    return render(request,'TAhome.html', context)

def StiReq(request, id):
    obj = ta.objects.get(id=id)
    context = {'taid' : obj.id}

    if obj.status == 'Not Assigned':
        context = {'taid' : obj.id, 'message': "You are not assigned to any course yet! So you can't send request!"}
        return render(request,'stipendReq.html', context)

    else:
        cours = course.objects.get(courseid = obj.cid.courseid, program_year= obj.cid.program_year)
        fac= faculty.objects.filter(cid = obj.cid)
        if fac.exists():
            fac= faculty.objects.get(cid = obj.cid)
            if request.method=="POST":
                StiRequest = stipendRequest()
                StiRequest.message = request.POST.get('message_text')
                StiRequest.Month = request.POST.get('month')
                StiRequest.TAObj = obj
                StiRequest.FacultyObj = fac
                StiRequest.CourseObj = cours
                StiRequest.save()
                context = {'taid' : obj.id, 'message': "Request sent. See status in \'See Previous Request\'!"}
                return render(request, 'TAhome.html', context)
        else :
            context = {'taid' : obj, 'message': "Your course is still not assigned to any faculty!! So you wait for a while!"}
            return render(request,'stipendReq.html', context)
    return render(request,'stipendReq.html', context)

def PrevReq(request, id):
    obj = ta.objects.get(id=id)
    context = {'taid' : obj.id}

    if obj.status == 'Not Assigned':
        context = {'taid':obj.id, 'message': "You are still not assigned to any course"}
        return render(request, 'prevReq.html', context)

    else:
        reqs = stipendRequest.objects.filter(TAObj = obj)
        context = {'taid':obj.id, 'message': "Status of your sent requests", 'reqs':reqs}
        return render(request, 'prevReq.html', context)

def viewCourse(request, id):
    obj = ta.objects.get(id=id)
    filtered_ratings = rating.objects.filter(TAObj = obj)
    if filtered_ratings:
        total=0
        for star in filtered_ratings:
            total+=star.rate
        # print(obj.ratings)
        obj.ratings= round(total/filtered_ratings.count(), 2)
        # obj.ratings=0
        obj.save()
    if obj.status == 'Not Assigned':
        text = "You are not assigned to any course yet!"
        context = {'taid' : obj.id, 'user':obj, 'message': text}
        return render(request,'viewAssignedCourse.html', context)

    else:
        cours = course.objects.get(courseid = obj.cid.courseid, program_year= obj.cid.program_year)
        fac= faculty.objects.filter(cid = obj.cid)
        if fac.exists():
            fac= faculty.objects.get(cid = obj.cid)
            text = ""
            context = { 'viewCourse':cours, 'fac':fac, 'user':obj, 'message':text}
            return render(request, 'viewAssignedCourse.html', context)
        else:
            text = "Your course is still not assigned to any faculty!!"
            context = { 'viewCourse':cours, 'user':obj, 'message':text}
            return render(request,'viewAssignedCourse.html', context)

def facultyHome(request, id):
    user = faculty.objects.get(id=id)
    context={'facid': user.id}
    return render(request,'facultyhome.html', context)
    #return render(request, 'facultyHome.html')

def seePendingReq(request, id):
    obj = faculty.objects.get(id=id)
    reqs = stipendRequest.objects.filter(FacultyObj = obj).exclude(status='Approved')
    #reqs = stipendRequest.objects.filter(FacultyObj = obj | status= 'Not Approved yet')
    context = {'facid':obj.id, 'reqs':reqs}
    if request.method=="POST":
        ID = request.POST.get('reqId')
        # print(ID)
        req = stipendRequest.objects.get(id=ID)
        # print(req)
        req.status = request.POST.get('status')
        # print(req.status)
        req.save()
        # StiRequest = stipendRequest.objects.get(TAObj.id == 24, Month=month)
        # StiRequest.save()
        return render(request, 'seePendingReq.html', context)
    return render(request, 'seePendingReq.html', context)

def seeApprovedReq(request, id):
    obj = faculty.objects.get(id=id)
    reqs = stipendRequest.objects.filter(FacultyObj = obj, status= 'Approved')
    context = {'facid':obj.id, 'reqs':reqs}
    return render(request, 'seeApprovedReq.html', context)

def assignedCourse(request, id):
    obj = faculty.objects.get(id=id)
    cours = course.objects.filter(courseid = obj.cid.courseid, program_year= obj.cid.program_year)
    context = {'viewCourse':cours, 'user':obj}
    return render( request, 'assignedCourse.html', context)

def seeList(request, id):
    see_List = ta.objects.all()
    context= {'seeList' : see_List, 'facid':id}
    return render(request, 'seeList.html', context)

def studentHome(request, id):
    context = {'sid':id}
    return render(request, 'StudentHome.html', context)

def rateTA(request, id):
    obj = student.objects.get(id=id)
    context = {'s':obj}

    if request.method=="POST":
        course1 = request.POST.get('selectcourse')
        # print(request.POST.get('selectcourse'))
        # course1 = request.POST.get('selectcourse')
        # course2= course1.split(" ")
        # course_selected = course.objects.get(name = course2[0], program_year=course2[1])
        course_selected = course.objects.get(id= course1)
        rate = rating.objects.filter(studentObj= obj, CourseObj=course_selected)
        if not rate:
            TA_list = ta.objects.filter(cid=course_selected)
            context = {'s':obj, 'course_sel': course_selected, 'TAlist':TA_list}
            return render(request, 'rateTA2.html', context)
        else :
            message= "You have already rated for this subject!! Rate for another."
            context = {'s':obj, 'message': message}
            return render(request, 'rateTA.html', context)
    return render(request, 'rateTA.html', context)

def rateTA2(request, id):
    obj = student.objects.get(id=id)
    context = {'sid':obj.id}

    if request.method=="POST":
        selectedTA= request.POST.get('selectTA')
        course_sel= request.POST.get('selectedCourse')
        stars= request.POST.get('ratings')
        TAObject = ta.objects.get(id = selectedTA)
        # print(selectedTA)
        rated = rating()
        rated.rate = stars
        rated.studentObj = student.objects.get(id= id)
        rated.TAObj = ta.objects.get(id = selectedTA)
        rated.CourseObj = course.objects.get(id = course_sel)
        rated.save()
        rates = rating.objects.filter(TAObj = TAObject)
        # print(rates.count())
        ta_rated = ta.objects.get(id = selectedTA)
        ta_rated.ratings= round((ta_rated.ratings + int(stars) )/(rates.count()+1), 2)
        # print(ta_rated.ratings)
        ta_rated.save()
        context = {'sid' : obj.id, 'message': "Successfully rated👍🏻. Rate another!"}
        return render(request, 'StudentHome.html', context)
    # return render(request, 'rateTA.html')


def submitPref(request, id):
    user = faculty.objects.get(id=id)
    List_see = ta.objects.all()
    listnum = range(1,user.cid.number_of_TA+1)
    context={'Listsee' : List_see, 'facid': user.id, 'listofnum': listnum}

    if request.method=="POST":
       ta_list = request.POST.getlist('boxes')
       tanum = request.POST.getlist('selectTA')
       print(ta_list)
       print(tanum)
       for index,obj in enumerate (ta_list):
                Preferences = preferences()
                Preferences.TAID = ta.objects.get(id=obj)
                Preferences.facultyID = user
                Preferences.preference = tanum[index]
                Preferences.save()
       return render(request, 'submitPref.html', context)          
    return render(request, 'submitPref.html', context) 
