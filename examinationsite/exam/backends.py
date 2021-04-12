from .models import Admin
from django.contrib.auth.backends import ModelBackend

class AdminBackend(ModelBackend):    
    def authenticate(self, request, **kwargs):
        username = kwargs['username']
        password = kwargs['password']
        try:
            user = Admin.objects.get(name=username,password=password)
            if user:
                user.is_authenticated = True
                user.save()
                return user
        except Admin.DoesNotExist:
            pass    

    def get_user(self, user_id):
        try:
            return Admin.objects.get(pk=user_id)
        except Admin.DoesNotExist:
            return None
