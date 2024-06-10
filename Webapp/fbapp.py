import datetime
from firebase_admin import credentials, firestore, initialize_app, storage, auth
import firebase_admin
from typing import List, Dict, Tuple, Optional
from argon2 import PasswordHasher
import json
ph = PasswordHasher()


with open('Creds/config.json') as f:
    config = json.load(f)

storage_loaction = config['storageBucket']+"/images"


# * old method for firebase
# import pyrebase
# firebase = pyrebase.initialize_app(config)
# firebase_storage = firebase.storage()
# firebase_auth = firebase.auth()

# # * Set up a credential
# cred = credentials.Certificate(r"Creds\firestore-creds.json")
# initialize_app(cred)
# db = firestore.client()

# * new method for firebase using firebase_admin
cred = credentials.Certificate(r"Creds\firestore-creds.json")
firebase = firebase_admin.initialize_app(credential=cred, options=config)
firebase_storage = storage.bucket()
firebase_auth = auth
db = firestore.client()


def get_locations(collection, document):
    images_retrieved = (
        db.collection(collection).document(document).get().to_dict()["images"]
    )
    locations = [image["location"] for image in images_retrieved]
    return locations


def create_user(collection, display_name, uid, password):
    print("creating New User...")
    db.collection(collection).document(uid).set(
        {
            "uid": uid,
            "name": display_name,
            "images": [],
            "password": ph.hash(password),
        }
    )


def get_name_from_uid(collection, uid):
    return db.collection(collection).document(uid).get().to_dict()["name"]


def create_form_data(
    image_type="Xray",
    image_path="static/sample/covid4.png",
    description="This is a sample description",
    id="patient1",
    diagnose="Covid",
):
    filename = image_path.split("/")[-1]
    data = {
        "image_type": image_type,
        "description": description,
        "id": id,
        "filename": filename,
        # "filename": id + "_" + filename.split(".")[1],
        "location": storage_loaction + "/" + filename,
        "diagnose": diagnose,
    }
    return data, image_path


def search_similar_images(images, filename):
    for idx, image in enumerate(images):
        if image["filename"] == filename:
            return idx, True
    return -1, False


def updateDB(
    collection,
    document,
    data,
    upload_path,
    create_new_user=False,
):
    results = db.collection(collection).document(document).get()
    if results.exists:
        images = results.to_dict()["images"]

        filename = data["filename"]
        # cloud_path = "images/" + filename
        cloud_path = f"images/{document}/" + filename
        
        idx, image_found = search_similar_images(images, filename)
        firebase_storage.blob(cloud_path).upload_from_filename(upload_path)

        if image_found:
            images[idx] = data
            print("Image Updated")
        else:
            images.append(data)
            print("Image Added")

        db.collection(collection).document(document).update({"images": images})
    else:
        print("Document does not exist")
    # if create_new_user:
    #     create_user(collection, document, document)
    #     updateDB(collection, document, data, upload_path)
    #     print("New User Created")


def create_timed_url(location, document):
    filename = location.split("/")[-1]
    blob = firebase_storage.blob(f"images/{document}/" + filename)
    expiration = datetime.datetime.now() + datetime.timedelta(minutes=60)
    timed_url = blob.generate_signed_url(expiration=expiration, version="v4")
    return timed_url


def requestDB(collection, document):
    all_data = db.collection(collection).document(document).get().to_dict()["images"]
    for item in all_data:
        item["url"] = create_timed_url(item["location"], document)
    db.collection(collection).document(document).update({"images": all_data})
    return all_data


def request_image_info(collection, document, filename):
    all_data = db.collection(collection).document(document).get().to_dict()["images"]
    for item in all_data:
        if item["filename"] == filename:
            return item
    return None 


def verify_password(collection, document, password):
    try:
        ph.verify(db.collection(collection).document(document).get().to_dict()["password"], password)
        return True
    except:
        return False



def login_fb(email):
    try:
        msg = firebase_auth.get_user_by_email(email)
        print("Authentication successful.")
    except firebase_auth.UserNotFoundError:
        msg = "User not found."
    except:
        msg = "Invalid Email or Password."
    return msg





def signup_fb(email, password, username):
    try:
        msg = firebase_auth.create_user(
            email=email, password=password, display_name=username
        )
        
        print("Signed in successfully")
    except firebase_auth.EmailAlreadyExistsError:
        msg = "User already exists."
    except:
        msg = "User already exists."

    return msg


def download(filename, document):
    download_path = f"static/download/downloaded.{filename.split('.')[-1]}"
    blob = firebase_storage.blob(f"images/{document}/{filename}")
    blob.download_to_filename(download_path)
    print("Image downloaded successfully.")
    return download_path
    
    
def delete_image(collection, document, filename):
    all_data = db.collection(collection).document(document).get().to_dict()["images"]
    for item in all_data:
        if item["filename"] == filename:
            print("found and deleting")
            all_data.remove(item)
        else:
            print("not found")
    db.collection(collection).document(document).update({"images": all_data})
    blob = firebase_storage.blob(f"images/{document}/{filename}")
    blob.delete()
    return all_data


if __name__ == "__main__":
    userid = '1WKqweFlcqVjNrRkXg01956jeZi2'
    crt_pwd = "password@k124"
    incrt_pwd = "incorretjml#"
    
    print(verify_password("Users", userid, incrt_pwd))
