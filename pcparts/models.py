from django.db import models
# Create your models here.

class processor(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='pics')
    desc = models.TextField()
    price = models.IntegerField()
    offer = models.BooleanField(default=False)

class ram(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='pics')
    desc = models.TextField()
    price = models.IntegerField()
    offer = models.BooleanField(default=False)

class storage(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='pics')
    desc = models.TextField()
    price = models.IntegerField()
    offer = models.BooleanField(default=False)

class motherboard(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='pics')
    desc = models.TextField()
    price = models.IntegerField()
    offer = models.BooleanField(default=False)

class powersupply(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='pics')
    desc = models.TextField()
    price = models.IntegerField()
    offer = models.BooleanField(default=False)

class gpu(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='pics')
    desc = models.TextField()
    price = models.IntegerField()
    offer = models.BooleanField(default=False)

class cart(models.Model):
    pid=models.IntegerField(blank=False)
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='pics')
    desc = models.TextField()
    price = models.IntegerField()
    cid=models.IntegerField(blank=False)
    category=models.CharField(max_length=100)

class extendeduser(models.Model):
    #Flat, House no., Building, Company, Apartment
    addressline1=models.TextField(max_length=100)
    #Area, Colony, Street, Sector, Village
    addressline2=models.TextField(max_length=100)
    city=models.TextField(max_length=100)
    pincode=models.TextField(max_length=100)
    state=models.TextField(max_length=100)
    alternatemobile=models.TextField(max_length=100)
    cid=models.IntegerField(blank=False)

class review(models.Model):
     cid=models.IntegerField(blank=False)
     cname = models.CharField(max_length=100)
     pid=models.IntegerField(blank=False)
     pcategory=models.CharField(max_length=100)
     review = models.TextField()
