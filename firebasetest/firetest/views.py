from django.shortcuts import render
import pyrebase
from django.contrib import auth
config = {
'apiKey': "AIzaSyDTG9IIvHj-v4-NmO-vgM92V2L1HfYv4wI",
    'databaseURL': "https://fir-test-df37b.firebaseio.com",
    'authDomain': "fir-test-df37b.firebaseapp.com",
    'projectId': "fir-test-df37b",
    'storageBucket': "fir-test-df37b.appspot.com",
    'messagingSenderId': "885236684439"
  }
firebase = pyrebase.initialize_app(config)
autha = firebase.auth()
database = firebase.database()

# Create your views here.
def login(request):

    return render(request,'login.html')

def postlogin(request):
    email = request.POST.get('email')
    password = request.POST.get('pass')
    try:
        user = autha.sign_in_with_email_and_password(email,password)
    except:
        msg="Wrong"
        return render(request,'post.html',{'msg':msg})
    context = {
        "em":email,
        }
    print(user)
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    return render(request,'post.html',context)

def logout(request):
    auth.logout(request)
    return render(request,'login.html')

def signup(request):
    return render(request,'signup.html')

def postup(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('pass')
    user = autha.create_user_with_email_and_password(email,password)
    uid = user['localId']
    data = {"name":name,"status": "1"}
    database.child("users").child(uid).child("details").set(data)
    return render(request,'login.html')

def create(request):
    return render(request,'create.html')

def post_create(request):
    import time
    from datetime import datetime,timezone
    import pytz
    tz = pytz.timezone('Asia/Kolkata')
    time_now  =datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))
    work = request.POST.get('work')
    progress = request.POST.get('progress')
    data = {
        "work":work,
            "progress":progress
            }
    idtoken = request.session['uid']
    a = autha.get_account_info(idtoken)
    uid = a["users"][0]["localId"]
    database.child('users').child(uid).child('reports').child(millis).set(data)
    name = database.child('users').child(uid).child('details').child('name').get().val()
    print(name)
    return render(request,'post.html',{"em":name})

def check(request):
    import datetime
    idtoken=request.session['uid']
    a = autha.get_account_info(idtoken)
    uid = a['users'][0]['localId']
    timestamps = database.child('users').child(uid).child('reports').shallow().get().val()
    lis = []
    for i in timestamps:
        lis.append(i)
    lis.sort(reverse=True)
    work = []
    for i in lis:
        wor = database.child('users').child(uid).child('reports').child(i).child('work').get().val()
        work.append(wor)
    date = []
    for i in lis:
        i = float(i)
        dat = datetime.datetime.fromtimestamp(i).strftime('%H : %M %d-%M-%Y')
        date.append(dat)
    comb = zip(lis,date,work)
    name = database.child('users').child(uid).child('details').child('name').get().val()
    context = {
        'comb':comb,
        'name':name
    }
    return render(request,'check.html',context)

def post_check(request):
    import datetime
    time = request.GET.get('z')
    idtoken = request.session['uid']
    a = autha.get_account_info(idtoken)
    uid = a['users'][0]['localId']
    work = database.child('users').child(uid).child('reports').child(time).child('work').get().val()
    progress = database.child('users').child(uid).child('reports').child(time).child('progress').get().val()
    i = float(time)
    dat = datetime.datetime.fromtimestamp(i).strftime('%H : %M %d-%M-%Y')
    name = database.child('users').child(uid).child('details').child('name').get().val()

    context = {
        'w':work,
        'p':progress,
        'd':dat,
        'name':name
    }
    print("Work ",work)
    print("Progress ",progress)
    return render(request,'post_check.html',context)

