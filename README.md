# YASAGASHI

Before i began this project, the capstone. I knew i wanted to try something different. Something i didnt  do  in any of the projects submitted throughout this course. Something that will present a bit of a challenge and not make it feel like i was making another django app like others i made. And thats when it hit me to add file management to this project,specifically images.I wanted to involve an external service like using firebase, for the closest i had come to working with images  was during the commerce where i displayed images on the page by refrencing urls of images found on the internet. This time i wanted to handle user submittted images myself, store them and manage refrences to them in a database. So i decided to make an accomadation listing web applcation, where users could list properties for sale or rent, add prices , locations , whether they came furnished or not  etc. I thought the application should also have filtering mechanisms to allow users to find specific listings quite easily and fast, say a filtering pannel where you could narrow down search results based on parameters like price range, accomadation type (rent or sale ) or even look at listings in only a specific locations.
This was my idea for the capstone project and i happy i was able to bring it to live. I shall now take you through the project step by step while addressing some design choices, reasons for using an exteranl package , challenges faced and a general overview of how the application works and some of it's features. 

The resulting app as metioned above displays a list of accomodation listings  posted by users of the app. The index page where these listings are displayed are paginated to display 10 lisitngs per page. Every listing holds information such as its location, whether its for rent or sale, the price and links to the profile of user that posted (the user profile holds extra information about user such as email , phone etc). This feature to see user profile from listings is only possible if user has an account and is logged in ofcourse. The app has 2 modes for when a user is logged in and not. The app serves up the index page with listings. Users who are not logged in can use the app the same way minus certain features like adding lisitngs to favourites or viewing profiles of users who have posted accomadations.
owners of listings have to abilty to remove them if they are no longer available too. 
users on the app have a profile page, where they can upload an image as a profile picture or use the default picture given a user upon registering for an account.
The application uses `googles firebase service` for storage service and authentication(email and password login). User generated files like profle pictures and pictures of acomadation listings are stored in a firebase storage bucket which has been configured with security rules to allow writes from only aunthenticated source.

