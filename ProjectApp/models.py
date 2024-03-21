from django.db import models

# Create your models here.
class Product(models.Model):
    
    NAME_CHOICES = [
        ("70","70"),
        ("125","125"),
    ]

    Name = models.CharField(db_column='Name',
                            max_length=50, 
                            null=False, 
                            default="")
    Rate = models.IntegerField(db_column='Rate', 
                               blank=True, 
                               null=True)
    Bike_Type = models.CharField(max_length=15,
                                 db_column='Bike Type', 
                                 choices=NAME_CHOICES, 
                                 blank=True, 
                                 null=True)
    def __str__(self):
        return self.Name

class Logistics(models.Model):
    Name = models.CharField(db_column='Name',
                            max_length=50, 
                            null=False)
    Contact_Num = models.CharField(db_column='Contact Number',
                                   max_length=100, 
                                   null=True, 
                                   blank=True)
    Email = models.CharField(db_column='Email', 
                             max_length=50, 
                             null=True, 
                             blank=True)
    Contact_prsn = models.CharField(db_column='Contact Person', 
                                    max_length=50, 
                                    null=False)
    Address = models.CharField(max_length=100, 
                               db_column='Address', 
                               null=True,
                               blank=True)
    def __str__(self):
        return self.Name

class Client(models.Model):
    Name = models.CharField(db_column='Name', 
                            max_length=50, 
                            null=False)
    Email = models.EmailField(db_column='Email', 
                              max_length=254,
                              null=True, 
                              blank=True)
    Contact_Num = models.CharField(db_column='Contact Number',
                                   max_length=100, 
                                   null=True, 
                                   blank=True)
    Company = models.CharField(db_column='Company', 
                               max_length=100, 
                               null=True, 
                               blank=True)
    Address = models.CharField(max_length=100, 
                               db_column='Address', 
                               null=True,
                               blank=True)
    def __str__(self):
        return self.Name

class Package(models.Model):
    City = models.CharField(db_column='City', 
                            max_length=10, 
                            null=False, 
                            blank=False)
    Num_of_Boxes = models.IntegerField(db_column='Num Of Boxes', 
                                       blank=True, 
                                       null=True)
    payorderDate = models.DateField(auto_now=True)
    DeliveryDate = models.DateField(null=True)
    Receivername = models.CharField(db_column='Name of Receiver', 
                                    max_length=50, 
                                    null=True, 
                                    blank=True)
    Status = models.CharField(db_column='Status', 
                              max_length=10, 
                              null=True, 
                              blank=True)
    #TODO: Check Cardinality
    Client = models.ForeignKey(Client, 
                               db_column='Client', 
                               on_delete=models.CASCADE)
    Logistics = models.ForeignKey(Logistics, 
                                  db_column='Logistics Company', 
                                  on_delete=models.DO_NOTHING, 
                                  null=True, 
                                  blank=True)
    Instructions = models.CharField(db_column='Instructions', 
                                    max_length=250, 
                                    null=True, 
                                    blank=True)
    

class AssociatedProducts(models.Model):
    Package = models.ManyToManyField(Package,
                                     db_column='Package')
    Product = models.ManyToManyField(Product, 
                                     db_column='Product')
    Quantity = models.IntegerField(db_column='Quantity', 
                                   blank=True, 
                                   null=True)