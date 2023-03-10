from django.shortcuts import render

# Create your views here.
from django.db.models import Max
from .models import user_login

def index(request):
    return render(request, './myapp/index.html')


def about(request):
    return render(request, './myapp/about.html')


def contact(request):
    return render(request, './myapp/contact.html')

#################### ADMIN #########################################
def admin_login(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        pwd = request.POST.get('pwd')
        #print(un,pwd)
        #query to select a record based on a condition
        ul = user_login.objects.filter(uname=un, passwd=pwd, u_type='admin')

        if len(ul) == 1:
            request.session['admin_name'] = ul[0].uname
            request.session['admin_id'] = ul[0].id
            return render(request,'./myapp/admin_home.html')
        else:
            msg = '<h1> Invalid Uname or Password !!!</h1>'
            context ={ 'msg1':msg }
            return render(request, './myapp/admin_login.html',context)
    else:
        msg = ''
        context ={ 'msg1':msg }
        return render(request, './myapp/admin_login.html',context)


def admin_home(request):
    try:
        uname = request.session['admin_name']
        print(uname)
    except:
        return admin_login(request)
    else:
        return render(request,'./myapp/admin_home.html')


def admin_logout(request):
    try:
        del request.session['admin_name']
        del request.session['admin_id']
    except:
        return admin_login(request)
    else:
        return admin_login(request)

def admin_changepassword(request):
    if request.method == 'POST':
        opasswd = request.POST.get('opasswd')
        npasswd = request.POST.get('npasswd')
        cpasswd = request.POST.get('cpasswd')
        uname = request.session['admin_name']
        try:
            ul = user_login.objects.get(uname=uname,passwd=opasswd,u_type='admin')
            if ul is not None:
                ul.passwd=npasswd
                ul.save()
                context = {'msg': 'Password Changed'}
                return render(request, './myapp/admin_changepassword.html', context)
            else:
                context = {'msg': 'Password Not Changed'}
                return render(request, './myapp/admin_changepassword.html', context)
        except user_login.DoesNotExist:
            context = {'msg': 'Password Err Not Changed'}
            return render(request, './myapp/admin_changepassword.html', context)
    else:
        context = {'msg': ''}
        return render(request, './myapp/admin_changepassword.html', context)


from .models import house_type


def admin_house_type_add(request):
    if request.method == "POST":
        type_name = request.POST.get('type_name')
        house_obj = house_type(type_name = type_name)
        house_obj.save()
        context = {'msg':'New house type added'}
        return render(request, './myapp/admin_house_type_add.html',context)
    else:
        return render(request, './myapp/admin_house_type_add.html')


def admin_house_type_view(request):
    type_list = house_type.objects.all()
    context = {'type_list':type_list}
    return render(request, './myapp/admin_house_type_view.html',context)


def admin_house_type_delete(request):
    id = request.GET.get('id')
    print('id = '+id)
    cg = house_type.objects.get(id=int(id))
    cg.delete()
    msg = 'House type removed'

    type_list = house_type.objects.all()
    context = {'type_list': type_list, 'msg':msg}
    return render(request, './myapp/admin_house_type_view.html', context)


def admin_house_type_edit(request):
    if request.method == 'POST':
        e_id = request.POST.get('e_id')
        type_name = request.POST.get('type_name')
        type_obj = house_type.objects.get(id=int(e_id))
        type_obj.type_name = type_name
        type_obj.save()

        msg = 'House type record Updated'
        type_list = house_type.objects.all()
        context = {'type_list': type_list, 'msg': msg}
        return render(request, './myapp/admin_house_type_view.html', context)
    else:
        id = request.GET.get('id')
        type_obj = house_type.objects.get(id=int(id))
        context = {'type_name': type_obj.type_name, 'e_id': type_obj.id}
        return render(request, './myapp/admin_house_type_edit.html',context)

from .models import user_details


def admin_user_details_view(request):
    user_list = user_details.objects.all()
    context = {'user_list': user_list}
    return render(request, './myapp/admin_user_details_view.html', context)

def admin_user_details_delete(request):
    try:
        uname = request.session['admin_name']
        print(uname)
    except:
        return admin_login(request)

    id = request.GET.get('id')
    print('id = '+id)
    user_obj = user_details.objects.get(id=int(id))
    user_id = user_obj.user_id
    user_obj.delete()
    user_obj = user_login.objects.get(id=int(user_id))
    user_obj.delete()

    msg = 'User Record Deleted'

    user_list = user_details.objects.all()

    context = {'user_list': user_list,  'msg':msg}
    return render(request, './myapp/admin_user_details_view.html', context)


from .models import house_manager

def admin_owner_details_view(request):
    owner_list = house_manager.objects.filter(status='approved')
    context = {'owner_list': owner_list}
    return render(request, './myapp/admin_owner_details_view.html', context)

def admin_owner_details_delete(request):
    try:
        uname = request.session['admin_name']
        print(uname)
    except:
        return admin_login(request)

    id = request.GET.get('id')
    print('id = '+id)
    owner_obj = house_manager.objects.get(id=int(id))
    user_id = owner_obj.user_id
    owner_obj.delete()
    user_obj = user_login.objects.get(id=int(user_id))
    user_obj.delete()

    msg = 'Manager Record Deleted'

    owner_list = house_manager.objects.all()

    context = {'owner_list': owner_list,  'msg':msg}
    return render(request, './myapp/admin_owner_details_view.html', context)


def admin_owner_details_pending_view(request):
    owner_list = house_manager.objects.filter(status='pending')
    context = {'owner_list': owner_list}
    return render(request, './myapp/admin_owner_details_pending_view.html', context)


def admin_owner_details_register_update(request):
    #user_id = request.session['staff_id']
    id = request.GET.get('id')
    hm_obj = house_manager.objects.get(id=int(id))
    status = request.GET.get('status')
    if status == 'rejected':
        hm_obj.status = status
        hm_obj.save()
        context = {'msg': 'Manager rejected'}
        return render(request, 'myapp/admin_messages.html', context)
    elif status == 'approved':
        hm_obj.status = status
        hm_obj.save()
        context = {'msg': 'Manager approved'}
        return render(request, 'myapp/admin_messages.html', context)

    context = {'msg':''}
    return render(request, './myapp/admin_messages.html',context)


def admin_house_details_pending_view(request):
    #user_id = int(request.session['owner_id'])
    hd_list = house_details.objects.filter(status='pending')
    type_list = house_type.objects.all()
    hm_list = house_manager.objects.all()
    context = {'house_list': hd_list,'type_list':type_list, 'owner_list': hm_list}
    return render(request, './myapp/admin_house_details_view.html', context)

def admin_house_details_register_update(request):
    #user_id = request.session['staff_id']
    id = request.GET.get('id')
    hd_obj = house_details.objects.get(id=int(id))
    status = request.GET.get('status')
    if status == 'rejected':
        hd_obj.status = status
        hd_obj.save()
        context = {'msg': 'House rejected'}
        return render(request, 'myapp/admin_messages.html', context)
    elif status == 'approved':
        hd_obj.status = status
        hd_obj.save()
        context = {'msg': 'House approved'}
        return render(request, 'myapp/admin_messages.html', context)

    context = {'msg':''}
    return render(request, './myapp/admin_messages.html',context)

############################################################################################
################################# OWNER ##################################
from .models import house_manager

def owner_login_check(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        passwd = request.POST.get('passwd')

        ul = user_login.objects.filter(uname=uname, passwd=passwd, u_type='owner')
        print(len(ul))
        if len(ul) == 1:
            hm_object = house_manager.objects.get(user_id=ul[0].id)
            if hm_object.status == 'pending':
                context = {'msg': 'Account not yet activated by Admin'}
                return render(request, 'myapp/owner_login.html', context)
            request.session['owner_id'] = ul[0].id
            request.session['owner_name'] = ul[0].uname
            context = {'uname': f'{hm_object.fname} {hm_object.lname}'}
            #send_mail('Login','welcome'+uname,uname)
            return render(request, 'myapp/owner_home.html',context)
        else:
            context = {'msg': 'Invalid Credentials'}
            return render(request, 'myapp/owner_login.html',context)
    else:
        return render(request, 'myapp/owner_login.html')

def owner_home(request):
    try:
        user_id = int(request.session['owner_id'])
        hm_object = house_manager.objects.get(user_id=user_id)
        context = {'uname': f'{hm_object.fname} {hm_object.lname}'}
        return render(request, './myapp/owner_home.html', context)
    except:
        context = {'msg': 'Session Expired'}
        return render(request, 'myapp/owner_login.html', context)


def owner_details_add(request):
    if request.method == 'POST':
        # 3. house_manager - id, user_id, fname, lname, addr, pin, email, contact, status
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')

        addr = request.POST.get('addr')
        pin = request.POST.get('pin')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = request.POST.get('pwd')
        uname = email
        status = "pending"

        ul_obj = user_login(uname=uname, passwd=password, u_type='owner')
        ul_obj.save()
        user_id = user_login.objects.all().aggregate(Max('id'))['id__max']

        hm_obj = house_manager(user_id=user_id, fname=fname, lname=lname, addr=addr,
                               pin=pin, contact=contact, email=email, status=status)
        hm_obj.save()

        print(user_id)
        context = {'msg': 'House Manager Registered , Admin verification pending'}
        return render(request, 'myapp/owner_login.html',context)

    else:
        return render(request, 'myapp/owner_details_add.html')

def owner_changepassword(request):
    if request.method == 'POST':
        uname = request.session['owner_name']
        new_password = request.POST.get('new_password')
        current_password = request.POST.get('current_password')
        print("username:::" + uname)
        print("current_password" + str(current_password))

        try:

            ul = user_login.objects.get(uname=uname, passwd=current_password)

            if ul is not None:
                ul.passwd = new_password  # change field
                ul.save()
                context = {'msg':'Password Changed Successfully'}
                return render(request, './myapp/owner_changepassword.html',context)
            else:
                context = {'msg': 'Password Not Changed'}
                return render(request, './myapp/owner_changepassword.html', context)
        except user_login.DoesNotExist:
            context = {'msg': 'Password Not Changed'}
            return render(request, './myapp/owner_changepassword.html', context)
    else:
        return render(request, './myapp/owner_changepassword.html')



def owner_logout(request):
    try:
        del request.session['owner_name']
        del request.session['owner_id']
    except:
        return owner_login_check(request)
    else:
        return owner_login_check(request)


def owner_profile_view(request):
    user_id = request.session['owner_id']
    hm_obj = house_manager.objects.get(user_id=int(user_id))
    context = {'owner_obj': hm_obj, 'e_id': hm_obj.id}
    return render(request, './myapp/owner_profile_view.html',context)

from .models import house_details

def owner_house_details_add(request):
    if request.method == 'POST':
        #4. house_details - id, user_id, house_name, house_type_id, rent_amt, rent_advance, addr1, addr2, addr3, pin, house_decp, house_rules, house_facilities, status
        user_id = int(request.session['owner_id'])
        house_name = request.POST.get('house_name')
        rent_amt = float(request.POST.get('rent_amt'))
        house_type_id = int(request.POST.get('house_type_id'))
        rent_advance = request.POST.get('rent_advance')
        addr1 = request.POST.get('addr1')
        addr2 = request.POST.get('addr2')
        addr3 = request.POST.get('addr3')
        pin = request.POST.get('pin')
        house_descp = request.POST.get('house_descp')
        house_rules = request.POST.get('house_rules')
        house_facilities = request.POST.get('house_facilities')
        status = 'pending'

        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        pic_path = fs.save(uploaded_file.name, uploaded_file)

        hd_obj = house_details(
            user_id=user_id,house_name=house_name, rent_advance=rent_advance, rent_amt=rent_amt,
            house_type_id=house_type_id, addr1=addr1, addr2=addr2,addr3=addr3, pin=pin,
            house_descp=house_descp, house_rules=house_rules, house_facilities=house_facilities, status=status)
        hd_obj.save()
        house_id = house_details.objects.all().aggregate(Max('id'))['id__max']

        hp_objj = house_pics(house_id=int(house_id), pic_path=pic_path)
        hp_objj.save()


        print(user_id)
        context = {'msg': 'New House Registered, Admin approval pending'}
        return render(request, 'myapp/owner_messages.html',context)

    else:
        type_list = house_type.objects.all()
        context = {'type_list': type_list}
        return render(request, 'myapp/owner_house_details_add.html', context)

def owner_house_details_view(request):
    user_id = int(request.session['owner_id'])
    hd_list = house_details.objects.filter(user_id=user_id, status='approved')
    type_list = house_type.objects.all()
    context = {'house_list': hd_list,'type_list':type_list}
    return render(request, './myapp/owner_house_details_view.html', context)

def owner_house_details_pending_view(request):
    user_id = int(request.session['owner_id'])
    hd_list = house_details.objects.filter(user_id=user_id, status='pending')
    type_list = house_type.objects.all()
    context = {'house_list': hd_list,'type_list':type_list}
    return render(request, './myapp/owner_house_details_view.html', context)

def owner_house_details_delete(request):
    try:
        uname = request.session['owner_name']
        print(uname)
    except:
        return owner_login_check(request)

    id = request.GET.get('id')
    print('id = '+id)
    hd_obj = house_details.objects.get(id=int(id))
    hd_obj.delete()

    msg = 'House Details Deleted'

    context = {'msg':msg}
    return render(request, './myapp/owner_messages.html', context)

def owner_house_details_edit(request):
    if request.method == 'POST':
        e_id = request.POST.get('e_id')

        user_id = int(request.session['owner_id'])
        house_name = request.POST.get('house_name')
        rent_amt = float(request.POST.get('rent_amt'))
        house_type_id = int(request.POST.get('house_type_id'))
        rent_advance = request.POST.get('rent_advance')
        addr1 = request.POST.get('addr1')
        addr2 = request.POST.get('addr2')
        addr3 = request.POST.get('addr3')
        pin = request.POST.get('pin')
        house_descp = request.POST.get('house_descp')
        house_rules = request.POST.get('house_rules')
        house_facilities = request.POST.get('house_facilities')

        hd_obj = house_details.objects.get(id=int(e_id))
        hd_obj.house_name = house_name
        hd_obj.rent_amt = float(rent_amt)
        hd_obj.rent_advance = rent_advance
        hd_obj.house_type_id = house_type_id
        hd_obj.addr1 = addr1
        hd_obj.addr2 = addr2
        hd_obj.addr3 = addr3
        hd_obj.pin = pin
        hd_obj.house_descp = house_descp
        hd_obj.house_rules = house_rules
        hd_obj.house_facilities = house_facilities
        hd_obj.save()

        msg = 'House Record Updated'

        context = { 'msg': msg}
        return render(request, './myapp/owner_messages.html', context)
    else:
        id = request.GET.get('id')
        hd_obj = house_details.objects.get(id=int(id))
        type_list = house_type.objects.all()
        context = {'hd_obj': hd_obj, 'e_id': hd_obj.id, 'type_list':type_list}
        return render(request, './myapp/owner_house_details_edit.html',context)


from .models import house_pics
from django.core.files.storage import FileSystemStorage

def owner_house_pic_add(request):
    if request.method == 'POST':
        house_id = request.POST.get('house_id')
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        pic_path = fs.save(uploaded_file.name, uploaded_file)

        hp_obj = house_pics(house_id=int(house_id),pic_path=pic_path)
        hp_obj.save()

        context = {'msg':'Picture added','house_id':house_id}
        return render(request, 'myapp/owner_house_pic_add.html',context)

    else:
        house_id = request.GET.get('house_id')
        context = {'msg':'','house_id':house_id}
        return render(request, 'myapp/owner_house_pic_add.html',context)

def owner_house_pic_delete(request):
    id = request.GET.get('id')
    house_id = request.GET.get('house_id')
    print("id="+id)
    hp_obj = house_pics.objects.get(id=int(id))
    hp_obj.delete()

    hp_list = house_pics.objects.filter(house_id=int(house_id))
    context ={'pic_list':hp_list,'house_id': house_id,'msg':'Picture deleted'}
    return render(request,'myapp/owner_house_pic_view.html',context)

def owner_house_pic_view(request):
    house_id = request.GET.get('house_id')
    hp_list = house_pics.objects.filter(house_id=int(house_id))

    context = {'pic_list': hp_list, 'house_id': house_id, 'msg': ''}
    return render(request, 'myapp/owner_house_pic_view.html', context)

#################################### USER #####################################
from .models import user_details

def user_login_check(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        passwd = request.POST.get('passwd')

        ul = user_login.objects.filter(uname=uname, passwd=passwd, u_type='user')
        print(len(ul))
        if len(ul) == 1:
            request.session['user_id'] = ul[0].id
            request.session['user_name'] = ul[0].uname
            context = {'uname': request.session['user_name']}
            #send_mail('Login','welcome'+uname,uname)
            return render(request, 'myapp/user_home.html',context)
        else:
            context = {'msg': 'Invalid Credentials'}
            return render(request, 'myapp/user_login.html',context)
    else:
        return render(request, 'myapp/user_login.html')

def user_home(request):

    context = {'uname':request.session['user_name']}
    return render(request,'./myapp/user_home.html',context)
    #send_mail("heoo", "hai", 'snehadavisk@gmail.com')

def user_details_add(request):
    if request.method == 'POST':

        fname = request.POST.get('fname')
        lname = request.POST.get('lname')

        gender = request.POST.get('gender')
        dob = request.POST.get('age')
        addr = request.POST.get('addr')
        pin = request.POST.get('pin')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = request.POST.get('pwd')
        uname=email
        status = "new"

        ul = user_login(uname=uname, passwd=password, u_type='user')
        ul.save()
        user_id = user_login.objects.all().aggregate(Max('id'))['id__max']

        ud = user_details(user_id=user_id,fname=fname, lname=lname, gender=gender, dob=dob,addr=addr,
                          pin=pin, contact=contact, email=email, status=status )
        ud.save()

        print(user_id)
        context = {'msg': 'User Registered'}
        return render(request, 'myapp/user_login.html',context)

    else:
        return render(request, 'myapp/user_details_add.html')

def user_changepassword(request):
    if request.method == 'POST':
        uname = request.session['user_name']
        new_password = request.POST.get('new_password')
        current_password = request.POST.get('current_password')
        print("username:::" + uname)
        print("current_password" + str(current_password))

        try:

            ul = user_login.objects.get(uname=uname, passwd=current_password)

            if ul is not None:
                ul.passwd = new_password  # change field
                ul.save()
                context = {'msg':'Password Changed Successfully'}
                return render(request, './myapp/user_changepassword.html',context)
            else:
                context = {'msg': 'Password Not Changed'}
                return render(request, './myapp/user_changepassword.html', context)
        except user_login.DoesNotExist:
            context = {'msg': 'Password Not Changed'}
            return render(request, './myapp/user_changepassword.html', context)
    else:
        return render(request, './myapp/user_changepassword.html')



def user_logout(request):
    try:
        del request.session['user_name']
        del request.session['user_id']
    except:
        return user_login_check(request)
    else:
        return user_login_check(request)



