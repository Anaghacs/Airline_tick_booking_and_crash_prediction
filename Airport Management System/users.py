from flask import *
from database import *
import uuid
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from flask_mail import Mail

users=Blueprint('users',__name__)
@users.route('/usershome')
def usershome():
	return render_template('usershome.html') 

@users.route('/usersbookticket', methods=['get', 'post'])
def usersbookticket():
    data = {}
    q2 = "select * from airports"
    r3 = select(q2)
    data['port'] = r3

    if 'search' in request.form:
        sdate = request.form['sdate']
        edate = request.form['edate']
        fname = request.form['fname']
        lname = request.form['lname']
        q1 = "SELECT *,aa.`name` AS fname,ab.`name` AS tname FROM `flight_schedule` fs,`flights` f,`airports` aa,`airports` ab WHERE fs.`flight_id`=f.`flight_id` AND fs.`from_airport_id`=aa.`airport_id` AND fs.`to_airport_id`=ab.`airport_id` AND start_date_time='%s' AND end_date_time='%s' AND aa.`name`='%s' AND ab.`name`='%s'" % (sdate, edate, fname, lname)
        print(q1,';//////////////////////////////////////////////////////////////////////////////////////////////////////')
        ra = select(q1)
        print(ra,'hbsdhcbcghjdbchjdbcjhdbchjbdhcbdhbchdbhjncb')
	
        if ra:
            data['viewss'] = ra
        else:
            data['nodata'] = 'No data'

    if 'action' in request.args:
        action = request.args['action']
        scheduleid = request.args['id']
    else:
        action = None

    if action == "bookticket":
        q = "delete from ticketsbooked where schedule_id='%s'" % (scheduleid)
        delete(q)
        return redirect(url_for('users.usersbookticket'))

    q = "SELECT *,aa.`name` AS fname,ab.`name` AS tname FROM `flight_schedule` fs,`flights` f,`airports` aa,`airports` ab WHERE fs.`flight_id`=f.`flight_id` AND fs.`from_airport_id`=aa.`airport_id` AND fs.`to_airport_id`=ab.`airport_id` "
    res = select(q)
    data['ticketsbooked'] = res
    return render_template('usersbookticket.html', data=data)


@users.route('/userbook',methods=['get','post']) 
def userbook():	
	data={}
	lg_id=session['lid']
	sid=request.args['sid'] 
	

	if 'action' in request.args:
		action=request.args['action'] 
		flightid=request.args['id']  
	else:
		action=None
	if action=="delete": 
		q="delete from booked where flight_id='%s'" %(flightid)  
		delete(q)
		return redirect(url_for('users.userbook'))  
	
	if 'add' in request.form: 
		
		total=request.form['total'] 
		noofpassengers=request.form['noofpassengers'] 

		q="insert into ticketsbooked values(null,'%s','%s','%s','pending','%s')" %(sid,total,noofpassengers,lg_id)    
		insert(q) 
		return redirect(url_for('users.userbook',sid=sid)) 

	q="SELECT *,aa.`name` AS fname,ab.`name` AS tname FROM `flight_schedule` fs,`flights` f,`airports` aa,`airports` ab WHERE fs.`flight_id`=f.`flight_id` AND fs.`from_airport_id`=aa.`airport_id` AND fs.`to_airport_id`=ab.`airport_id` AND`schedule_id`='%s'" %(sid)
	res=select(q)
	data['val']=res
	t_seat=res[0]['noofseats']
	print(t_seat)


	q="select *,aa.`name` AS fname,ab.`name` AS tname from ticketsbooked t,`flight_schedule` fs,`flights` f,`airports` aa,`airports` ab WHERE t.schedule_id=fs.schedule_id AND fs.`flight_id`=f.`flight_id` AND fs.`from_airport_id`=aa.`airport_id` AND fs.`to_airport_id`=ab.`airport_id` AND t.`schedule_id`='%s'" %(sid)
	res=select(q)
	data['booked']=res 	

	q="SELECT SUM(`noofpassengers`) AS va1 FROM `ticketsbooked` WHERE `schedule_id`='%s'"%(sid)
	ress=select(q)
	if ress[0]['va1']!=None:

		av=ress[0]['va1']
		print(av)
		av_seat=int(t_seat)-int(av)
		data['av_seat']=av_seat
		print(av_seat)
	else:
		data['av_seat']=t_seat

	
	return render_template('userbook.html',data=data) 

