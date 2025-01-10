import pyrebase

firebaseConfig = {

  "apiKey": "AIzaSyA_1u-yUULkNFOqngiStL3YLmQobHkDXrw",

  "authDomain": "skillsync-14532.firebaseapp.com",

  "projectId": "skillsync-14532",

  "storageBucket": "skillsync-14532.firebasestorage.app",

  "messagingSenderId": "394660088399",

  "appId": "1:394660088399:web:6e90ba87f6381217c2f83a",

  "measurementId": "G-115SYLPZ5V",

  "databaseURL": "https://skillsync-14532-default-rtdb.firebaseio.com/"

}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

def signup():
    email = input("Enter email: ")
    password = input("Enter password: ")
    try:
        user = auth.create_user_with_email_and_password(email, password)
        print("Successfully signed up")
    except:
        print("Email already exists")

def login():
    ... # code for login



answer = input("Are you a new user? [y/n]")   
if answer == 'yes':
    signup()
elif answer == 'n':
    login()
#comment
