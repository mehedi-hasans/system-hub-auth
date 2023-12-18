from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailBackEnd(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else: 
            if user.check_password(password):
                return user
        return None
    




# class EmailBackEnd(ModelBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         UserModel = get_user_model()
        
#         # Use filter instead of get to handle multiple objects
#         users = UserModel.objects.filter(email=username)

#         # Check if there is exactly one user with the given email
#         if users.exists() and users.count() == 1:
#             user = users.first()
#             if user.check_password(password):
#                 return user
#         return None