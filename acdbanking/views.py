from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.db import transaction
from django.db.models import Max
from django.utils import timezone
from django.contrib import messages

# Password Encryption/Decryption Algorithms
from cryptography.fernet import Fernet, InvalidToken
key = b'gxcJK4tRX9gJQ9vKXWNG_oBpCemjCqak-fgXGwJ1G-E='
fernet = Fernet(key)

# Create your views here.
from .models import AcdCustomer, AcdSafeAcnt, AcdChecking, AcdSavings, AcdLoan, AcdPersonal, AcdStudent, AcdInstitute, AcdHome, AcdInsurance, UserAuthEncrypt, UserAuthEncrypt

# To get current highest account number value
def get_highest_a_uid():
    highest_a_uid = AcdSafeAcnt.objects.aggregate(Max('a_uid'))
    highest_a_uid_value = highest_a_uid['a_uid__max']
    return highest_a_uid_value

# Login Page
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user = UserAuthEncrypt.objects.get(username=username)
            if user.is_admin and fernet.decrypt(user.password).decode() == password:
                return redirect('admin_page', username=username)
            elif not user.is_admin and fernet.decrypt(user.password).decode() == password:
                return redirect('customer_page', username=username)
            else:
                return render(request, 'login.html', {'error': 'Invalid username or password'})
        except UserAuthEncrypt.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
        except InvalidToken:
            return render(request, 'login.html', {'error': 'Invalid or tampered token'})
        except TypeError and ValueError:
            return render(request, 'login.html', {'error': 'An error occured'})

    return render(request, 'login.html')

# Customer Page
def customer_page(request, username):
    try:
        customer = AcdCustomer.objects.get(c_id=username)
    except AcdCustomer.DoesNotExist:
        return redirect('login')

    # Fetch additional details from related models
    i = int(username)

    safe_acnts = AcdSafeAcnt.objects.filter(a_uid=username)[:3]
    safe_acnt = safe_acnts[0]
    if len(safe_acnts) == 2:
        safe_acnt1 = safe_acnts[1]
    if len(safe_acnts) == 3:
        safe_acnt1 = safe_acnts[1]
        safe_acnt2 = safe_acnts[2]

    checking_acnts = AcdChecking.objects.filter(acct_no=1000000 + i)
    
    savings_acnts = AcdSavings.objects.filter(acct_no=2000000 + i)
    
    loans = AcdLoan.objects.filter(acct_no=3000000 + i)
    personals = AcdPersonal.objects.filter(pl_uid=40000 + i)
    
    try:
        students = AcdStudent.objects.filter(sl_uid=50000 + i)
        institutes = AcdInstitute.objects.filter(inst_code=i%15)
    except AcdStudent.DoesNotExist:
        institutes = []
    
    try:
        homes = AcdHome.objects.filter(hl_uid=60000 + i)
        insurances = AcdInsurance.objects.filter(ins_acct_no=7000000 + i)
    except AcdHome.DoesNotExist:
        insurances = []

    # Check if the request is a POST request to update the address
    if request.method == 'POST':
        # Retrieve form data
        c_street = request.POST.get('c_street')
        c_city = request.POST.get('c_city')
        c_state = request.POST.get('c_state')
        c_zipcode = request.POST.get('c_zipcode')

        # Update customer's address in the database
        customer.c_street = c_street
        customer.c_city = c_city
        customer.c_state = c_state
        customer.c_zipcode = c_zipcode
        customer.save()
        # Redirect to customer page to display updated details
        return redirect('customer_page', username=username)

    # Render the customer page with the customer's details
    if len(safe_acnts) == 1:
        return render(request, 'customer_page.html', {'customer': customer, 'safe_acnt': safe_acnt, 'checking': checking_acnts,
                                                   'savings': savings_acnts, 'loan': loans, 'personal': personals,
                                                   'student': students, 'institute': institutes, 'home': homes, 'insurance': insurances})

    if len(safe_acnts) == 2:
        return render(request, 'customer_page.html', {'customer': customer, 'safe_acnt': safe_acnt, 'safe_acnt1': safe_acnt1, 'checking': checking_acnts,
                                                   'savings': savings_acnts, 'loan': loans, 'personal': personals,
                                                   'student': students, 'institute': institutes, 'home': homes, 'insurance': insurances})

    if len(safe_acnts) == 3:
        return render(request, 'customer_page.html', {'customer': customer, 'safe_acnt': safe_acnt, 'safe_acnt1': safe_acnt1, 'safe_acnt2': safe_acnt2, 'checking': checking_acnts,
                                                   'savings': savings_acnts, 'loan': loans, 'personal': personals,
                                                   'student': students, 'institute': institutes, 'home': homes, 'insurance': insurances})

