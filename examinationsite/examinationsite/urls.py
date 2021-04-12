"""examinationsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from exam import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.Home, name = 'home'),
    url(r'^login', views.login_view, name = 'AdminLogin'),
    url(r'^logout', views.logout_view, name="logout"),
    url(r'^user_detail', views.Userdetail, name = 'UserDetail'),
    url(r'^add_test', views.Addtest, name = 'AddTest'),
    url(r'^add_question', views.Addquestion, name = 'AddQuestion'),
    url(r'^add_option', views.Addoption, name = 'AddOption'),
    url(r'^user/(?P<pk>\d+)/tests/', views.Testlist, name = 'TestList'),
    url(r'^user/(?P<user_pk>\d+)/test/(?P<pk>\d+)/detail/', views.Testdetail.as_view(), name = 'TestDetail'),
    url(r'^user/(?P<user_pk>\d+)/test/(?P<test_pk>\d+)/attempt/(?P<attempt>\d+)/question/(?P<pk>\d+)/', views.Questiondetail.as_view(), name = 'QuestionDetail'),
    url(r'^answer_reader/(?P<question_pk>\d+)/(?P<user_pk>\d+)/(?P<test_pk>\d+)/(?P<attempt>\d+)', views.answer_reader, name = 'AnswerReader'),
    url(r'^user/(?P<user_pk>\d+)/test/(?P<test_pk>\d+)/attempt/(?P<attempt>\d+)/score', views.Userinformation, name="UserInformation"),
    url(r'^user_list', views.Userlist, name = 'UserList'),
    url(r'^user/(?P<user_pk>\d+)/all_tests/', views.Alltests, name = 'AllTests'),
    url(r'^user/(?P<user_pk>\d+)/(?P<test_name>\w+)/attempt/(?P<attempts>\d+)/all_questions/', views.Allquestions, name = 'AllQuestions'),
    url(r'^option/create', views.OptionCreatePopup, name = "OptionCreate"),  
    url(r'^edit_question/(?P<question_id>\d+)', views.Editquestion, name = 'EditQuestion'),
    url(r'^edit_test/(?P<test_id>\d+)', views.Edittest, name = 'EditTest'),
    url(r'^admin', views.Adminpage, name = 'AdminPgae'),
    url(r'^all_test_list', views.Alltestlist, name = 'AllTestList'),
    url(r'^all_question_list', views.Allquestionlist, name = 'AllQuestionList'),
    url(r'^delete_test/(?P<test_id>\d+)', views.Deletetest, name = 'DeleteTest'),
    url(r'^delete_question/(?P<question_id>\d+)', views.Deletequestion, name = 'DeleteQuestion'),
]
