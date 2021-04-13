from django.shortcuts import render, get_object_or_404
from .models import Admin,UserDetail,Test,Question,UserAnswer
from .forms import UserDetailForm,TestForm,QuestionForm,OptionForm
from django.contrib.auth import authenticate,login,logout
from .decorators import admin_is_logged_in
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic.detail import DetailView
import random
from django.urls import reverse
from django import http
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist

def Home(request):
    return render(request,"exam/home.html")

def Adminpage(request):
    return render(request,"exam/admin_page.html")

def login_view(request):
    model = Admin
    if request.method == "POST":
        username = request.POST.get('Username')
        password = request.POST.get('Password')
        user = authenticate(request = request, username=username, password=password) 
        if user is not None:
            login(request,user)
            return redirect("AdminPgae")
        else:
            messages.add_message(request, messages.WARNING, "Invalid creadentials")
            return render(request,"exam/login.html")

    return render(request,"exam/login.html")


@admin_is_logged_in
def logout_view(request):
    logout(request)
    return redirect('home')


def Userdetail(request):
    model = UserDetail
    user_detail_form = UserDetailForm()
    if request.method == "POST": 
        user_detail_form = UserDetailForm(request.POST)
        if user_detail_form.is_valid():
            email = user_detail_form.cleaned_data.get('email')
            try:
                matched_user = UserDetail.objects.get(email=email)
                user = matched_user
            except UserDetail.DoesNotExist:
                user = user_detail_form.save()                
            return redirect('TestList',user.id)            
    else:  
        return render(request,"exam/user_detail.html",{'form':user_detail_form})
    return render(request,"exam/user_detail.html",{'form':user_detail_form})


@admin_is_logged_in
def Addtest(request): 
    test_form = TestForm()
    if request.method == "POST": 
        if 'continue-editing' in request.POST:
            test_form = TestForm(request.POST)
            if test_form.is_valid():
                test = test_form.save()
                return redirect("EditTest",test.id)    
        else:
            test_form = TestForm(request.POST)
            if test_form.is_valid():
                test_form.save()
                return redirect("AdminPgae")
    else: 
        return render(request,"exam/add_test.html",{'form':test_form})
    return render(request,"exam/add_test.html",{'form':test_form})


@admin_is_logged_in
def Edittest(request,test_id):
    model = Test
    test_id = model.objects.get(id = test_id)
    test_form = TestForm(instance=test_id)
    if request.method == "POST": 
        test_form = TestForm(request.POST,instance=test_id)
        if test_form.is_valid():
            test_form.save()
            return redirect("AdminPgae")
    else:
        return render(request,"exam/edit_test.html",{'form':test_form})
    return render(request,"exam/edit_test.html",{'form':test_form})

@admin_is_logged_in
def Addquestion(request): 
    question_form = QuestionForm()
    if request.method == "POST": 
        if 'continue-editing' in request.POST:
            question_form = QuestionForm(request.POST)
            if question_form.is_valid():
                question = question_form.save()
                return redirect("EditQuestion",question.id)
        else:
            question_form = QuestionForm(request.POST)
            if question_form.is_valid():
                question_form.save()
                return redirect("AdminPgae")             
    else: 
        return render(request,"exam/add_question.html",{'form':question_form})
    return render(request,"exam/add_question.html",{'form':question_form})

@admin_is_logged_in
def Editquestion(request,question_id):
    model = Question
    question_id = model.objects.get(id = question_id)
    question_form = QuestionForm(instance=question_id)
    if request.method == "POST": 
        question_form = QuestionForm(request.POST,instance=question_id)
        if question_form.is_valid():
            question_form.save()
            return redirect("AdminPgae")
    else:
        return render(request,"exam/edit_question.html",{'form':question_form})
    return render(request,"exam/edit_question.html",{'form':question_form})

@admin_is_logged_in
def Addoption(request):
    option_form = OptionForm() 
    if request.method == "POST": 
        option_form = OptionForm(request.POST)
        if option_form.is_valid():
            option_form.save()
    else: 
        return render(request,"exam/add_option.html",{'form':option_form})
    return render(request,"exam/add_option.html",{'form':option_form})


def Testlist(request,pk):
    model = Test
    all_test = Test.objects.all()
    context = {'all_test':all_test,'user_pk' : pk}
    return render(request,"exam/test_list.html",context)



class Testdetail(DetailView):
    model = Test
    context_object_name = 'test'

    def first_question(self):
        questions = self.object.questions.all()
        if not questions:
            return None
        return self.object.questions.all()[0]
    
    def total_questions(self):
        questions = self.object.questions.all()
        return questions.count()

    def total_time(self):
        total = 0
        all_questions = self.object.questions.all()
        for question in all_questions:
            time = question.max_time_in_sec
            total = time+total
        return total

    def get_context_data(self, **kwargs):
        context = super(Testdetail, self).get_context_data(**kwargs)
        context['user_pk'] = self.kwargs['user_pk']
        context['test_pk'] = self.kwargs['pk']
        return context 
    
    def get_attempts(self,**kwargs):
        user = UserAnswer.objects.filter(user = self.kwargs['user_pk'],test = self.kwargs['pk'])
        if user.exists():
            attempts = user.aggregate(Max('attempts'))['attempts__max']
            attempt = attempts+1
            return attempt
        else:
            attempt = 1
            return attempt


