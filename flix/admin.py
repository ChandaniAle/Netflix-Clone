from django.contrib import admin
from . models import Movie,Video,Profile
# Register your models here.
from .models import PaymentStatus
admin.site.register(Movie)
admin.site.register(Video)
admin.site.register(Profile)
admin.site.register(PaymentStatus)
