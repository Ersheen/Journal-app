from flask import Flask, request, jsonify, session, redirect, url_for, Response, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS  # Optional, if doing cross-origin requests
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a strong secret key
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL").replace("postgresql://", "postgresql+psycopg://")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)  

# user database model
class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    mail = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)

# journal entries database
class Journal_entries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    month = db.Column(db.String(50), nullable=False)

    user = db.relationship('User', backref=db.backref('entries', lazy=True))


# route to send data to backend 
@app.route('/api/post_entries', methods=['POST'])
def add_entry():

    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized access'}), 401

    title = request.form.get('title')
    content = request.form.get('content')
    now = datetime.utcnow()
    month_name = datetime.utcnow().strftime('%B')  # e.g., 'July'

    new_entry = Journal_entries(title=title, content=content, user_id=session['user_id'], date=now, month=month_name)
    db.session.add(new_entry)
    db.session.commit()

    date_str = new_entry.date.strftime('%Y-%m-%d')
    return Response(status=204)
    # return f"""
    # <div class="about_journal">
    #     <div class="journal_title">
    #         <h3 class="head_title">{new_entry.title}</h3>
    #         <h5 class="date">{date_str}</h5>
    #     </div>
    #     <p class="journal_content">{new_entry.content}</p>
    # </div>
    # """


@app.route('/filter_journal_bydate', methods=['POST'])
def filtering_bydate():
    date_value = request.form.get('date_picker')
    query = Journal_entries.query.filter_by(user_id=session['user_id'])
    # if not date_value:
    #     return 'No date provided'
    if date_value:
        try:
            date_obj = datetime.strptime(date_value, '%Y-%m-%d')
            next_day = date_obj + timedelta(days=1)
            query = query.filter(
                Journal_entries.date >= date_obj,
                Journal_entries.date < next_day)
        except ValueError:
            return 'Invalid date format'

    journals = query.order_by(Journal_entries.date.desc()).all()
    html = ''
    for j in journals:
        date_str = j.date.strftime('%Y-%m-%d') if j.date else ''
        html += f"""
        <div class="about_journal">
            <div class="journal_title">
                <h3 class="head_title">{j.title}</h3>
                <h5 class="date">{date_str}</h5>
            </div>
            <p class="journal_content">{j.content}</p>
        </div>
"""
    return html



# signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return app.send_static_file('signup.html')
    else:
        name = request.form.get('name')
        mail = request.form.get('mail')
        password = request.form.get('password')

        if User.query.filter_by(mail=mail).first():
            return '<p>User already exists</p>'
        

        hashed_pw = generate_password_hash(password)
        new_user = User(name=name, mail=mail, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        response = make_response("", 204)
        response.headers["HX-Redirect"] = "/login"
        return response


    
# login route
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return app.send_static_file('login.html')

    else:
            mail = request.form.get('mail')
            password = request.form.get('password')

            user = User.query.filter_by(mail=mail).first()

            if user:
                session['user_id'] = user.id
            if user and check_password_hash(user.password, password):
                response = make_response("", 204)
                response.headers["HX-Redirect"] = "/dashboard"
                return response

            
            return '<p>Invalid credenials</p>'


# dashboard route
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return app.send_static_file('dashboard.html')


# logout route
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)  # Remove user ID from session
    return jsonify({'message': 'Logged out successfully', 'success': True})

# route to get journal entries
@app.route('/api/get_entries', methods=['GET'])
def get_notes():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized access'}), 401

    journals = Journal_entries.query.filter_by(user_id=session['user_id']).order_by(Journal_entries.date.desc()).all()
    html = ''
    for j in journals:
        date_str = j.date.strftime('%Y-%m-%d') if j.date else ''
        html += f"""
        <div class="about_journal">
                <div class="journal_title">
                    <h3 class="head_title">{j.title}</h3>
                    <h5 class="date">{date_str}</h5>
                </div>
                <p class="journal_content">{j.content}</p>
            </div>
        """
    return html

@app.route('/reset_journal', methods=['GET'])
def reset():
    journal = Journal_entries.query.filter_by(user_id=session['user_id']).order_by(Journal_entries.date.desc()).all()
    html = ''
    for j in journal:
        date_str = j.date.strftime('%Y-%m-%d') if j.date else ''
        html += f"""
    <div class="about_journal">
            <div class="journal_title">
                <h3 class="head_title">{j.title}</h3>
                <h5 class="date">{date_str}</h5>
            </div>
            <p class="journal_content">{j.content}</p>
        </div>
"""
    return html

@app.route('/view_journal') 
def view_journal():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return app.send_static_file('view_journal.html')



@app.route('/filter_by_keywords', methods=['POST'])
def filter_by_keyword():
    keyword = request.form.get('keyword_search')
    journals = Journal_entries.query.filter(
    Journal_entries.user_id == session['user_id'],
    db.or_(
        Journal_entries.title.ilike(f"%{keyword}%"),
        Journal_entries.content.ilike(f"%{keyword}%"))
        ).order_by(Journal_entries.date.desc()).all()
    
    html = ''
    for j in journals:
        date_str = j.date.strftime('%Y-%m-%d') if j.date else ''
        html += f"""
        <div class="about_journal">
            <div class="journal_title">
                <h3 class="head_title">{j.title}</h3>
                <h5 class="date">{date_str}</h5>
            </div>
            <p class="journal_content">{j.content}</p>
        </div>
"""
    return html

@app.route("/test-user")
def test_user():
    try:
        user = User.query.first()  # 🧪 Replace with your actual model name
        if user:
            return f"✅ First user email: {user.email}"
        else:
            return "✅ Connected to DB, but no users found."
    except Exception as e:
        print("❌ DB test error:", e)
        return f"❌ DB connection failed: {e}", 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)