from flask import *
from database import *
import uuid


public=Blueprint('public',__name__)

@public.route('/')
def home():
	return render_template('home.html')
@public.route('/login/', methods=['GET', 'POST'])   
def login():
    if 'submits' in request.form: 
        uname = request.form['username']
        passw = request.form['password']
        q = "SELECT * FROM login WHERE username='%s' AND password='%s'" % (uname, passw) 
        res = select(q)
        print(res)
        if res:
            session['lid'] = res[0]['login_id']
            if res[0]['usertype'] == "admin":
                return redirect(url_for('admin.adminhome'))   
            if res[0]['usertype'] == "staff":
                q = "SELECT * FROM `staff` WHERE `login_id`='%s'" % res[0]['login_id']
                res2 = select(q)
                session['sid'] = res2[0]['staff_id']
                return redirect(url_for('staff.staffhome')) 
            if res[0]['usertype'] == "users": 
                q = "SELECT * FROM `users` WHERE `login_id`='%s'" % res[0]['login_id']
                res2 = select(q)
                session['uid'] = res2[0]['user_id']
                return redirect(url_for('users.usershome'))	
        else:
            return '''<script>alert('invalid username or password');window.location='/'</script>'''

    return render_template('login.html')

@public.route('/register/', methods=['GET', 'POST'])	
def register():
    if request.method == 'POST' and 'submit' in request.form:
        fname = request.form['fname'] 
        lname = request.form['lname'] 
        place = request.form['place']
        phone = request.form['phone'] 
        email = request.form['email']
        username = request.form['username']  
        password = request.form['password'] 
        images = request.files['images']
        path = "static/uploadimages/" + str(uuid.uuid4()) + images.filename
        images.save(path)
        q1="select * from users where fname='%s' and lname='%s' and email='%s'"%(fname,lname,email)
        res=select(q1)
        if res:
            return '''<script>alert('Already Registered');window.location='/register'</script>'''
        else:

            q = "INSERT INTO login VALUES(null, '%s', '%s', 'pending')" % (username, password)
            id = insert(q) 
            q = "INSERT INTO users VALUES(null, '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (id, fname, lname, place, phone, email, path) 
            insert(q)  
            return '<script>alert("Registration Success. Please Login");window.location="/"</script>'

    return render_template('usersregister.html')
			











		

	

	