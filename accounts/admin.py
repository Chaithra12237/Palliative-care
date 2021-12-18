from django.contrib import admin
from . models import *
# Register your models here.
admin.site.register(Users)
admin.site.register(Service)
admin.site.register(ProviderService)
admin.site.register(SubProduct)
admin.site.register(UserFavorite)
admin.site.register(Review)
admin.site.register(AdminMessage)
admin.site.register(AdminMessageStatus)