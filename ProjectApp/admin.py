from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Product)
admin.site.register(Package)
admin.site.register(Client)
admin.site.register(Logistics)
admin.site.register(AssociatedProducts)