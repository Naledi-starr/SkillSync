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
db = firebase.database()

# Firebase Authentication
def signup(email, password, name, role, expertise=None):
    user = auth.create_user_with_email_and_password(email, password)
    db.child("Users").child(user["localId"]).set({
        "name": name,
        "email": email,
        "role": role,
        "expertise": expertise
    })
    return "Signup successful!"

def login(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        return user["idToken"], user["localId"]
    except:
        return None, None

# Firebase Database Operations
def fetch_users(role, expertise=None):
    users = db.child("Users").order_by_child("role").equal_to(role).get()
    if expertise:
        users = [user for user in users if user.val().get("expertise") == expertise]
    return users

def save_meeting(mentor_id, peer_id, meeting_time):
    db.child("Meetings").push({
        "mentor_id": mentor_id,
        "peer_id": peer_id,
        "time": meeting_time.isoformat(),
        "status": "pending"
    })

def fetch_meetings():
    return db.child("Meetings").get()

def cancel_meeting(booking_id):
    db.child("Meetings").child(booking_id).remove()