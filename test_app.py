import pytest
from app import app, db, User, RegisterForm, Tasks
from datetime import date


@pytest.fixture
def client():

    # === Configure for testing === #
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # temporary database used
        "WTF_CSRF_ENABLED": False  # disable CRF protecting for testing
    })

    # === Create database tables === #
    with app.app_context():
        db.create_all()

    # === Create test client === #
    with app.test_client() as client:
        yield client  # allows setup before tests and cleanup after tests


# ======== Tests ======== #
# ===== Test 1 - Registration ===== #
def test_registration_user(client):
    """Test to check if a user is able to register with correct details"""

    response = client.post("/register", data={
        "username": "testuser",
        "email": "test-user@gmail.com",
        "password": "password123"
    }, follow_redirects=True)  # redirect to avoid 302 status code

    assert response.status_code == 200  # checks that the response status is 200 (success)


# ===== Test 2 - Registration ===== #
def test_registration_invalid(client):
    """Test to check if a user is unable to register with not unique email address"""

    with app.app_context():
        form = RegisterForm(data={
            "username": "Testuser2",
            "email": "test-user@gmail.com",
            "password": "password123"
        }, follow_redirects=True)

        assert form.validate() is False
        assert "That email address already exists. Please choose a different one." in form.email.errors


# ===== Test 3 - Login ===== #
def test_login_invalid(client):
    """Test to check if a user is unable to login with incorrect details"""

    with client.application.app_context():
        user = User(username="testuser", password="password123")
        db.session.add(user)
        db.session.commit()

    response = client.post("/login", data={
        "username": "testuser",
        "password": "wrongpassword"
    }, follow_redirects=True)

    assert response.status_code == 200
    user = User.query.filter_by(password="wrongpassword").first()
    assert user is None


# ===== Test 4 - Login ===== #
def test_login_valid(client):
    """Test to check if a user is able to login with correct details"""

    with client.application.app_context():
        user = User(username="testuser", email="test-user@gmail.com", password="password123")
        db.session.add(user)
        db.session.commit()

    response = client.post("/login", data={
        "username": "testuser",
        "password": "password123"
    }, follow_redirects=True)

    assert response.status_code == 200
    user = User.query.filter_by(username="testuser").first()
    assert user is not None


# ===== Test 5 - Create Task ===== #
def test_create_task(client):
    """Test creating a new task"""

    # == Login user == #
    client.post("/login", data={
        "username": "testuser",
        "password": "password123"
    })

    # == Create task == #
    response = client.post("/tasks/new", data={
        "title": "Test Task",
        "description": "Testing task creation",
        "priority": "Low",
        "due_date": "2026-03-10",
        "status": "To Do"
    }, follow_redirects=True)

    print("STATUS:", response.status_code)

    with app.app_context():
        task = Tasks.query.filter_by(title="Test Task").first()
        assert task is not None


# ===== Edit task ===== #
def test_edit_task(client):
    """Test editing a task"""

    # == Login user == #
    client.post("/login", data={
        "username": "testuser",
        "password": "password123"
    })

    # == Create a new task to be edited == #
    task = Tasks(
        title="Test Task",
        description="Testing task creation",
        priority="Low",
        due_date=date(2026, 3, 10),
        status="To Do",
        user_id=3
    )

    db.session.add(task)
    db.session.commit()

    # == Update task  == #
    response = client.post(f"/tasks/{task.id}/edit", data={
        "title": "Updated Task",
        "description": "Updated description",
        "priority": "High",
        "status": "In Progress",
        "due_date": "2026-03-15"
    }, follow_redirects=True)

    print("STATUS:", response.status_code)

    updated_task = db.session.get(Tasks, task.id)

    assert updated_task.title == "Updated Task"


# ===== Delete a task ===== #
def test_delete_task(client):
    """Test deleting a task"""

    # == Login user == #
    client.post("/login", data={
        "username": "testuser",
        "password": "password123"
    })

    # == Create a new task to be edited == #
    task = Tasks(
        title="Task to delete",
        description="Test deleting",
        priority="Low",
        due_date=date(2026, 6, 10),
        status="Completed",
        user_id=10
    )

    db.session.add(task)
    db.session.commit()

    # == delete task == #
    client.get(f"/tasks/{task.id}/delete", follow_redirects=True)

    deleted_task = db.session.get(Tasks, task.id)

    assert deleted_task is None


# ===== Read tasks ===== #
def test_read_tasks(client):
    """Test to check if a user is able to view their tasks"""

    # == Login user == #
    client.post("/login", data={
        "username": "testuser",
        "password": "password123"
    })

    # == Create a new task to be viewed == #
    task = Tasks(
        title="Task to view",
        description="Test viewing",
        priority="Medium",
        due_date=date(2026, 5, 10),
        status="In Progress",
        user_id=1
    )

    db.session.add(task)
    db.session.commit()

    response = client.get("/tasks", follow_redirects=True)

    assert response.status_code == 200
