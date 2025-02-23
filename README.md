# Social Media Application

A simple social media application built with Django that allows users to create, read, update, and delete posts.

## Installation

1. Clone the repository, run the following command in your terminal

    git clone https://github.com/ancientfahad/DJA01_Social_Media_Application_BRD.git

2. cd DJA01_Social_Media_Application_BRD

3. pipenv shell

4. cd social_media

5. pip install Pillow

6. pip install django-widget-tweaks

7. python manage.py makemigrations

8. python manage.py migrate

9. python manage.py runserver

## Features

- User authentication (register, login, logout)
- CRUD (Create, Read, Update and Delete posts)
- Upload images with posts
- View all posts on the homepage
- Personal profile page with user's posts
- Responsive design using Bootstrap, CSS

## Test Credentials

Regular Users:
- Username: testuser1
- Password: testpass123

Admin User:
- Username: admin
- Password: admin

If admin credentials don't work, try creating a new admin user using the following command in the terminal:

python manage.py createsuperuser