# Admin Page
def admin_page(request, username):
    return render(request, 'admin_page.html', {'username': username})

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# Create Customer Page
def create_customer(request):
    # Retrieve admin username from query parameters
    username = request.GET.get('admin_username')
    if request.method == 'POST':
        try:
            # Retrieve form data
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            street = request.POST['street']
            city = request.POST['city']
            state = request.POST['state']
            zipcode = request.POST['zipcode']
            account_types = request.POST.getlist('account_types')
            loan_types = request.POST.getlist('loan_types')
            
            # Validate form data (add more validation as needed)
            if not (first_name and last_name and street and city and state and zipcode):
                raise ValueError("All fields are required")

            # Create customer
            with transaction.atomic():
                i = int(get_highest_a_uid()) + 1
                customer = AcdCustomer.objects.create(
                    c_id = i,
                    c_fname=first_name,
                    c_lname=last_name,
                    c_street=street,
                    c_city=city,
                    c_state=state,
                    c_zipcode=zipcode,
                    a_safe_acnt_id = i
                )
                customer.save()

                # Create associated accounts based on selected types
                if 'checking' in account_types:
                    safe_acct = AcdSafeAcnt.objects.create(
                        a_uid=i,
                        acct_type='C',
                        acct_name=f'Account {i}',
                        a_street=f'Street {i}',
                        a_city=f'City {i}',
                        a_state='NY',
                        a_zipcode='100' + str(i),
                    )
                    safe_acct.save()
                    checking_acct = AcdChecking.objects.create(
                        a_safe_acnt_id=i,
                        acct_no=1000000 + i,
                        date_open=timezone.now(),
                        serv_charge=20.00
                    )
                    checking_acct.save()
                
                if 'savings' in account_types:
                    safe_acct = AcdSafeAcnt.objects.create(
                        a_uid=i,
                        acct_type='S',
                        acct_name=f'Account {i}',
                        a_street=f'Street {i}',
                        a_city=f'City {i}',
                        a_state='NY',
                        a_zipcode='1000' + str(i),
                    )
                    safe_acct.save()
                    savings_acct = AcdSavings.objects.create(
                        a_safe_acnt_id=i,
                        acct_no=2000000 + i,
                        date_open=timezone.now(),
                        intrst_rate=0.02
                    )
                    savings_acct.save()

                if len(loan_types) >= 1:
                    safe_acct = AcdSafeAcnt.objects.create(
                        a_uid=i,
                        acct_type='L',
                        acct_name=f'Account {i}',
                        a_street=f'Street {i}',
                        a_city=f'City {i}',
                        a_state='NY',
                        a_zipcode='1000' + str(i),
                    )
                    safe_acct.save()
                if 'loan' in account_types and 'student_loan' in loan_types:
                    # Create loan accounts based on selected types
                    loan_acct = AcdLoan.objects.create(
                        a_safe_acnt_id=i,
                        acct_no=3000000 + i,
                        loan_type='SL',
                        loan_amt=10000.00 * i,
                        loan_rate=0.05,
                        loan_months=12,
                        loan_payment=1000.00
                    )
                    loan_acct.save()
                    student_loan = AcdStudent.objects.create(
                        a_safe_acnt_id=i,
                        sl_uid=50000 + i,
                         date_open=timezone.now(),
                        student_id=f'STUD00{i}',
                        degree_type='Undergraduate',
                        grad_month='May',
                        grad_year=2024,
                        inst_code_id=i  % 15
                    )
                    student_loan.save()
                if 'loan' in account_types and 'home_loan' in loan_types:
                    loan_acct = AcdLoan.objects.create(
                        a_safe_acnt_id=i,
                        acct_no=3000000 + i,
                        loan_type='HL',
                        loan_amt=10000.00 * i,
                        loan_rate=0.05,
                        loan_months=12,
                        loan_payment=1000.00
                    )
                    loan_acct.save()
                    home_loan = AcdHome.objects.create(
                        a_safe_acnt_id=i,
                        hl_uid=60000 + i,
                        date_open=timezone.now(),
                        built_year=2010 + i
                    )
                    home_loan.save()
                    home_loan = AcdHome.objects.get(hl_uid=60000 + i)
                    # Use the retrieved AcdHome instance when creating AcdInsurance
                    insurance = AcdInsurance.objects.create(
                        ins_acct_no=7000000 + i,
                        ins_company=f'Insurance Company {i}',
                        ins_street=f'Insurance Street {i}',
                        ins_city=f'Insurance City {i}',
                        ins_state='NY',
                        ins_zipcode='100' + str(i),
                        yearly_prm=500.00 * i,
                        hl_uid=home_loan
                    )
                    insurance.save()
                if 'loan' in account_types and 'personal_loan' in loan_types:
                    loan_acct = AcdLoan.objects.create(
                        a_safe_acnt_id=i,
                        acct_no=3000000 + i,
                        loan_type='PL',
                        loan_amt=10000.00 * i,
                        loan_rate=0.05,
                        loan_months=12,
                        loan_payment=1000.00
                    )
                    loan_acct.save()
                    personal_loan = AcdPersonal.objects.create(
                        a_safe_acnt_id=i,
                        pl_uid=40000 + i,
                        date_open=timezone.now()
                    )
                    personal_loan.save()
                
                customerUser = UserAuthEncrypt.objects.create(
                    username=i,
                    password=fernet.encrypt(('AbcXyz@' + str(i)).encode()),
                    is_admin=False
                )
                customerUser.save()

            # Redirect to admin page with success message
            return redirect('admin_page', username=username)
        
        except Exception as e:
            error = str(e)
            acntno = int(get_highest_a_uid()) + 1
            return render(request, 'create_customer.html', {'error': error, 'admin_username': username, 'newacnt': acntno})
    else:
        acntno = int(get_highest_a_uid()) + 1
        return render(request, 'create_customer.html', {'admin_username': username, 'newacnt': acntno})