@users.route('/userpassengerdetails',methods=['get','post']) 
def userpassengerdetails():		
	data={}
	bid=request.args['bid']
	data['bid']=bid
	no_pas=request.args['no_pas']

	if 'action' in request.args:
		action=request.args['action']  
		passengerid=request.args['id'] 
	else:
		action=None
	if action=="delete":
		q="delete from passengers where passenger_id='%s'" %(passengerid) 
		delete(q)
		return redirect(url_for('users.userpassengerdetails',bid=bid))	


	if 'add' in request.form:
		# bookedid=request.form['booked_id'] 
		firstname=request.form['first_name'] 
		lastname=request.form['last_name'] 
		phone=request.form['phone']
		email=request.form['email']
		dob=request.form['dob']
		gender=request.form['gender']
		housename=request.form['house_name']
		place=request.form['place']
		country=request.form['country']
		passportno=request.form['passport_no']
		validitydate=request.form['validity_date']	
		image1=request.files['image1']
		path="static/uploadimages/"+str(uuid.uuid4())+image1.filename
		image1.save(path) 
		image2=request.files['image2']
		path2="static/uploadimages/"+str(uuid.uuid4())+image2.filename
		image2.save(path2)

		q="SELECT COUNT(`passengers_id`) AS ps FROM `passengers` WHERE `booked_id`='%s' HAVING COUNT(`passengers_id`)>='%s'"%(bid,no_pas)
		print(q)
		rd=select(q)
		print(rd)
		if rd:
			flash("No. Of Passengers Exceed..")
		else:
			q="INSERT INTO `passengers`(`booked_id`,`first_name`,`last_name`,`phone`,`email`,`dob`,`gender`,`house_name`,`place`,`country`,`passport_no`,`validity_date`,`image1`,`image2`,`status`)values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','pending')" %(bid,firstname,lastname,phone,email,dob,gender,housename,place,country,passportno,validitydate,path,path2)    
			insert(q)
			return redirect(url_for('users.userpassengerdetails',bid=bid,no_pas=no_pas)) 	



	
	q="select * from passengers where booked_id='%s'"%(bid)
	res=select(q) 
	data['passengers']=res 
	return render_template('userpassengerdetails.html',data=data)  	

@users.route('/usersuploadluggageinfo',methods=['get','post']) 
def usersuploadluggageinfo():		
	data={}	
	bid=request.args['bid'] 
	data['bid']=bid
	if 'action' in request.args:
		action=request.args['action'] 
		luggageid=request.args['id'] 
	else:
		action=None
	if action=="delete": 
		q="delete from luggage_info where luggage_id='%s'" %(luggageid) 
		delete(q)
		return redirect(url_for('users.usersuploadluggageinfo',bid=bid)) 	
	if 'add' in request.form:
		totalweight=request.form['total_weight']
		details=request.form['details']
		
		q="insert into luggage_info values(null,'%s','%s','%s','pending')" %(bid,totalweight,details)     
		insert(q) 
		return redirect(url_for('users.usersuploadluggageinfo',bid=bid)) 
	q=" SELECT * FROM luggage_info WHERE `booked_id`='%s'"%(bid)
	res=select(q) 
	data['luggage_info']=res 
	return render_template('usersuploadluggageinfo.html',data=data)  	

@users.route('/usersviewflights',methods=['get','post']) 
def usersviewflights():		
	data={}	

	q="select * from flights INNER JOIN flight_schedule using(flight_id)" 
	res=select(q)
	data['flights']=res 	
	q="select * from flight_schedule"  
	res=select(q) 
	data['flight_schedule']=res

	return render_template('usersviewflights.html',data=data)   