class Questiondetail(DetailView):
    model = Question
    context_object_name = 'question'
    
    def get_context_data(self, **kwargs):
        context = super(Questiondetail, self).get_context_data(**kwargs)
        context['user_pk'] = self.kwargs['user_pk'] 
        context['test_pk'] = self.kwargs['test_pk']
        context['attempt'] = self.kwargs['attempt']
        return context

def Alltests(request,user_pk):
    model = UserAnswer
    all_tests = UserAnswer.objects.filter(user = user_pk).values('test__test_name', 'attempts').distinct().order_by('test__test_name')
    context = {'all_tests':all_tests,'user_pk':user_pk}
    return render(request,"exam/all_tests.html",context)

def Allquestions(request, user_pk, test_name, attempts):
    all_questions = UserAnswer.objects.filter(user = user_pk, attempts = attempts,test__test_name = test_name)
    Total = sum(question.score for question in all_questions)
    context = {'all_questions':all_questions,'Total_score':Total,'user_pk':user_pk}
    return render(request,"exam/all_questions.html",context)


object_id_list = []
score_list = []
def answer_reader(request, question_pk, user_pk, test_pk, attempt):
    question = Question.objects.get(pk=question_pk)
    if request.method == 'POST':
        answers = request.POST.getlist('answer')
    user = UserDetail.objects.get(pk=user_pk)
    test_name = Test.objects.get(pk=test_pk)
    if request.method == 'POST':
        time_taken= request.POST.get('timer')
    correct_answer =list(question.correct_answer.values_list('option',flat=True))
    score = 0
    if answers == correct_answer:
        score = score+1
        score_list.append(correct_answer)
    else:
        score = 0
    UserAnswer.objects.create(question=question, user=user, answer=answers, test=test_name, attempts=attempt, time_taken=time_taken, score=score)

    object_id_list.append(question_pk)
    test=Test.objects.get(pk=test_pk)
    que=[]
    for question in test.questions.all().exclude(id__in=object_id_list):
        que.append(question)
    all_questions_list = que

    if not len(all_questions_list) == 0:
        random_pk = random.choice(all_questions_list)
        object_id_list.append(random_pk.pk) 
        next_question = reverse("QuestionDetail", kwargs={'pk': random_pk.pk,'user_pk':user_pk,'test_pk':test_pk,'attempt':attempt})
        return http.HttpResponseRedirect(next_question)
    else:
        object_id_list.clear()
        score_list.clear()
        return redirect("UserInformation",user_pk,test_pk,attempt)

def OptionCreatePopup(request):
    form = OptionForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        print(instance.pk,instance)
        return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "#id_options");</script>' % (instance.pk, instance))
        
    return render(request, "exam/add_option.html", {"form" : form})

@admin_is_logged_in
def Userlist(request):
    model = UserDetail
    all_user_detail = UserDetail.objects.all().order_by('-id')[:]
    context = {'all_user_detail':all_user_detail}
    return render(request,"exam/user_list.html",context)

@admin_is_logged_in
def Alltestlist(request):
    model = Test
    tests = model.objects.all().order_by('-id')[:]
    context = {'tests':tests}
    return render(request,"exam/all_test_list.html",context)

@admin_is_logged_in
def Allquestionlist(request):
    model = Question
    questions = model.objects.all().order_by('-id')[:]
    context = {'questions':questions}
    return render(request,"exam/all_question_list.html",context)

@admin_is_logged_in
def Deletetest(request, test_id):
    test = get_object_or_404(Test, id = test_id)
    matched_test = UserAnswer.objects.filter(test=test)
    if matched_test.count()==0:
        if request.method =="POST":
            test.delete()        
            return redirect('AllTestList')
        return render(request, "exam/delete_test.html")
    else:
        return render(request, "exam/not_delete_test.html")

@admin_is_logged_in
def Deletequestion(request, question_id):
    question = get_object_or_404(Question, id = question_id)    
    matched_question = Test.objects.filter(questions = question)
    if matched_question.count()==0:
        if request.method =="POST":
            question.delete()
            return redirect('AllQuestionList')
        return render(request, "exam/delete_question.html")
    else:
        return render(request, "exam/not_delete_question.html")


def Userinformation(request,user_pk,test_pk,attempt):
    all_questions = UserAnswer.objects.filter(user = user_pk, attempts = attempt,test = test_pk)
    user = UserDetail.objects.get(pk=user_pk)
    Total_score = sum(question.score for question in all_questions)
    context = {'user_info':user,'Total_score':Total_score,'user_pk':user_pk}
    return render(request,"exam/user_information.html",context)