Also in addition to do verification checks on the server against the database, users login details are authenticated using firebase authentication. Upon registering for an account, in addition to creating an entry in database as a user object, an account is created in the cloud so on loggin in , user details is authenticated to exist and if correct , is logged in. I understand that it was also possible to just check for user details in database and authenticate there, but as i said earlier i wanted to involve a(Backend as a Service (BaaS) like firebase.So in addition to using their cloud storage i added user authentication.

In contrast to using the firebase admin SDK, i used `pyrebase service` , a python wrapper around the google firebase api which exposed methods that make it cleaner and easy to implement functionality which involve  user authentication and pushing files to your storage bucket . I used pyrebase for how easy and straight to the point it is . After reading the documentation i found on github i was completely sure that was what i wanted to go with.
Moving forward i shall discuss  the contents of various files in the poject and how the help in the overall functionality, like auth, storage, filtering of results in the front end etc.


## main/\_\_init__.p
Starting from the \_\_init__.py file inside  the `main` directory. The contents of this file is executed first everytime the server is started. For this reason i  import the pyrebase module , set up and initialize the pyrebase objet with the firebase credentials i genrated when i created a firebase project and app to use for this project. There is code that basically opens a file (config.json) that contains details of my firebase app in the cloud and i read from the file as a json and pass it into the method for initializing the pyrebase object. With the prebase object returned, i can obtain the pyrebase auth object(auth) for authentication and storage object (storage) for pushing files to my storage bucket hosted on firebase and also getting details of uploaded files like urp paths to them.
So basically in this file i initialize the pyrebase object and generate the auth and storage objects which will be  used in my creation of accounts for users, authentication of credentials and also the storage object for uplaoding and storing the image files submitted by users per pyrebase documentation.





## urls.py
This is where url paths  enpoints and various view functions that handle request to them are defined.We create a list of url patterns  and the view functions that handle them in a list obect with name urlpatterns. The paths defined here like `/login`  or `/profile_settings` are linked the the view function that handle them in the `views.py` module.

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

get request to the post route hits this view function which returns the post template view which has a form to allo users to submit accomadation post details such as images prices etc.

when form is submitted it is handles by this view fucntion. user deatils are checked and authenticated for validity. if this checks out , user submittted images are loaded from the `request.FILES` object and the uplaoded  to the storage ucket on firebase in a forloop incase user submitted multiple files. on every iteration a random sting is gerated using acobination of   'usetr-listing' plus  current date and generated uuid number which is used as  the image name in storage bucket. after uplaod we get url of uplaoded file in the bucket and add append it to a list later to be comverted to a formated list thatcan be split into seperate urls and sent to client to be displayed .

after firebase operaion , databse transactin is performed . agai this is done in a `trasaction.atomic` context block. we add a new entry into the listing table in the databse and then user is redireted bak to the index/ hoe page where they can see their newly added entry.This is decorated with the `login_required` decorator hence handles request from only authenticated users

if case of error when submitting form  like missing fields or requiref information , user is redirected back to form with a flash message showing error message




`stared and unstar`

The stared  and  unstar view functions handle request from only authenticated users. a user has to have an account and logged in to be able to acces this feature. users can star listings they see which means the lisitng will be adde dto the users favourties. that is a new entry is created in the database under the `Listing_favourites` table and is linked to the user. users can then later view all thier stared lisitngs. the unstar view function on the other hand handles request tht removes stared listings from users favorites. post request sent to these routes are done via ajax calls using the javascript fetch api.



`lisitng`

the listing view function handles request sent to the lisiting route which contain an integer url parameter. the parameter is grabbed in the view functions and used as id to  retrieve a particular listing and return it.
this view function returns a view template which renders extra inforamtion about a lisitng such as all images associiated eith it , loacation and contact information of user who listed it .
This view fuction is hit usually  when user clicks  on a lisitng on the home page. This is not decorated with the `login_required` decorator becaue users both authenticated and not should be able to view information abaout a listing.

## helpers.py

the helpers.py contain utility fuctions that are abstarcted away from the views.py file. fucntions like `hanndle_post` that is used in the home view fucntion to hadle post request sent to the route to filter rensered listings 

also contains the a`add_count` fucntion that calculates how many lisitings are available in every location and returns a dictionaty of loacations as keys and number of listings there as the value. This allows as to display the lisitng account for each location so users know 


there is also the `authenticat_post_form` fuction which is used in  the post view fuction to authenticate user submitted data before they are used. it involves checking for missing fields etc




## config.json and serviceAc.json

these are files that contain firbase authentivation details . the contents of these files are used by the pyrebase module to establish connection with our firebas eapp in th cloud. without these we canot connect to our firebase account. the config.json contains a dictioanry object which is what is aminly required.however there is an approach where you can authenticate your backend as a service account which means request from your server has admin priviledges. this was you done have to pass in user tokens in other to have request to firebse acknowledged.






however during developemnt i ca, accrossa a bug when i try to use service account credentials by passing it in config.json dictionary object. my server gets authenticated as admin but the `put` method  that uplaods files to my storage bucket kept throwing an error coming from the pyrebase package source code  . i traced the error and was able to resolve it after researching it. i have made a pull request to the repository and im not usre when or whether it will be merged so for the purpose of this profect . is shall not authenticate as an admin and shall pass token when perfoming actions . this is to prevent insatnces where bugs are reproduced when the app is run by others 





## admin.py

database models from `models.py` module are imported here and registered so they can be visible and edited  in the django admin pannel




## templates directory
this contains the various view templates that are rendered and handles by view functions in the `views.py` file


## static directory
the static directory contains statics files like css file and  javascript file called `script.js`. the js file contains logic that sends AJAX calls to the backend and also document manuupulations code such as displaying spinners or changing contents of html files

the css files contain user defined styles in addition to bootsrap styles applied in html files 
