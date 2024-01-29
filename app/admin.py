from django.contrib import admin
from .models import Student,User,IAF,Signed

class StudentAdmin(admin.ModelAdmin):
    pass

class SignedAdmin(admin.ModelAdmin):
    pass

class SignedInline(admin.TabularInline):
    model = Signed

class IAFAdmin(admin.ModelAdmin):
      inlines = [SignedInline]

class UserAdmin(admin.ModelAdmin):
      list_display = ["email","password"]
      

# Register your models here.
admin.site.register(Student,StudentAdmin)
admin.site.register(User,UserAdmin)
admin.site.register(IAF,IAFAdmin)
admin.site.register(Signed,SignedAdmin)