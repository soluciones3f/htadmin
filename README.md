# htadmin
Simple web application to manage users in htpasswd files

In our company we use SVN and TRAc authentication throught htpasswd files. But unfortunatly we did not have a simple application to create users, or to allow the users to change theirs passwords.

That is the motivation of this application. To be used as CRUD for htpasswd file. And to allow a user to change their passwords. Currently it does not allow a user that forgot the password to recover it, but allow to use a new password if they want to change.

This app was made with python because it is a language that is pre-installed in Debian.
The app have to library dependencies, flask and passlib. Both dependencies can be installed with pip

The user who run the app should have read/write permission over the htpasswd file.
