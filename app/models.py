from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

choices = lambda *x : list(zip(x,x))

insti_choices = choices("IIT Bombay","IIT Delhi","IIT Kharagpur")
program_choices = ["btech","btech+mtech","mtech","phd"]

class Student(models.Model) : 
      user = models.OneToOneField("User" , on_delete=models.CASCADE , related_name="student" )
      name = models.CharField(max_length=30,null=False) 
      institution = models.CharField( choices=insti_choices , max_length=30  , null = False )
      branch = models.CharField( max_length=30 , null = False )
      year = models.IntegerField(null=False,choices=zip( range(1,6),range(1,6) ) )
      program = models.CharField(max_length= 15,null=False,choices=zip(program_choices,program_choices))
      rollno = models.CharField(max_length=30,null=True)
      minor = models.CharField(max_length=15)
      resume = models.FileField(null=False,upload_to="app/files")
      def __str__(self) -> str:
           return f"{self.name} - {self.user.email}"

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True) 
    username = models.CharField(unique=False,null=True,max_length=20)   
    def __str__(self) : return self.email  

class Signed(models.Model) : 
      iaf = models.ForeignKey("IAF",on_delete=models.CASCADE)
      student = models.ForeignKey("Student",on_delete=models.CASCADE)
      status = models.CharField( max_length = 30 , choices = choices("Unsigned","Signed","Accepted","Rejected") )
      class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['iaf', 'student'], name='iaf_student_combination'
            )
        ]

from django.db.models.functions import Now
class IAF(models.Model) : 
      title = models.CharField(max_length=50)
      company = models.CharField(max_length=50)
      sector = models.CharField(max_length=20)
      opening_date = models.DateTimeField( db_default=Now() )
      closing_date = models.DateTimeField( null = True )
      def __str__(self) : return f"{self.company} - {self.title[:10]}"
      