@users.route('/usersviewhotels',methods=['get','post']) 
def usersviewhotels():		 
	data={}	

	q="SELECT * FROM hotels INNER JOIN `place` USING(`place_id`) INNER JOIN `countries` USING(`country_id`)"  
	res=select(q) 
	data['hotels']=res 	
	return render_template('usersviewhotels.html',data=data) 	  


@users.route('/usersbookroom',methods=['get','post']) 
def usersbookroom():		
	data={}	
	hroomid=request.args['id']  
	data['hroom_id']=hroomid 
	if 'add' in request.form:  
		roomid=request.form['room_id'] 
		fromdate=request.form['fromdate']  
		print("fromdate",fromdate)   
		todate=request.form['todate'] 
		q="insert into bookroom values(null,(select user_id from users where login_id='%s'),'%s','pending','%s','%s')" %(session['lid'],roomid,fromdate,todate)   
		id=insert(q)  
		q="select * from rooms where room_id='%s'" %(roomid)
		res=select(q)
		rnt=res[0]['rate']
		date_format = "%Y-%m-%d"

		a = datetime.strptime(fromdate,date_format)
		b = datetime.strptime(todate,date_format )
		delta = b - a
		print("dif date",delta.days)

		print(rnt)
		tot_amount=rnt*delta.days
		data['tot_amount']=tot_amount
		print(tot_amount)

		return redirect(url_for('users.usersmakepayment',action="room",bid=id,amount=tot_amount)) 
	q="SELECT * FROM bookroom INNER JOIN `rooms` USING(`room_id`) INNER JOIN `payment` ON `bookroom`.`broom_id`=`payment`.`booked_id` WHERE `type`='room'"  	 
	res=select(q)  
	data['bookroom']=res  
	q="select * from rooms where hotel_id='%s'"%(hroomid) 
	res1=select(q)
	data['viewrooms']=res1
	return render_template('usersbookroom.html',data=data)          

@users.route('/userviewpendingseat',methods=['get','post']) 
def userviewpendingseat():		 
	data={}	

	q="select * from seats"   
	res=select(q) 
	data['seats']=res 	
	return render_template('userviewpendingseat.html',data=data)          


@users.route('/usersviewtickets',methods=['get','post']) 
def usersviewtickets():		 
	data={}	 
	lg_id=session['lid']

	if 'action' in request.args:
		action=request.args['action']
		sh_id=request.args['sh_id']
	else:
		action=None
	print(action)

	if action=="stat":
		q="SELECT * FROM `flighttiming` INNER JOIN `airports` WHERE `schedule_id`='%s'"%(sh_id)
		
		rsd=select(q)
		data['stat']=rsd
		# print("sfg"+str(rsd))

	q="SELECT *,aa.`name` AS fname,aa.airport_id as aaid,ab.airport_id as abid,ab.`name` AS tname FROM ticketsbooked t,`flight_schedule` fs,`flights` f,`airports` aa,`airports` ab WHERE t.schedule_id=fs.schedule_id AND fs.`flight_id`=f.`flight_id` AND fs.`from_airport_id`=aa.`airport_id` AND fs.`to_airport_id`=ab.`airport_id` AND `user_id`='%s'"%(lg_id)
	print(q)
	res=select(q)
	data['ticketsbooked']=res 


	return render_template('usersviewtickets.html',data=data)    
 

@users.route('/usersmakepayment',methods=['get','post']) 
def usersmakepayment():		
	data={}


	bid=request.args['bid']  
	data['bid']=bid
	amount=request.args['amount']
	data['amount']=amount

	action=request.args['action']

	if 'pay' in request.form:

		
		
		q="insert into payment values(null,'%s','%s',curdate(),'%s')" %(bid,amount,action)
		insert(q)

		q="update ticketsbooked set booked_status='Paid' where booked_id='%s'" %(bid)
		update(q)


		return '''<script>alert('Payment Successful');window.location='/users/usershome'</script>'''
	
	return render_template('make_payment.html',data=data)    
	

