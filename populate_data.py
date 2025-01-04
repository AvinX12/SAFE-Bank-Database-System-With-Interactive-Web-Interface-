import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "acdproject.settings")
import django
django.setup()

from cryptography.fernet import Fernet
key = b'gxcJK4tRX9gJQ9vKXWNG_oBpCemjCqak-fgXGwJ1G-E='
fernet = Fernet(key)

from datetime import datetime
from django.utils import timezone
from acdbanking.models import AcdSafeAcnt, AcdCustomer, AcdChecking, AcdSavings, AcdLoan, AcdPersonal, AcdInstitute, AcdStudent, AcdHome, AcdInsurance, UserAuthEncrypt

'''
# Populate AcdSafeAcnt table - Checking
for i in range(1, 16):
    safe_acct = AcdSafeAcnt.objects.create(
        a_uid=i,
        acct_type='C',
        acct_name=f'Account {i}',
        a_street=f'Street {i}',
        a_city=f'City {i}',
        a_state='NY',
        a_zipcode='1000' + str(i),
    )
    safe_acct.save()

print("Polulated AcdSafeAcnt Table 'C'...")

# Populate AcdSafeAcnt table - Savings
for i in range(10, 25):
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

print("Polulated AcdSafeAcnt Table 'S'...")

# Populate AcdSafeAcnt table - Loan
for i in range(20, 35):
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

print("Polulated AcdSafeAcnt Table 'L'...")

# Populate AcdCustomer table
for i in range(1, 35):
    customer = AcdCustomer.objects.create(
        c_id=i,
        c_fname=f'CustFirstName{i}',
        c_lname=f'CustLastName{i}',
        c_street=f'CustStreet{i}',
        c_city=f'CustCity{i}',
        c_state='NY',
        c_zipcode='1000' + str(i),
        a_safe_acnt_id=i
    )
    customer.save()

print("Polulated AcdCustomer Table...")

# Populate AcdChecking table
for i in range(1, 16):
    checking_acct = AcdChecking.objects.create(
        a_safe_acnt_id=i,
        acct_no=1000000 + i,
        date_open=timezone.now(),
        serv_charge=20.00
    )
    checking_acct.save()

print("Polulated AcdChecking Table...")

# Populate AcdSavings table
for i in range(10, 25):
    savings_acct = AcdSavings.objects.create(
        a_safe_acnt_id=i,
        acct_no=2000000 + i,
        date_open=timezone.now(),
        intrst_rate=0.02
    )
    savings_acct.save()

print("Polulated AcdSavings Table...")

# Populate AcdLoan table
for i in range(20, 26):
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

print("Polulated AcdLoan Table 'SL'...")

# Populate AcdLoan table
for i in range(24, 31):
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

print("Polulated AcdLoan Table 'HL'...")

# Populate AcdLoan table
for i in range(30, 35):
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

print("Polulated AcdLoan Table 'PL'...")

# Populate AcdPersonal table
for i in range(30, 35):
    personal_loan = AcdPersonal.objects.create(
        a_safe_acnt_id=i,
        pl_uid=40000 + i,
        date_open=timezone.now()
    )
    personal_loan.save()

print("Polulated AcdPersonal Table...")

# Populate AcdInstitute table
institutes_data = [
    {'inst_code': 0, 'inst_name': 'University of New York'},
    {'inst_code': 1, 'inst_name': 'New York University'},
    {'inst_code': 2, 'inst_name': 'Columbia University'},
    {'inst_code': 3, 'inst_name': 'Cornell University'},
    {'inst_code': 4, 'inst_name': 'Stony Brook University'},
    {'inst_code': 5, 'inst_name': 'Harvard University'},
    {'inst_code': 6, 'inst_name': 'Arizona State University'},
    {'inst_code': 7, 'inst_name': 'Princeton University'},
    {'inst_code': 8, 'inst_name': 'Yale University'},
    {'inst_code': 9, 'inst_name': 'Stanford University'},
    {'inst_code': 10, 'inst_name': 'University of Cambridge'},
    {'inst_code': 11, 'inst_name': 'University of Oxford'},
    {'inst_code': 12, 'inst_name': 'MIT Boston'},
    {'inst_code': 13, 'inst_name': 'University of Chicago'},
    {'inst_code': 14, 'inst_name': 'UC, Berkeley'}
]

for data in institutes_data:
    institute = AcdInstitute.objects.create(**data)
    institute.save()

print("Polulated AcdInstitute Table...")
# Populated data till AcdInstitute Successfully!

# Populate AcdStudent table
for i in range(20, 26):
    student_loan = AcdStudent.objects.create(
        a_safe_acnt_id=i,
        sl_uid=50000 + i,
        date_open=timezone.now(),
        student_id=f'STUD00{i}',
        degree_type='Undergraduate',
        grad_month='May',
        grad_year=2024,
        inst_code_id= i % 15
    )
    student_loan.save()

print("Polulated AcdStudent Table...") # Done population successfully

# Populate AcdHome table
for i in range(24, 31):
    home_loan = AcdHome.objects.create(
        a_safe_acnt_id=i,
        hl_uid=60000 + i,
        date_open=timezone.now(),
        built_year=2010 + i
    )
    home_loan.save()

print("Polulated AcdHome Table...") # Done population successfully


# Populate AcdInsurance table
for i in range(24, 31):
    # Retrieve the corresponding AcdHome instance
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

print("Polulated AcdInsurance Table...")

# Username & Passwords for customers
for i in range(1, 35):
    customerUser = UserAuthEncrypt.objects.create(
        username=i,
        password=fernet.encrypt(('AbcXyz@' + str(i)).encode()),
        is_admin=False
    )
    customerUser.save()

print("Polulated UserAuthEncrypt Table - Customers...")

admin_user = UserAuthEncrypt.objects.create(
    username=1234567890,
    password=fernet.encrypt('admin123'.encode()),
    is_admin=True
)
admin_user.save()

admin_user = UserAuthEncrypt.objects.create(
    username=9999,
    password=fernet.encrypt('admin123'.encode()),
    is_admin=True
)
admin_user.save()

admin_user = UserAuthEncrypt.objects.create(
    username=99999,
    password=fernet.encrypt('admin123'.encode()),
    is_admin=True
)
admin_user.save()

print("Polulated UserAuthEncrypt Table - Admin...")
'''