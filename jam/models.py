from django.db import models
from django.contrib.auth.models import User

class Jam(models.Model):
    Title = models.CharField(max_length=200)
    NoLines = models.IntegerField()
    Creator = models.ForeignKey(User,on_delete = models.CASCADE)
    Start_date = models.DateTimeField(auto_now_add = True)
    End_date = models.DateTimeField(null=True)
    cover=models.ImageField(upload_to="jam_covers/", default="jam_covers/cover.jpg")
    Status = models.BooleanField()

    def __str__(self):
	       return f"{self.id}. {self.Title}"

class JamLines(models.Model):
    Jamid=models.ForeignKey(Jam,on_delete=models.CASCADE,default=None)
    LineNo = models.IntegerField()
    Line = models.CharField(max_length = 100)
    Contributer = models.ForeignKey(User,on_delete = models.CASCADE)
    Date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
	       return f"{self.id}. {self.LineNo}. {self.Line}"
