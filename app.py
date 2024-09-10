from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mydb.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'testmy676@gmail.com'
app.config['MAIL_PASSWORD'] = 'clashofclans123'
app.config['MAIL_DEFAULT_SENDER'] = 'testmy676@gmail.com'

mail = Mail(app)

# Define the Todo model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('todos', lazy=True))

    def __repr__(self) -> str:
        return f"{self.title} - {self.category}"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self) -> str:
        return f"{self.username}"

@app.route("/send_email")
def send_email():
    try:
        msg = Message(
            "Hello from Flask",
            recipients=["ifhamhero123@gmail.com"]
        )
        msg.body = "This is a test email sent from a Flask web application!"
        msg.html = "<h1>This is a test email</h1><p>Sent from <strong>Flask</strong>!</p>"
        mail.send(msg)
        return "Email sent successfully!"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user is None or user.password != password:
            return "Invalid username or password", 401
        session["username"] = username
        return redirect(url_for("hello_world"))
    return render_template("login.html")

@app.route("/", methods=["GET", "POST"])
def hello_world():
    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]
    user = User.query.filter_by(username=username).first()
    if user is None:
        session.pop("username", None)
        return redirect(url_for("login"))

    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        due_date_str = request.form['due_date']
        # Convert due_date_str to a datetime object
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
        todo = Todo(title=title, category=category, due_date=due_date, user_id=user.id)
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.filter_by(user_id=user.id).all()
    notifications = []
    current_time = datetime.now()
    notification_time = timedelta(hours=72)  # 3 days before due date

    for todo in allTodo:
        time_left = todo.due_date - current_time
        if time_left <= notification_time and time_left > timedelta(0):
            notifications.append(f"Task '{todo.title}' is due soon on {todo.due_date.strftime('%Y-%m-%d')}.")

    return render_template("index.html", allTodo=allTodo, notifications=notifications)


   

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user:
            return "Username already exists", 400
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/logout")
def logout():
    if 'username' in session:
        session.pop('username', None)
    return redirect(url_for("login"))

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    todo = Todo.query.get_or_404(id)
    if request.method == "POST":
        todo.title = request.form.get("title")
        todo.category = request.form.get("category")
        due_date_str = request.form.get("due_date")
        # Convert due_date_str to a datetime object
        todo.due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
        db.session.commit()
        return redirect(url_for('hello_world'))
    return render_template('update.html', todo=todo)


@app.route("/delete/<int:id>")
def delete(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('hello_world'))

def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    create_tables()
    app.run(debug=True, port=8000)
