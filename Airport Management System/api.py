from flask import *
from database import *

import demjson
import uuid

api=Blueprint('api',__name__)

@api.route('/login',methods=['get','post'])
def login():

	data={}

	uname=request.args['username']
	pword=request.args['password']

	q="SELECT * FROM login WHERE username='%s' AND password='%s'"%(uname,pword)
	res=select(q)

	if res:
		data['status']='success'
		data['data']=res
	else:
		data['status']='failed'

	data['method']='login'

	return demjson.encode(data)

@api.route('userregister',methods=['get','post'])
def userregister():

	data={}

	uname=request.args['uname']
	pword=request.args['pass']
	fname=request.args['fname']
	lname=request.args['lname']
	place=request.args['place']
	phone=request.args['phone']
	email=request.args['email']

	q="SELECT * FROM login WHERE username='%s' AND password='%s'"%(uname,pword)
	res=select(q)

	if res:
		data['status']='duplicate'
	else:
		q="INSERT INTO `login`(`username`,`password`,`usertype`)VALUES('%s','%s','user')"%(uname,pword)
		id=insert(q)
		q1="INSERT INTO `users`(`login_id`,`fname`,`lname`,`place`,`phone`,`email`)VALUES('%s','%s','%s','%s','%s','%s')"%(id,fname,lname,place,phone,email)
		ress=insert(q1)

		if ress:
			data['status']='success'
		else:
			data['status']='failed'

		data['method']='userregister'

	return demjson.encode(data)

@api.route('/view_hotels')
def view_hotels():

	data={}

	q="SELECT * FROM hotels INNER JOIN place USING(place_id)"
	res=select(q)
	if res:
		data['status']='success'
		data['data']=res
	else:
		data['status']='failed'

	data['method']='view_hotels'

	return demjson.encode(data)

@api.route('/view_flights')
def view_flights():

	data={}

	q="SELECT * FROM flights"
	res=select(q)
	if res:
		data['status']='success'
		data['data']=res
	else:
		data['status']='failed'

	data['method']='view_flights'
	
	return demjson.encode(data)

@api.route('/view_schedule')
def view_schedule():

	data={}

	q="SELECT * FROM `flight_schedule` INNER JOIN `flights` USING(flight_id) INNER JOIN `airports` ON `to_airport_id`=`airport_id`"
	res=select(q)

	if res:
		data['status']='success'
		data['data']=res
	else:
		data['status']='failed'

	data['method']='view_schedule'

	return demjson.encode(data)

@api.route('/view_tickets')
def view_tickets():

	data={}

	login_id=request.args['login_id']

	q="SELECT * FROM `ticketsbooked` INNER JOIN `flight_schedule` USING(schedule_id) INNER JOIN flights USING(flight_id) WHERE user_id=(SELECT user_id FROM users WHERE login_id='%s')"%(login_id)
	res=select(q)

	if res:
		data['status']='success'
		data['data']=res
	else:
		data['status']='failed'

	data['method']='view_tickets'

	return demjson.encode(data)

@api.route('/view_flight_timing')
def view_flight_timing():

	data={}

	login_id=request.args['login_id']

	q="SELECT * FROM `flighttiming` INNER JOIN airports USING (airport_id) INNER JOIN `flight_schedule` USING(schedule_id) INNER JOIN flights USING(flight_id)"
	res=select(q)

	if res:
		data['status']='success'
		data['data']=res
	else:
		data['status']='failed'

	data['method']='view_flight_timing'

	return demjson.encode(data)

@api.route('/sent_message')
def sent_message():

	data={}

	login_id=request.args['loginid']
	message=request.args['message']

	q="INSERT INTO `message`(`sender_id`,`message`,`reply`)VALUES((SELECT user_id FROM users WHERE login_id='%s'),'%s','pending')"%(login_id,message)
	res=insert(q)

	if res:
		data['status']='success'
	else:
		data['status']='failed'

	data['method']='sent_message'

	return demjson.encode(data)


@api.route('/view_message')
def view_message():

	data={}

	login_id=request.args['loginid']

	q="SELECT * FROM `message` WHERE `sender_id`=(SELECT user_id FROM users WHERE login_id='%s')"%(login_id)
	res=select(q)

	if res:
		data['status']='success'
		data['data']=res
	else:
		data['status']='failed'

	data['method']='view_message'

	return demjson.encode(data)

@api.route('/sent_feedback')
def sent_feedback():

	data={}

	login_id=request.args['login_id']
	feedback=request.args['feedback']

	q="INSERT INTO `feedback`(`user_id`,`feedback`,`date`)VALUES((SELECT user_id FROM users WHERE login_id='%s'),'%s',CURDATE())"%(login_id,feedback)
	res=insert(q)

	if res:
		data['status']='success'
	else:
		data['status']='failed'

	data['method']='sent_feedback'

	return demjson.encode(data)