@users.route('/user_send_feedback',methods=['get','post']) 
def user_send_feedback():		 
	data={}	
	lg_id=session['lid']

	if 'feeds' in request.form:
		feedb=request.form['feedb']
		q="INSERT INTO `feedback` VALUES(NULL,(SELECT `user_id` FROM `users` WHERE `login_id`='%s'),'%s',NOW())"%(lg_id,feedb)
		insert(q)

	q="SELECT * FROM `feedback` WHERE `user_id`=(SELECT `user_id` FROM `users` WHERE `login_id`='%s')"%(lg_id)   
	print(q)
	res=select(q) 
	data['feed']=res 	
	return render_template('user_send_feedback.html',data=data)          



@users.route('/user_send_message',methods=['get','post']) 
def user_send_message():		 
	data={}	
	aaid=request.args['aaid']
	abid=request.args['abid']
	lg_id=session['lid']

	if 'msgs' in request.form:
		msg=request.form['msg']
		stf=request.form['stf']
		q="INSERT INTO `message` VALUES(NULL,'%s','%s','%s','NA') "%(lg_id,stf,msg)
		insert(q)

	q="SELECT distinct(staffallocate.staff_id) as ids,staff.login_id,CONCAT(staff.firstname,' ',staff.lastname) AS staff_name FROM `staffallocate` INNER JOIN `staff` USING(`staff_id`) WHERE `airport_id`='%s' OR `airport_id`='%s'"%(aaid,abid)
	print(q)
	res=select(q) 
	if res:
		rid=res[0]['login_id']
		print(rid)
		data['view_staffs']=res 

		q="SELECT * FROM `message` INNER JOIN `staff` ON `message`.`receiver_id`=`staff`.`login_id`  WHERE `message`.`sender_id`='%s' or `message`.`receiver_id`='%s'"%(lg_id,rid)	
		print(q)
		msg=select(q)
		data['msg']=msg
	return render_template('user_send_message.html',data=data)  

@users.route('/userbookseat', methods=['get', 'post'])   
def userbookseat():
    data = {}
    uid = request.args['uid']
    fid = request.args['fid']
    qa = "SELECT * FROM seats INNER JOIN type USING (type_id) WHERE flight_id='%s'" % fid
    res = select(qa)
    data['view'] = res
    if 'submit' in request.form:
        seat = request.form['seat']
        qb = "INSERT INTO assignseat VALUES(NULL, '%s', '%s', 'pending')" % (session['uid'], seat)
        insert(qb)
        return '''<script>alert('Seat added');window.location='usersviewtickets'</script>'''
    return render_template('userbookseat.html', data=data)


@users.route('/calcel_ticket', methods=['get','post'])
def calcel_ticket():
    id = request.args['id']
    qa = "DELETE FROM ticketsbooked WHERE booked_id='%s'" % (id)
    delete(qa)
    qb = "SELECT * FROM users WHERE login_id='%s'" % (session['lid'])
    res = select(qb)
    if res:
        print(res)
        session['uname'] = res[0]['fname']
        email = res[0]['email']
        print(email)
        msg = f"Hy {session['uname']}. Your cancellation of ticket has been confirmed. Refund will begin soon."
        try:
            gmail = smtplib.SMTP('smtp.gmail.com', 587)
            gmail.ehlo()
            gmail.starttls()
            gmail.login('projectsriss2020@gmail.com', 'vroiyiwujcvnvade')
        except Exception as e:
            print("Couldn't set up email!! " + str(e))

        msg = MIMEText(msg)

        msg['Subject'] = 'Cancellation Policy'

        msg['To'] = email

        msg['From'] = 'projectsriss2020@gmail.com'

        try:

            gmail.send_message(msg)
            print(msg)
            flash("EMAIL SENT SUCCESSFULLY")
            return redirect(url_for('users.usershome'))


        except Exception as e:
            print("COULDN'T SEND EMAIL", str(e))
            return redirect(url_for('users.usershome'))




