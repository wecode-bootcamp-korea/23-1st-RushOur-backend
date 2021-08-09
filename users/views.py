import json
import bcrypt
import jwt, re

from django.views          import View
from django.http           import JsonResponse

from users.models          import User
from rushour.settings      import SECRET_KEY
from users.utils           import login_required

def email_validation(email):
        p = re.compile('^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$')
        return not p.match(email)
        
def password_validation(password):
        p = re.compile('^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$')
        return not p.match(password)

        
class UserView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            if email_validation(email=data['email']): 
                return JsonResponse({"MESSAGE":"INVALID_EMAIL"}, status=400)
            
            if password_validation(password=data['password']): 
                return JsonResponse({"MESSAGE":"INVALID_PASSWORD"}, status=400)
                
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'MESSAGE' : 'EMAIL_ALREADY_EXISTS'}, status=400)

            if User.objects.filter(username=data['username']).exists():
                return JsonResponse({'MESSAGE' : 'USERNAME_ALREADY_EXISTS'}, status=400)
                
            if User.objects.filter(phone_number=data['phone_number']).exists():
                return JsonResponse({'MESSAGE' : 'PHONE_NUMBER_ALREADY_EXISTS'}, status=400)
                
            if User.objects.filter(name=data['name']).exists():
                return JsonResponse({'MESSAGE' : 'NAME_ALREADY_EXISTS'}, status=400)
                
            if User.objects.filter(nickname=data['nickname']).exists():
                return JsonResponse({'MESSAGE' : 'NICKNAME_ALREADY_EXISTS'}, status = 400)
                
            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                username     = data['username'],
                name          = data['name'],
                nickname      = data['nickname'],
                phone_number  = data['phone_number'],
                password      = hashed_password,
                email         = data['email'],
                address       = data['address'],
            )

            return JsonResponse({"MESSAGE" : "SUCCESS"}, status = 201)
        except KeyError:
            return JsonResponse({"MESSAGE" : "KEY_ERROR"}, status = 400)
            
class SigninView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            password = data['password']
            
            if not User.objects.filter(username=data['username']).exists():
                return JsonResponse({"MESSAGE" : "INVALID_USER"}, status=401)
                
            user = User.objects.get(username=data['username'])
            
            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'MESSAGE':'INVALID_USER'}, status=401)
                
            access_token = jwt.encode({'id' : user.id}, SECRET_KEY, algorithm = 'HS256')
            return JsonResponse({'MESSAGE':'SUCCESS', 'TOKEN': access_token },status=200)
        except KeyError:
            return JsonResponse({"MESSAGE" : "KEY_ERROR"}, status=400)