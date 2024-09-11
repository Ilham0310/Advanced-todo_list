Todo List App
Overview

This is a simple Todo List App built with Flask, a micro web framework for Python. The app allows users to create, update, and delete todo tasks, and also provides in-app notifications for upcoming deadlines.

Features

User registration and login system
Create, update, and delete todo tasks
Task list display with due dates and categories
User-specific task list
In-app notifications for upcoming deadlines (3 days before due date)
How to Use

Installation
Clone the repository: git clone https://github.com/your-username/todo-list-app.git
Install the required packages: pip install -r requirements.txt
Create a new database file: sqlite:///mydb.db (or update the SQLALCHEMY_DATABASE_URI configuration)
Run the app: python app.py
Usage
Open a web browser and navigate to http://localhost:8000
If you're a new user, click on the "Register" link to create a new account. Fill out the registration form with your desired username and password.
Log in with your username and password
Create a new todo task by filling out the form on the homepage
Update or delete tasks by clicking on the "Update" or "Delete" links
The app will automatically send you in-app notifications 3 days before the due date of each task, reminding you to complete it on time.
Important: Logout After Use

Remember to logout after using the Todo List App to protect your account and tasks. This is crucial to prevent unauthorized access to your account. Note that simply closing the app or refreshing the page will not log you out, so it's essential to click on the "Logout" link to ensure your account is secure.

Why Logging Out is Important

If you don't log out, your account will remain active, allowing others to access your tasks and make changes without your permission.
Logging out ensures that your account is locked and secure, protecting your personal data and tasks.
Configuration
Update the database configuration in app.config to use a different database
Adjust the notification time frame by modifying the notification_time variable in the hello_world function
Notes
This app uses a SQLite database, which is not suitable for production use. Consider using a more robust database solution for a production environment.
Make sure to logout after using the app to protect your account and tasks.
The in-app notifications are only visible when you are logged in and viewing the task list.
I hope you find this Todo List App helpful