import json
import pyrebase
# # pyrebase initalization


with open("main/config.json","r") as f:
    firebaseConfig = json.load(f)
     
firebase = pyrebase.initialize_app(firebaseConfig)

firebase_auth = firebase.auth()
firebase_storage = firebase.storage()
    



