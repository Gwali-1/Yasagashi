# YASAGASHI(house-hunting)

Before i began this project, the capstone. I knew i wanted to try something different. Something i didn't  do  in any of the projects submitted throughout this course. Something that will present a bit of a challenge and not make it feel like i was making another django app like others i made. And thats when it hit me to add file management to this project,specifically images.I wanted to involve an external service like firebase. The closest i had come to working with images  was during the commerce where i displayed images on the page by refrencing urls of images found on the internet. This time i wanted to handle user submittted images myself, store them and manage refrences to them in a database. So i decided to make an accomodation listing web applcation, where users find or  could list properties for sale or rent, add prices , locations , whether they came furnished or not  etc. I thought the application should also have filtering mechanisms to allow users to find specific listings quite easily and fast, say a filtering pannel where you could narrow down search results based on parameters like price-range, accomodation type (rent or sale ) or even look at listings in only a specific locations.
.I shall now go through the project step by step while addressing some design choices, reasons for using an external package(pyrebase), challenges faced and a general overview of how the application works and some of it's features. 

The resulting app as metioned above displays a list of accomodation listings  posted by users of the app. The index page where these listings are displayed are paginated to display 10 lisitngs per page. Every listing holds information such as its location, whether its for rent or sale, the price and links to the profile of user that posted (the user profile holds extra information about user such as email , phone etc). This feature to see user profile from listings is only possible if user has an account and is logged in ofcourse. The app has 2 modes for when a user is logged in and not. The app serves up the index page with listings. Users who are not logged in can use the app the same way minus certain features like adding lisitngs to favourites or viewing profiles of users who have posted accomadations.
Owners of listings have to abilty to view listings they made and remove them if they are no longer available too. 
users on the app have a profile page, where they can upload an image as a profile picture or use the default picture given a user upon registering for an account.
The application uses `googles firebase service` for storage  and authentication(email and password login). User generated files like profle pictures and pictures of acomadation listings are stored in a firebase storage bucket which has been configured with security rules to allow writes from only aunthenticated source.