# Create Admin Page
def create_admin(request):
    username1 = request.GET.get('admin_username')
    if request.method == 'POST':
        try:
            # Retrieve form data
            username = request.POST['username']
            password = request.POST['password']

            # Check if the username is already taken
            if UserAuthEncrypt.objects.filter(username=username).exists():
                raise ValueError("Username already exists")

            # Create the admin user
            UserAuthEncrypt.objects.create(username=username, password=fernet.encrypt(password.encode()), is_admin=True)

            # Redirect to admin page with success message
            messages.success(request, 'Admin user created successfully.')
            return redirect('admin_page', username=username1)

        except Exception as e:
            error = str(e)
            return render(request, 'create_admin.html', {'admin_username': username1, 'error': error})

    return render(request, 'create_admin.html', {'admin_username': username1})

# Delete Admin User Page
def delete_user(request):
    username1 = request.GET.get('admin_username')
    if request.method == 'POST':
        try:
            # Retrieve form data
            username = request.POST['username']

            # Check if the user exists and is not the current admin user
            try:
                user = UserAuthEncrypt.objects.get(username=username)
            except UserAuthEncrypt.DoesNotExist:
                raise ValueError("Account doesn't exist")
            if user.is_admin:
                username2 = user.username
                if str(username1) == str(username2):
                    raise ValueError("Cannot delete current logged in admin account")
                else:
                    user.delete()
                    messages.success(request, 'User deleted successfully.')
            else:
                raise ValueError("Cannot delete non admin account")

            # Redirect to admin page with success message
            return redirect('admin_page', username=username1)

        except Exception as e:
            error = str(e)
            return render(request, 'delete_user.html', {'admin_username': username1, 'error': error})

    return render(request, 'delete_user.html', {'admin_username': username1})

