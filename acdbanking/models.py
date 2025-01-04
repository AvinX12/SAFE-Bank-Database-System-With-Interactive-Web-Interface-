from django.db import models

# SAFE Bank Accounts
class AcdSafeAcnt(models.Model):
    a_uid = models.BigIntegerField()
    acct_type = models.CharField(max_length=2)
    acct_name = models.CharField(max_length=30)
    a_street = models.CharField(max_length=30)
    a_city = models.CharField(max_length=30)
    a_state = models.CharField(max_length=2)
    a_zipcode = models.CharField(max_length=5)
    surrogate_key = models.AutoField(primary_key=True)

    class Meta:
        # managed = False
        # db_table = 'AcdSafeAcnt'
        unique_together = ('a_uid', 'acct_type')

# Customer Details
class AcdCustomer(models.Model):
    c_id = models.IntegerField(primary_key=True)
    c_fname = models.CharField(max_length=30)
    c_lname = models.CharField(max_length=30)
    c_street = models.CharField(max_length=30)
    c_city = models.CharField(max_length=30)
    c_state = models.CharField(max_length=2)
    c_zipcode = models.CharField(max_length=5)
    a_safe_acnt = models.ForeignKey(AcdSafeAcnt, on_delete=models.CASCADE, verbose_name='SAFE Unique Account', related_name='Customer_Info')

    '''
    class Meta:
        managed = False
        db_table = 'AcdCustomer'
    '''

    def getSAFEAcntDetails(self):
        return f"SAFE Unique Accound ID: {self.a_safe_acnt.a_uid}\tCustomer Unique ID: {self.c_id}"

# Checking Accounts
class AcdChecking(models.Model):
    a_safe_acnt = models.ForeignKey(AcdSafeAcnt, on_delete=models.CASCADE, verbose_name='SAFE Unique Account', related_name='Checking_Accounts')
    acct_no = models.BigIntegerField(unique=True)
    date_open = models.DateTimeField()
    serv_charge = models.DecimalField(max_digits=6, decimal_places=2)

    '''
    class Meta:
        managed = False
        db_table = 'AcdChecking'
    '''
        
    def getSAFEAcntDetails(self):
        return f"SAFE Unique Accound ID: {self.a_safe_acnt.a_uid}\tAccount Type: {self.a_safe_acnt.acct_type}"

# Savings Accounts
class AcdSavings(models.Model):
    a_safe_acnt = models.ForeignKey(AcdSafeAcnt, on_delete=models.CASCADE, verbose_name='SAFE Unique Account', related_name='Savings_Accounts')
    acct_no = models.BigIntegerField(unique=True)
    date_open = models.DateTimeField()
    intrst_rate = models.DecimalField(max_digits=4, decimal_places=2)

    '''
    class Meta:
        managed = False
        db_table = 'AcdSavings'
    '''
        
    def getSAFEAcntDetails(self):
        return f"SAFE Unique Accound ID: {self.a_safe_acnt.a_uid}\tAccount Type: {self.a_safe_acnt.acct_type}"

# Loan Accounts
class AcdLoan(models.Model):
    a_safe_acnt = models.ForeignKey(AcdSafeAcnt, on_delete=models.CASCADE, verbose_name='SAFE Unique Account', related_name='Loan_Accounts')
    acct_no = models.BigIntegerField()
    loan_type = models.CharField(max_length=2)
    loan_amt = models.DecimalField(max_digits=10, decimal_places=2)
    loan_rate = models.DecimalField(max_digits=4, decimal_places=2)
    loan_months = models.SmallIntegerField()
    loan_payment = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        # managed = False
        # db_table = 'AcdLoan'
        unique_together = ('acct_no', 'loan_type')
    
    def getSAFEAcntDetails(self):
        return f"SAFE Unique Accound ID: {self.a_safe_acnt.a_uid}\tAccount Type: {self.a_safe_acnt.acct_type}"

# Personal Loan - From Loan Accounts
class AcdPersonal(models.Model):
    a_safe_acnt = models.ForeignKey(AcdSafeAcnt, on_delete=models.CASCADE, verbose_name='SAFE Unique Account', related_name='Personal_Loan')
    pl_uid = models.IntegerField(unique=True)
    date_open = models.DateTimeField()

    '''
    class Meta:
        managed = False
        db_table = 'AcdPersonal'
    '''
        
    def getSAFEAcntDetails(self):
        return f"SAFE Unique Accound ID: {self.a_safe_acnt.a_uid}\tAccount Type: {self.a_safe_acnt.acct_type}"

# Institutes - For Student Loans
class AcdInstitute(models.Model):
    inst_code = models.IntegerField(primary_key=True)
    inst_name = models.CharField(max_length=30)

    '''
    class Meta:
        managed = False
        db_table = 'AcdInstitute'
    '''
    
# Student Loan - From Loan Accounts
class AcdStudent(models.Model):
    a_safe_acnt = models.ForeignKey(AcdSafeAcnt, on_delete=models.CASCADE, verbose_name='SAFE Unique Account', related_name='Student_Loan')
    sl_uid = models.FloatField(unique=True)
    date_open = models.DateTimeField()
    student_id = models.CharField(max_length=6)
    degree_type = models.CharField(max_length=13)
    grad_month = models.CharField(max_length=10)
    grad_year = models.SmallIntegerField()
    inst_code = models.ForeignKey(AcdInstitute, models.DO_NOTHING)

    '''
    class Meta:
        managed = False
        db_table = 'AcdStudent'
    '''
         
    def getSAFEAcntDetails(self):
        return f"SAFE Unique Accound ID: {self.a_safe_acnt.a_uid}\tAccount Type: {self.a_safe_acnt.acct_type}"

# Home Loan - From Loan Accounts
class AcdHome(models.Model):
    a_safe_acnt = models.ForeignKey(AcdSafeAcnt, on_delete=models.CASCADE, verbose_name='SAFE Unique Account', related_name='Home_Loan')
    hl_uid = models.IntegerField(unique=True)
    date_open = models.DateTimeField()
    built_year = models.SmallIntegerField()

    '''
    class Meta:
        managed = False
        db_table = 'AcdHome'
    '''

    def getSAFEAcntDetails(self):
        return f"SAFE Unique Accound ID: {self.a_safe_acnt.a_uid}\tAccount Type: {self.a_safe_acnt.acct_type}"

# Insurance - For Home Loans
class AcdInsurance(models.Model):
    ins_acct_no = models.BigIntegerField(primary_key=True)
    ins_company = models.CharField(max_length=30)
    ins_street = models.CharField(max_length=30)
    ins_city = models.CharField(max_length=30)
    ins_state = models.CharField(max_length=2)
    ins_zipcode = models.CharField(max_length=5)
    yearly_prm = models.DecimalField(max_digits=8, decimal_places=2)
    hl_uid = models.ForeignKey(AcdHome, models.DO_NOTHING)

    '''
    class Meta:
        managed = False
        db_table = 'AcdInsurance'
    '''

# Login Details
class UserAuthEncrypt(models.Model):
    username = models.BigIntegerField(primary_key=True)
    password = models.BinaryField(null=False)
    is_admin = models.BooleanField(default=False, null=False)

    '''
    class Meta:
        managed = False
        db_table = 'UserAuth'
    '''