Also with authentication using firebase, in addition to doing verification checks on the server against the database, users login details are authenticated using firebase authentication. Upon registering for an account, in addition to creating an entry in database as a user object, an account is created in the cloud so on logging in , user details is authenticated to exist and if correct , is logged in. I understand that it was also possible to just check for user details in database and authenticate there, but as i said earlier i wanted to involve a (Backend as a Service (BaaS) like firebase.So in addition to using their cloud storage i added user authentication.

In contrast to using the firebase admin SDK, i used `pyrebase` package, a python wrapper around the google firebase api which exposed methods that make it cleaner and easy to implement functionality which involve  user authentication and pushing files to your storage bucket . I used pyrebase for how easy and straight to the point it is. After reading the documentation i found on github i was completely sure that was what i wanted to go with.
Moving forward i shall discuss  the contents of various files in the poject and how the help in the overall functionality, like auth, storage, filtering of results in the front end etc.


## How to run application

The app can be run by first making sure all dependencies are available in the environment. The requirements to run this project are listed in the requirements.txt file in the project directory.
* run `pip install -r requirements.txt` to install all dependencies
after that make sure youre in main project directory where `manage.py` file exist  and
* run  `python manage.py runserver` in terminal. 





## main/\_\_init__.p
Starting from the \_\_init__.py file inside  the `main` directory. The contents of this file is executed first everytime the server is started. For this reason i  import the pyrebase module , set up and initialize the pyrebase objet with the firebase credentials i genrated when i created a firebase project and app to use for this project. There is code that basically opens a file (config.json) that contains details of my firebase app in the cloud and i read from the file as a json and pass it into the method for initializing the pyrebase object. With the prebase object returned, i can obtain the pyrebase auth object(auth) for authentication and storage object (storage) for pushing files to my storage bucket hosted on firebase and also getting details of uploaded files like urp paths to them.
So basically in this file i initialize the pyrebase object and generate the auth and storage objects which will be  used in my creation of accounts for users, authentication of credentials and also the storage object for uplaoding and storing the image files submitted by users per pyrebase documentation.





## urls.py
This is where url paths enpoints and various view functions that handle request to them are defined. We create a list of url patterns  and the view functions that handle them in a list obect with name urlpatterns. The paths defined here like `/login`  or `/profile_settings` are linked the the view function that handle them in the `views.py` module.

## views.py

The views.py contain mainly functionality for handle client request to the server. Here we define functions to handle request at specific routes in the app and return response to the client. There are various view functions for different url endpoints that handle request in this file. Some are decorated to handle request only  from users who are authenticated and some are also csrf protected. Database models from `models.py` file are imported here and are used to perform database transactions such as storing data collected from users or retrieving data to be returned to client in the functions.  some some of the view functions in this file include ... 

`index`
The `index` view function does only one thing and that is redirect user request to the `home` view function. 



`home`
The home view function handles both GET and POST requests. It is decorated with the `csrf_protect` decorator from the `django.views.decorators.csrf module`. This is because it handles post request from the client and this is to prevent cross site request forgery by ensuring a csrf token is included in the request. The `home` function handles request for both authenticated and unaunthenticated users. GET reques=t from users who are not signed in are handled the same as authenticated users. Difference is that response from unauthencated users exclude certain data like user favorited post and user profile information and this limits features in the front end.

POST request from users are handled in the same way for both instances. POST request sent to this view function is to filter lisitng results .POST request sent include directives on what type of filtering to be done, the user requesting and depending on what info is needed to filter results. POST is sent from the client as an AJAX call using javascript fetch api with the csrf token specified in the header and payload is added to the request body.
The post request is handled by the `handle_post` function which is imported from the `helpers.py` file where its defined. It loads the POST request body and based on the action key does the requiring filtering then returns a json object with filter results. Filter results are recieved and handled by  a fuction in the `script.js` file in `/static/main`  and then rendered for user in the view template.
The fact that there is a distinction of request handling in this view function for both authenticated and unauthticated users allows the app to be used my users even if they don't have an account or are not signed in while limiting some app features. 



`signup`

The signup view function handles request from users who want to register for accounts. GET request sent to the signup route hit this functions and an html file (register.html) is returned to allow user to submit required info via form. Registration form is submitted via post request. 
user info such as username, email and password is retrieved from the `request.POST` object and authenticated by checking for presence  validity, whether user account with submitted email already exist or if passwords do not match. If any of these fail,  a response with an error message is sent back to be displayed to user.


If checks passes, using the firebase `auth` object created in the `__init__` file and imported here. We create a user account on firebase with user email and password in a try except block in order to catch any excpeptions that arise and send appropriate error message back to user.
After creating firebase user account we store the firebase object returned from the expresson in the request session object under users username. This firebase object contains information about user account on firebase and most important a user token that will be used to perform operations like uplaoding files into storage bucket.
After firebase operations with the pyrebase auth object we also perform some database transactions on our server like creating a new entry into our user table and a profile for our user by also creating an entry into the `user_profile`  table using the `user` and `user_profile` model imported from the `models.py` module
If these operations are succesful , user is redirected to the profile view fuction which presents the `profile_settings.html` view template to allow user to edit profile settings, if exceptions is caught in the try block user is redirected to the signup page again with rendered error message. 




`signin`

The signin view functions  signs users in if authentication passes. User submit login credentials via login form rendered if user hit the signin route via GET request. Uset credentials are checked for presence even before there are authentcated against database. Then before credentials are authenticated using the auth object from pyrebase against firebase cloud we authenticate credentials against our databse first to verify if account exist with such credentials and also to avoid making an uncessary network call. If that passes we do an extra verificaion agains firebase auth system. After firebase authentication of user details we store firebase object returned into the session object to be used later fot other operations. 

If user credentials passes, request is redirected to the index view function which in turn sends users to the home view where listings are displayed. And if verification fails user is redirected back to signin form  again wth rendered error.




`profile_settings`

The profile_setings view function returns a `profile_settings.html` view template if user sends a GET request. The template presents a display of current state of the users profile such as, email, primary location, contact info  etc which can be edited and saved.
when a user edits and saves changes, this triggers a POST request to this view function. Again user submitted data is authenticated and checked for validity before user profile is updated with new information.

There are mainly two scenarios that are checked for in the view function if a POST request is submitted. POST request body is checked if user submitted a new profile picture, if not database is updated with other information submitted but if a profile image is included in user submission then in addition to updating database, we uplaod new image file into our firebase storage bucket. we pass in the  user token in the directive to uplad file. This is because in the firebase storage bucket rules , we only allow write request from authenticated user or source. Database transaction is performed with `transaction.atomic` context manager which ensures that in any case of a database exception, changes are rolled back and database entry is left unchanaged. Only when the block gets executed succesfully thus the return stament is hit is all profile changes written to database. This helps keeps database atomic and prevent database corruption. If user profile is updated succesfully , user is redirected back to the prfile settings page.This is decorated with the `login_required` decorator hence handles request from only authenticated users.




`profile`

Thee profile view function simply displays user profile information for a specific user. This view functions handles request for when authenticated users click on the user name displayed as path of listing information.Profile info for the user is retrieved from database and added to reasponse as context to be used to display user profile information.This is decorated with the `login_required` decorator hence handles request from only authenticated users.



`post`

GET request to the post route hits this view function which returns the `post.html` template view which has a form to allow users to submit accomadation post details such as images, prices etc.
When form is submitted, it is handled by this view fucntion. User details are checked and authenticated for validity. If this checks out, user submittted images are loaded from the `request.FILES` object and the uplaoded  to the storage bucket on firebase in a for loop incase user submitted multiple files. On every iteration a random sting is generated using acobination of 'user-listing' plus  current `date` and generated `uuid` number which is used as the image name in storage bucket. After uplaod we get url of uploaded file in the bucket and  append it to a list later to be converted to a formated list that can be split into seperate urls and sent to client to be displayed . This formatted list is stored in the databse as the lisitng url in the listing table. 
After firebase operation, database transactin is performed. Again this is done in a `trasaction.atomic` context block. We add a new entry into the listing table in the databse and then user is redireted back to the index/home page where they can see their newly added entry.This is decorated with the `login_required` decorator hence handles request from only authenticated users.
If case of error when submitting form like missing fields or required information, user is redirected back to form with a flash message showing error message.




`stared and unstar`

The stared and unstar view functions handle request from only authenticated users. A user has to have an account and logged in to be able to access this feature. Users can star listings they see which means the lisiting will be added to the users favourties. That is a new entry is created in the database under the `Listing_favourites` table and is linked to the user. Users can then later view all their stared lisitngs. The unstar view function on the other hand handles request tht removes stared listings from users favorites. POST request sent to these routes are done via ajax calls using the javascript fetch api. Also both of these routes are csrf protected.



`lisitng`

The listing view function handles request sent to the listing route which contain an integer url parameter. The parameter is grabbed in the view function and used as id to retrieve a particular listing and returns it.
This view function returns a view template which renders extra inforamtion about a lisitng such as all images associated with it, location and contact information of user who listed it.
This view fuction is hit usually  when user clicks  on a lisitng on the home page. This is not decorated with the `login_required` decorator because users both authenticated and not should be able to view information abaout a listing.

## helpers.py

The helpers.py contain utility fuctions that are abstarcted away from the views.py file. Fuctions like `hanndle_post` that is used in the home view fucntion to handle POST request sent to the route to filter rendered listings.
Also contains the `get_ad_count` function that calculates how many lisitings are available in a location and returns a dictionary of locations as keys and number of listings there as the value. This allows as to display the lisitng number for each location so users know. 

There is also the `authenticate_post_form` function which is used in the post view fuction to authenticate user submitted data before they are used. It involves checking for missing fields etc




## config.json and serviceAc.json

These are files that contain firbase authentication details. The contents of these files are used by the pyrebase module to establish connection with our firebase app in th cloud. Without these we cannot connect to our firebase account. The config.json contains a dictionary object which is what is mainly required.However there is an approach where you can authenticate your backend as a service account which means request from your server has admin priviledges. other than that you have to pass in user tokens in other to have request to firebse acknowledged. This is how it was done in this project for reasons to be explained in the problems faced session.









## admin.py
Database models from `models.py` module are imported here and registered so they can be visible and edited  in the django admin pannel. The app uses a total of 4 database models. There a `User` model which inherits from the abstract user class  and models for the lisitngs , user favourited listings etc 




## templates directory
This contains the various view templates that are rendered and handles by view functions in the `views.py` file. These templates use the `layout.html` as a base template.


## static directory
The static directory contains static files like css file and  javascript file called `script.js`. The js file contains logic that sends AJAX calls(like when user is filtering listings) to the backend and also  does document manipulation  such as displaying spinners or changing contents of html files in response to certain events.
The css files contain user defined styles in addition to bootstrap styles applied in html files .


##  Distinctiveness and Complexity

For reasons why i believe my project satisfies the distinctiveness and Complexity  requirements ,  the project is neither a social network nor a commerce site. I like to think of it in the category of accomadation and hotel. The app is fully mobile responsive and ofcourse is built with django. It uses a total of 4 database models and also incoorporate google's firebase  backend service to store and manage user generated files and login authentication.





## Problems faced and Challenges

* During developement i came, accross a a bug when i tried to use service account credentials by passing it in `config.json` dictionary object as indicated by the pyrebase documentaion.According to the docs  my server gets authenticated as admin and all security rules are ignored when request comes from the server but the `put` method that uplaods files to my storage bucket kept throwing an error coming from the pyrebase package source code. I was able to trace the error and was able to resolve it after researching it.I have made a pull request to the repository and im not sure when or whether it will be merged so for the purpose of this project and to prevent situations where others are not able to run the application , i did not authenticate server as an admin  which was my desired approach. This would have made it easier and safe for me knowing i had security rules that prevented request from any other source excpet my server .I therefore  have to pass token when perfoming actions. To indicate that request are authenticated. Token expire after an hour so in other to make sure , i always refresh tokens before making the request.


* Also i realized the server will not start when there was no interent connection when service account credentials was provided. My guess from the error messages is as part of the initialization process , pyrebase was making some network calls to firebase , perharps to verify details and this needed internet connection.This is only a problem if the app is run locally without network connection.

## For staff
The project requires a firebase app to be provisioned in firebase cloud to work. This will require setting up a firebase project and setting up storage and authentication but in other to make running of the project easy and prevent the need to create a firebase project all over agin i shall leave the conf.json file out of the gitignore file. This will allow the pyreabase package to succesfully initialize using the firebase app i created and also prevent certain error. There shall also be the `.env` file which contains some environmental variables like django secrete key , allowed host etc that are refrenced in the settings file.
