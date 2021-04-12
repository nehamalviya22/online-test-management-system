from django.db import models
from collectionfield.models import CollectionField

class Admin(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    
    def is_authenticated(self): 
        return False

class Option(models.Model):
    option = models.CharField(max_length=200,unique=True)
    
    def __str__(self):
        return "{}".format(self.option)

class Question(models.Model):
    question =models.CharField(max_length=200,unique=True)
    choice = (
        ('MC', 'multiple_choice'),
        ('TF', 'true_false'),
        ('FB', 'fill_in_the_blanks'),
    )
    question_type = models.CharField(max_length = 50, choices = choice)
    options = models.ManyToManyField(Option,blank = True )
    correct_answer = models.ManyToManyField(Option,related_name='correct_answer',blank = True )
    max_time_in_sec = models.PositiveIntegerField()
        

    def __str__(self):
        return (self.question)
    
    def get_options(Question):
        return ",".join([str(p) for p in Question.options.all()])

class Test(models.Model):
    test_name = models.CharField(max_length=60,unique=True)
    questions = models.ManyToManyField(Question)

    def __str__(self):
        return (self.test_name)


class UserDetail(models.Model):
    name = models.CharField(max_length = 50)
    email = models.EmailField(max_length = 50)
    mobile_number = models.CharField(max_length = 10)

    def __str__(self):
        return (self.name)


class UserAnswer(models.Model):
    user = models.ForeignKey(UserDetail)
    question = models.ForeignKey(Question)
    test = models.ForeignKey(Test)
    attempts =  models.PositiveIntegerField(default = 1)
    time_taken = models.PositiveIntegerField(default = 0)
    score = models.PositiveIntegerField(default = 0)
    answer = CollectionField()

    def __str__(self):
        return "{}".format(self.question)