# Delete Customer Page
def delete_customer(request):
    username1 = request.GET.get('admin_username')
    if request.method == 'POST':
        try:
            # Retrieve customer username to delete
            username = request.POST.get('username')

            if str(username) == str(username1):
                raise ValueError("Cannot delete current account.")
            
            try:
                user = UserAuthEncrypt.objects.get(username=username)
            except UserAuthEncrypt.DoesNotExist:
                raise ValueError("Account doesn't exist")
            
            if user.is_admin:
                raise ValueError("Cannot delete admin account")

            with transaction.atomic():
                # Delete the customer details from all related tables
                user.delete()
                (AcdCustomer.objects.filter(c_id=username)).delete()
                i = int(username)
                safe_acnts = AcdSafeAcnt.objects.filter(a_uid=username, acct_type='C')
                safe_acnts.delete()
                safe_acnts = AcdSafeAcnt.objects.filter(a_uid=username, acct_type='S')
                safe_acnts.delete()
                safe_acnts = AcdSafeAcnt.objects.filter(a_uid=username, acct_type='L')
                safe_acnts.delete()
                (AcdChecking.objects.filter(acct_no=1000000 + i)).delete()
                (AcdSavings.objects.filter(acct_no=2000000 + i)).delete()
                (AcdLoan.objects.filter(acct_no=3000000 + i)).delete()
                (AcdPersonal.objects.filter(pl_uid=40000 + i)).delete()
                (AcdStudent.objects.filter(sl_uid=50000 + i)).delete()
                (AcdHome.objects.filter(hl_uid=60000 + i)).delete()
                (AcdInsurance.objects.filter(ins_acct_no=7000000 + i)).delete()

            # Redirect back to admin page with success message
            return redirect('admin_page', username=username1)
        
        except Exception as e:
            error = str(e)
            # Return to admin page with error message
            return render(request, 'delete_customer.html', {'admin_username': username1, 'error': error})
    else:
        # If request method is not POST, redirect to admin page
        return render(request, 'delete_customer.html', {'admin_username': username1})

# Change Password Page - Admins
def change_password(request):
    username = request.GET.get('username')
    if request.method == 'POST':
        try:
            # Retrieve form data
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_new_password = request.POST.get('confirm_new_password')

            # Check if new password and confirm new password match
            if new_password != confirm_new_password:
                raise ValueError("New password and confirm new password do not match.")

            # Check if the current password matches the stored admin password
            # Replace this logic with your actual authentication logic
            user = UserAuthEncrypt.objects.get(username=username)
            if fernet.decrypt(user.password).decode() != current_password:
                raise ValueError("Current password is incorrect.")

            # Update the admin password
            user.password = fernet.encrypt(new_password.encode())
            user.save()

            # Redirect back to admin page with success message
            if user.is_admin == True:
                return redirect('admin_page', username=username)
            else:
                return redirect('customer_page', username=username)

        except Exception as e:
            error = str(e)
            # Return to change password page with error message
            return render(request, 'change_password.html', {'username': username, 'error': error})
    else:
        # If request method is not POST, render the change password page
        return render(request, 'change_password.html', {'username': username})

# Change Password Page - Customers
def change_customer_password(request):
    # Retrieve customer id from query parameters
    customer_id = request.GET.get('customer_id')
    if request.method == 'POST':
        try:
            # Retrieve form data
            new_password = request.POST.get('new_password')
            confirm_new_password = request.POST.get('confirm_new_password')

            # Check if new password and confirm new password match
            if new_password != confirm_new_password:
                raise ValueError("New password and confirm new password do not match.")
            
            # Retrieve customer object based on the customer id
            customer = UserAuthEncrypt.objects.get(username=customer_id)

            # Update the customer password
            customer.password = fernet.encrypt(new_password.encode())
            customer.save()

            # Redirect back to customer page with success message
            return redirect('customer_page', username=customer_id)

        except Exception as e:
            error = str(e)
            # Return to change password page with error message
            return render(request, 'change_customer_password.html', {'error': error, 'customer_username':customer_id})
    else:
        # If request method is not POST, render the change password page
        return render(request, 'change_customer_password.html', {'customer_username':customer_id})

