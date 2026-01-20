# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.contrib.auth.hashers import make_password, check_password
# from .models import Student
# from django.views.decorators.cache import never_cache


# def register(request):
#     if request.method == 'POST':
#         full_name = request.POST['full_name']
#         email = request.POST['email']
#         mobile = request.POST['mobile']
#         password = request.POST['password']
#         confirm_password = request.POST['confirm_password']

#         if password != confirm_password:
#             messages.error(request, "Passwords do not match")
#             return redirect('/')

#         if Student.objects.filter(email=email).exists():
#             messages.error(request, "Email already exists")
#             return redirect('/')

#         Student.objects.create(
#             full_name=full_name,
#             email=email,
#             mobile=mobile,
#             password=make_password(password)
#         )

#         messages.success(request, "Registration successful! Please login.")
#         return redirect('/login/')

#     return render(request, 'register.html')


# def login_view(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']

#         try:
#             student = Student.objects.get(email=email)
#             if check_password(password, student.password):
#                 request.session['student_id'] = student.id
#                 request.session['student_name'] = student.full_name
#                 request.session['student_email'] = student.email
#                 return redirect('/dashboard/')
#             else:
#                 return render(request, 'login.html', {'error': 'Invalid email or password'})
#         except Student.DoesNotExist:
#             return render(request, 'login.html', {'error': 'Invalid email or password'})

#     return render(request, 'login.html')


# def dashboard(request):
#     if not request.session.get('student_id'):
#         return redirect('/login/')
#     return render(request, 'dashboard.html')


# def logout_view(request):
#     request.session.flush()
#     messages.success(request, "Logged out successfully")
#     return redirect('/login/')





from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.cache import never_cache
from .models import Student

# ===== Register View =====
@never_cache
def register(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('/')

        if Student.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('/')

        Student.objects.create(
            full_name=full_name,
            email=email,
            mobile=mobile,
            password=make_password(password)
        )

        messages.success(request, "Registration successful! Please login.")
        return redirect('/login/')  # ✅ redirect login page

    return render(request, 'register.html')


# ===== Login View =====
@never_cache
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            student = Student.objects.get(email=email)
            if check_password(password, student.password):
                request.session['student_id'] = student.id
                request.session['student_name'] = student.full_name
                request.session['student_email'] = student.email
                return redirect('/dashboard/')
            else:
                return render(request, 'login.html', {'error': 'Invalid email or password'})
        except Student.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid email or password'})

    return render(request, 'login.html')


# ===== Dashboard =====
@never_cache
def dashboard(request):
    if not request.session.get('student_id'):
        return redirect('/login/')
    return render(request, 'dashboard.html')


# ===== Logout =====
@never_cache
def logout_view(request):
    request.session.flush()
    messages.success(request, "Logged out successfully")
    return redirect('/login/')
