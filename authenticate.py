from firebase import firebase
from app import f
result = firebase.get('/users', None, {'print': 'pretty'})
print result

authentication = firebase.FirebaseAuthentication('THIS_IS_MY_SECRET', 'ozgurvt@gmail.com', extra={'id': 123})
firebase.authentication = authentication
print authentication.extra

user = authentication.get_user()
print user.firebase_auth_token


result = firebase.get('/users', None, {'print': 'pretty'})
print result

