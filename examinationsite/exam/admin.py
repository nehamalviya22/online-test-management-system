from django.contrib import admin
from exam.models import Admin,Option,Question,Test,UserDetail,UserAnswer

# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'get_options','question_type')

admin.site.register(Admin)
admin.site.register(Option)
admin.site.register(Question,QuestionAdmin)
admin.site.register(Test)
admin.site.register(UserDetail)
admin.site.register(UserAnswer)
