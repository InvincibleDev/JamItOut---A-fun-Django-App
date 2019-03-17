from django.shortcuts import render, redirect
from django.http import HttpResponse
from jam.models import *
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    return render(request,"home.html")

def signIn(request):
    if request.method=='POST':
        form_username=request.POST.get('username',None)
        form_password=request.POST.get('password',None)
        user = authenticate(request,username=form_username,password=form_password)
        if user is not None:
            login(request,user)
            return redirect("/dashboard")
        else:
            return render(request,"SignIn.html",{'error':'Wrong Credentials'})
    return render(request,"signIn.html")

def signOut(request):
	logout(request)
	return redirect("/")

def signUp(request):
	if request.method=="POST":
		fullname=request.POST.get('fullname',None)
		email=request.POST.get('email',None)
		username=request.POST.get('username',None)
		password=request.POST.get('password',None)

		user_exists=User.objects.filter(username=username).exists()
		if not user_exists:
			user=User.objects.create_user(
			username=username,
			password=password,
			email=email,
			first_name=fullname.split()[0],
			last_name=" ".join(fullname.split()[1:])
			)

			login(request,user)
			return redirect("/dashboard")
		else:
			return render(request,"signIn.html",{'errorsign':"user already Exists. Try other User Name"})
	return render(request,"signIn.html")


@login_required(login_url='/login/')
def dashboard(request):
    lastlinelist=[]
    jams=Jam.objects.filter(Creator=request.user)
    for jam in jams:
        last_lines=JamLines.objects.filter(Jamid=jam).last()
        lastlinelist.append(last_lines)
    contributions=JamLines.objects.filter(Contributer=request.user)
    return render(request,"dashboard.html",{'my_jams':jams,'contributions':contributions,'lastlineslist':lastlinelist})


@login_required(login_url='/login/')
def create_jam(request):
    if request.method=='POST':
        jam_name=request.POST['jam_name']
        noLines=request.POST['noLines']
        start_line=request.POST['start_line']
        form_cover=request.FILES['coverImage']
        now=datetime.now()
        if form_cover.name.endswith(".jpg") or form_cover.name.endswith(".png") or form_cover.name.endswith(".jpeg"):
            new_jam = Jam.objects.create(Title=jam_name, NoLines=noLines, Creator=request.user, Start_date=now.date(), cover=form_cover, Status=True)
            first_line=JamLines.objects.create(Jamid=new_jam,LineNo=1,Line=start_line,Contributer=request.user)
            return redirect(f"/dashboard/")
        else:
            return render(request,"dashboard.html",{'error':'Invalid file type'})
    return HttpResponse("create_jam")


@login_required(login_url='/login/')
def read_jam(request, jam_id):
    allowed=True
    jam = Jam.objects.get(id=jam_id)
    jamline=JamLines.objects.filter(Jamid=jam)
    last_lines=JamLines.objects.filter(Jamid=jam).last()
    if JamLines.objects.filter(Contributer=request.user,Jamid=jam).exists() or last_lines.LineNo == jam.NoLines or last_lines.LineNo==100 or jam.Status == False:
        allowed=False
    return render(request,"read-jam.html",{'jamdet':jam,'jamlines':jamline,'allowed':allowed,'line_no':last_lines.LineNo})


@login_required(login_url='/login/')
def display_jams(request):
    lastlinelist=[]
    jams=Jam.objects.all()
    for jam in jams:
        last_lines=JamLines.objects.filter(Jamid=jam).last()
        lastlinelist.append(last_lines)
    return render(request,"all-jams.html",{'my_jams':jams,'lastlineslist':lastlinelist})


@login_required(login_url='/login/')
def stop_jam(request,jam_id):
    now=datetime.now()
    jam = Jam.objects.get(id=jam_id)
    if request.user!=jam.Creator:
        return render(request,"error.html")
    jam.Status=False
    jam.End_date=now.date()
    jam.save()
    return redirect(f'/readJam/{jam.id}/')


@login_required(login_url='/login/')
def restartjam(request,jam_id):
    jam = Jam.objects.get(id=jam_id)
    if request.user!=jam.Creator:
        return render(request,"error.html")
    jam.Status=True
    jam.End_date=None
    jam.save()
    print(jam)
    return redirect(f'/readJam/{jam.id}/')



@login_required(login_url='/login/')
def new_line(request):
    if request.method=='POST':
        line=request.POST['newline']
        id=request.POST['id']
        contributer=request.user
        line_no=int(request.POST['lno'])+1
        print(id)
        jam=Jam.objects.get(id=id)
        JamLines.objects.create(Jamid=jam,LineNo=line_no,Line=line,Contributer=contributer)
        return redirect(f'/readJam/{jam.id}/')
    return redirect('/dashboard')
