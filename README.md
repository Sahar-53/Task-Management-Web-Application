# Task Management Web Application

## Project Overview
This is a Flask-based task management web application. Users need to be registered to access the application. 
Once registered, users can log in to create, manage and delete the tasks. 
Users get an overview of their tasks i.e. Dashboard, where they can organise tasks by setting due dates, priority level and status. 
There is also a search feature for users to look up their tasks either by title or description. 
Moreover, users can also sort the tasks by due date, title or status. 
The application includes filtering options by status and priority to help users organise and manage tasks more effectively.

## Setup Instructions
1.	Clone the repository:
git clone https://github.com/Sahar-53/Task-Management-Web-Application
2. Create a virtual environment:
python -m venv venv
3. Activate the virtual environment:
venv\Scripts\activate
4.	Install dependencies:
pip install -r requirements.txt
5.	Set up the database:
Run the application once to initialise the database: python app.py
This will create the SQLite database and required tables
6.	Run the application:
python app.py

Next: open your browser and visit: http://127.0.0.1:5000

## Instruction for running tests
To run the automated test, execute the following in terminal:
pytest
This will run all the test cases defined in the test files. The tests cover following:
1. User registration with valid details
2. User registration with invalid details 
3. User login with valid details
4. User login with invalid details
5. Creating new tasks
6. Editing a task
7. Deleting a task
8. Retrieving tasks for a user

## Advanced features
#### User Authentication
Users can securely register and log in to access their personal task dashboard. password_hash() is used to store users’ password securely. 
Users register with their email address, username and password. However, to login they can use either username or email address.

#### Task Management
Users can view tasks, create new ones and edit or delete any current ones via Dashboard
Safe delete: users are prompted to confirm deletion for a task before deleting it.

#### Task Attributes:
Each task includes a title, description, due date, priority level, and status.
Actions: Next to every task, users can choose to edit or delete the task.
Search: Users can search for tasks by title or description.
Filter: Tasks can be filtered by their status and priority. There is also a button to clear the search or filter once it has been applied.
Sorting: Tasks can be sorted in ascending or descending order by title, due date, or status.
Priority colours: The priority level is colour-coded:
o	Green for Low
o	Amber for Medium
o	Red for High
When searching, creating or editing a task, users have the option to go back to the previous page.

#### Flash messages
The system displays feedback messages for actions such as invalid inputs for registrations and login, task creation and if due date is in the past.

#### Automated Testing
Unit tests were implemented using pytest to verify that the applications functions correctly.

## Known Issues or Limitations
The application currently uses SQLite, which may not scale well for larger production systems.
The user interface is basic and could be improved with additional styling or responsiveness.
