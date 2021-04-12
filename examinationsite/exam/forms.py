from django import forms  
from .models import UserDetail,Option,Question,Test
from itertools import chain
from django.contrib.admin.widgets import FilteredSelectMultiple

class UserDetailForm(forms.ModelForm): 
    def __init__(self, *args, **kwargs):
        super(UserDetailForm, self).__init__(*args, **kwargs)
        self.fields['mobile_number'].required = False

    class Meta:  
        model = UserDetail  
        fields = ('id', 'name', 'email', 'mobile_number',)
        error_messages = {
            'name': {
                'required': ("name can not be empty"),
            },
            'email': {
                'required': ("email can not be empty"),
            },
        }
        widgets = {
            'name' :forms.TextInput(
				attrs={
					'class': 'form-control',
                    }
                ),
            'email' :forms.EmailInput(
				attrs={
					'class': 'form-control',
                    }
                ),
            'mobile_number' :forms.TextInput(
				attrs={
					'class': 'form-control',
                    }
                ),
        }

class OptionForm(forms.ModelForm):  
    class Meta:  
        model = Option  
        fields = ('option',) 
        error_messages = {
            'option': {
                'required': ("can not be empty"),
            },
        }
        widgets = {
            'option' :forms.TextInput(
				attrs={
					'class': 'form-control',
                    }
                ),
        }

    # def clean_option(self):
    #     cleaned_data = self.cleaned_data
    #     field_name = cleaned_data.get('option')
    #     if len(field_name) < 3:
    #         field = 'option'
    #         error_message = "cannot be less than 3 charcaters"
    #         self.add_error(field, error_message)
    #     return field_name
   


class QuestionForm(forms.ModelForm):  

    class Meta:  
        model = Question  
        fields = ('question','question_type','options','correct_answer','max_time_in_sec',)
        error_messages = {
            'question': {
                'required': ("must add question"),
            },
            'question_type':{
                'required': ("atleast select one option"),
            },
            'options':{
                'required': ("atleast select one option"),
            },
            'correct_answer':{
                'required': ("atleast select one option"),
            },
            'max_time_in_sec':{
                'required': ("Add maximum time for your question"),
            },
        }
        widgets = {
            'question': forms.TextInput(
				attrs={
					'class': 'form-control',
                    }
                ),
            'question_type': forms.Select(
				attrs={
					'class': 'form-control',
					}
				),
            'options': forms.SelectMultiple(
				attrs={
					'class': 'form-control',
					}
				),
            'correct_answer': forms.SelectMultiple(
				attrs={
					'class': 'form-control',
					}
				),
            'max_time_in_sec': forms.NumberInput(
				attrs={
					'class': 'form-control',
					}
				),
			}

   
class TestForm(forms.ModelForm):  
    
    class Meta:  
        model = Test  
        fields = ('test_name','questions',)
        error_messages = {
            'test_name': {
                'required': ("must add test title"),
            },
            'questions':{
                'required': ("atleast select one option"),
            }
        }
        widgets = {
            'test_name': forms.TextInput(
				attrs={
					'class': 'form-control',
                    }
                ),
            'questions': forms.SelectMultiple(
				attrs={
					'class': 'form-control',
                    'id' : 'fruit_select',
					}
				),
			}
 
    


