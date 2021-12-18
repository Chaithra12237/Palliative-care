from django.db import models
from django.contrib.auth.models import User


# Create your models here.

gender = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Others', 'Others'),
)

states = (
    ('Andhra Pradesh','Andhra Pradesh'),
    ('Arunachal Pradesh','Arunachal Pradesh'),
    ('Assam','Assam'),
    ('Bihar','Bihar'),
    ('Chhattisgarh','Chattisgarh'),
    ('Goa','Goa'),
    ('Gujarat','Gujarat'),
    ('Haryana','Haryana'),
    ('Himachal Pradesh','Himachal Pradesh'),
    ('Jharkhand','Jharkhand'),
    ('Karnataka','Karnataka'),
    ('Kerala','Kerala'),
    ('Madhya Pradesh','Madhya Pradesh'),
    ('Maharashtra','Maharashtra'),
    ('Manipur','Manipur'),
    ('Meghalaya','Meghalaya'),
    ('Mizoram','Mizoram'),
    ('Nagaland','Nagaland'),
    ('Odisha','Odisha'),
    ('Rajasthan','Rajasthan'),
    ('Sikkim','Sikkim'),
    ('Tamil Nadu','Tamil Nadu'),
    ('Telangana','Telangana'),
    ('Tripura','Tripura'),
    ('Uttar Pradesh','Uttar Pradesh'),
    ('Uttarakhand','Uttarakhand'),
    ('West Bengal','West Bengal')
    )


user_type=(
    ('admin','admin'),
    ('service_provider','service_provider'),
    ('public','public'),
)

approval_choices=(
    ('2','Pending'),
    ('1','Approved'),
    ('3','Rejected')
)

class Users(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=200,null=True, blank=True)
    organization = models.CharField(max_length=250,null=True, blank=True)
    mob = models.CharField(max_length=12)
    sex = models.CharField(max_length=10,choices=gender,default='Male')
    house = models.CharField(max_length=100,null=True, blank=True)
    street1 =models.CharField(max_length=100,null=True, blank=True)
    street2 =models.CharField(max_length=100,null=True, blank=True)
    city = models.CharField(max_length=100,null=True, blank=True)
    district = models.CharField(max_length=100,null=True, blank=True)
    state = models.CharField(max_length=100,null=True,choices=states, blank=True)
    pin = models.CharField(max_length=100,null=True,blank=True)
    age = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=20,choices=user_type)
    approval = models.CharField(max_length=20,choices=approval_choices,default='Pending')
    document = models.FileField(upload_to='documents',null=True, blank=True)
    profile_picture = models.FileField(upload_to='dp',default='assets/img/user3.png')

    def __str__(self):
        return self.name

class Service(models.Model):
    category = models.CharField(max_length=250)
    providers = models.IntegerField(null=True, blank=True)
    users = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.category

class ProviderService(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE,null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE,null=True, blank=True)
    count = models.IntegerField(null=True, blank=True)
    cost = models.IntegerField()

    def __str__(self):
        return ("%s_%s") %(self.user,self.service)
    

class SubProduct(models.Model):
    service = models.ForeignKey(ProviderService, on_delete=models.CASCADE,null=True, blank=True)
    name = models.CharField(max_length=250)
    count = models.IntegerField(null=True, blank=True)
    cost = models.IntegerField()
    details = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class UserFavorite(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey(ProviderService, on_delete=models.CASCADE,null=True, blank=True)
    product = models.ForeignKey(SubProduct, on_delete=models.CASCADE,null=True, blank=True)

class Review(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey(ProviderService, on_delete=models.CASCADE,null=True, blank=True)
    product = models.ForeignKey(SubProduct, on_delete=models.CASCADE,null=True, blank=True)
    message = models.TextField()
    datetime = models.DateTimeField()

class Booking(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey(ProviderService, on_delete=models.CASCADE,null=True, blank=True)
    product = models.ForeignKey(SubProduct, on_delete=models.CASCADE,null=True, blank=True)
    booking_id = models.CharField(max_length=250)
    datetime = models.DateTimeField()
    amount_transferred = models.CharField(max_length=250)

class AdminMessage(models.Model):
    message = models.TextField()
    datetime = models.DateTimeField()

    def __str__(self):
        return self.message

class AdminMessageStatus(models.Model):
    message = models.ForeignKey(AdminMessage, on_delete=models.CASCADE,null=True, blank=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE,null=True, blank=True)
    status = models.BooleanField(default=False)