@api.route('/viewfeedback')
def viewfeedback():

	data={}

	login_id=request.args['login_id']

	q="SELECT * FROM `feedback` WHERE `user_id`=(SELECT user_id FROM users WHERE login_id='%s')"%(login_id)
	res=select(q)

	if res:
		data['status']='success'
		data['data']=res
	else:
		data['status']='failed'

	data['method']='viewfeedback'

	return demjson.encode(data)

@api.route('/book_room')
def book_room():

	data={}

	hotel_id=request.args['hotel_id']

	q="SELECT * FROM `rooms` INNER JOIN hotels USING(hotel_id) WHERE hotel_id='%s'"%(hotel_id)
	res=select(q)

	if res:
		data['status']='success'
		data['data']=res
	else:
		data['status']='failed'

	data['method']='book_room'
	return demjson.encode(data)

@api.route('/user_payment',methods=['get','post'])
def user_payment():

	data={}

	booking_id=request.args['booking_id']
	amount=request.args['amount']

	q="INSERT INTO `payment`(`booked_id`,`amount`,`date`,`type`)VALUES('%s','%s',CURDATE(),'room')"%(booking_id,amount)
	res=insert(q)

	if res:
		data['status']='success'
	else:
		data['status']='failed'
	data['method']='user_payment'
	return demjson.encode(data)

@api.route('/Ticket_booking',methods=['get','post'])
def Ticket_booking():

	data={}
	loginid=request.args['loginid']
	schedule_id=request.args['schedule_id']
	passengers=request.args['passengers']
	amount=request.args['amount']
	q="INSERT INTO `ticketsbooked`(`schedule_id`,`amount`,`noofpassengers`,`booked_status`,`user_id`)VALUES('%s','%s','%s','pending',(SELECT user_id FROM users WHERE login_id='%s'))"%(schedule_id,amount,passengers,loginid)
	res=insert(q)

	if res:
		data['status']='success'
	else:
		data['status']='failed'

	data['method']='Ticket_booking'
	return demjson.encode(data)

@api.route('/luggage_information',methods=['get','post'])
def luggage_information():

	data={}

	booked_id=request.args['booked_id']
	weight=request.args['weight']
	details=request.args['details']

	q="INSERT INTO `luggage_info`(`booked_id`,`total_weight`,`details`,`status`)VALUES('%s','%s','%s','pending')"%(booked_id,weight,details)
	res=insert(q)

	if res:
		data['status']='success'
	else:
		data['status']='failed'
	data['method']='luggage_information'
	return demjson.encode(data)

@api.route('/flight_payment',methods=['get','post'])
def flight_payment():

	data={}

	booking_id=request.args['booking_id']
	amount=request.args['amount']

	q="INSERT INTO `payment`(`booked_id`,`amount`,`date`,`type`)VALUES('%s','%s',CURDATE(),'flight')"%(booking_id,amount)
	insert(q)
	q="UPDATE `ticketsbooked` SET `booked_status`='paid' WHERE `booked_id`='%s'"%(booking_id)
	update(q)
	data['status']='success'
	
	data['method']='flight_payment'

	return demjson.encode(data)

@api.route('/Passport_details',methods=['get','post'])
def Passport_details():

	data={}

	booked_id=request.form['booked_id']
	fname=request.form['fname']
	lname=request.form['lname']
	phone=request.form['phone']
	email=request.form['email']
	dob=request.form['dob']
	gender=request.form['gender']
	hname=request.form['hname']
	place=request.form['place']
	country=request.form['country']
	passport_no=request.form['passport_no']
	validity_date=request.form['vdate']

	image1=request.files['image1']
	path1='static/passport_details/'+str(uuid.uuid4())+image1.filename
	image1.save(path1)

	image2=request.files['image2']
	path2='static/passport_details/'+str(uuid.uuid4())+image2.filename
	image2.save(path2)

	q="INSERT INTO `passengers`(`booked_id`,`first_name`,`last_name`,`phone`,`email`,`dob`,`gender`,`house_name`,`place`,`country`,`passport_no`,`validity_date`,`image1`,`image2`,`status`)VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','pending')"%(booked_id,fname,lname,phone,email,dob,gender,hname,place,country,passport_no,validity_date,path1,path2)
	res=insert(q)

	if res:
		data['status']='success'
	else:
		data['status']='failed'

	data['method']='Passport_details'

	return demjson.encode(data)