from flask import *
from database import *
staff=Blueprint('staff',__name__)

@staff.route('/staffhome')
def staffhome():
	return render_template('staffhome.html')

# @staff.route('/staffupdateflightsanddeparture',methods=['get','post'])
# def staffupdateflightsanddeparture():




@staff.route('/staffviewticketsbooked',methods=['get','post'])
def staffviewticketsbooked():
	data={}
	if 'bid' in request.args:

		bid=request.args['bid']
		fid=request.args['fid']
		q="update ticketsbooked set booked_status='Approve' where booked_id='%s'" %(bid)
		update(q)
		return redirect(url_for('staff.staffviewticketsbooked'))
	q = "SELECT `ticketsbooked`.*, `flight_schedule`.*,flights.*,passengers.*, `from_airport`.`name` AS `from_airport_name`, `to_airport`.`name` AS `to_airport_name` FROM ticketsbooked INNER JOIN flight_schedule USING(schedule_id)INNER JOIN `airports` AS `from_airport` ON `flight_schedule`.`from_airport_id` = `from_airport`.`airport_id` INNER JOIN `airports` AS `to_airport` ON `flight_schedule`.`to_airport_id` = `to_airport`.`airport_id` INNER JOIN passengers USING(booked_id) INNER JOIN flights USING(flight_id)"
	res=select(q)
	data['ticketsbooked']=res 	
	return render_template('staffviewticketsbooked.html',data=data)

@staff.route('/staffverifyluggage_info',methods=['get','post'])  
def staffverifyluggage_info():
	data={} 
	bid=request.args['bid'] 
	data['bid']=bid	
	if 'action' in request.args: 
		action=request.args['action']  
		luggageid=request.args['id']  
		bid=request.args['bid']
	else:
		action=None	

	if action=="approve": 
		q="update luggage_info set status='approve' where luggage_id='%s'" %(luggageid)           
		update(q) 
		return redirect(url_for('staff.staffverifyluggage_info',bid=bid)) 
		
	if action=="reject": 
		q="update luggage_info set status='reject' where luggage_id='%s'" %(luggageid)  
		update(q) 
		return redirect(url_for('staff.staffverifyluggage_info',bid=bid)) 
		



	q="select * from luggage_info where booked_id='%s'" %(bid) 
	res=select(q)
	data['luggage_info']=res 		

	return render_template('staffverifyluggage_info.html',data=data)  

@staff.route('/staffverifypassengerdetails',methods=['get','post']) 
def staffverifypassengerdetails():
	data={} 
	bid=request.args['bid'] 
	data['bid']=bid
	fid=request.args['fid']
	data['fid']=fid
	if 'action' in request.args:
		action=request.args['action'] 
		passengerid=request.args['id'] 
		bid=request.args['bid']
	else:
		action=None	

	if action=="approve": 
		q="update passengers set status='approve' where passengers_id='%s'" %(passengerid)           
		update(q) 
		return redirect(url_for('staff.staffverifypassengerdetails',bid=bid,fid=fid)) 
		
	if action=="reject": 
		q="update passengers set status='reject' where passengers_id='%s'" %(passengerid)  
		update(q) 
		return redirect(url_for('staff.staffverifypassengerdetails',bid=bid,fid=fid)) 
		
	q="select *,concat(first_name,' ',last_name) as names from passengers where booked_id='%s'" %(bid) 
	res=select(q)
	data['passengers']=res 		
	return render_template('staffverifypassengersdetails.html',data=data)  

@staff.route('/staffallocateseat',methods=['get','post']) 
def staffallocateseat():
	data={} 
	fid=request.args['fid']
	data['fid']=fid
	bid=request.args['bid']
	data['bid']=bid
	pid=request.args['pid']
	data['pid'] =pid
	pname=request.args['pname']
	data['names']=pname

	if 'actions' in request.args:
		action=request.args['actions'] 
		assignid=request.args['id'] 
	else:
		action=None 
	if action=="delete":
		q="delete from assignseat where assign_id='%s'" %(assignid)  
		delete(q)
		return redirect(url_for("staff.staffallocateseat",bid=bid,pid=pid,pname=pname,fid=fid))  
	
	if 'add' in request.form:
		# passengerid=request.form['passenger_id'] 
		seatid=request.form['seat_id'] 
		
		
	 
		q="insert into assignseat values(null,'%s','%s','accept')" %(pid,seatid)   
		insert(q) 
		return redirect(url_for('staff.staffverifypassengerdetails',bid=bid,fid=fid)) 	
	q="SELECT *,CONCAT(`first_name`,' ',`last_name`)AS NAMES FROM assignseat INNER JOIN passengers USING(passengers_id) INNER JOIN seats USING(seat_id) WHERE `passengers_id`='%s'"%(pid)
	print(q)
	res=select(q)
	data['viewseats']=res  


	 	
	q="select *,concat(first_name,' ',last_name) as names from passengers where booked_id='%s'" %(bid)	
	res=select(q)
	data['assignseat']=res  

	q="SELECT * FROM `seats` INNER JOIN `type` USING(`type_id`) INNER JOIN `flights` USING(`flight_id`) WHERE `flight_id`='%s' and seat_id Not in(select assignseat.seat_id from assignseat inner join seats where flight_id='%s')"%(fid,fid)
	print("seat",q)
	res=select(q)
	print(res)
	data['viewseat']=res   
	return render_template('staffallocateseat.html',data=data) 


@staff.route('/staffupdateflightarrival',methods=['get','post']) 
def staffupdateflightarrival():
	data={} 

	if 'action' in request.args: 
		action=request.args['action'] 
		scheduleid=request.args['id']  
	else:
		action=None
	if action=="arrival": 
		q="select * from staffallocate where staff_id=(select staff_id from staff where login_id='%s')" %(session['lid'])
		print(q)
		res=select(q)  
		if res:  
			q="SELECT * FROM `flighttiming` WHERE `schedule_id`='%s' and type='arrival'"%(scheduleid)
			rs=select(q)
			if rs:
				flash("Already Arrived")
				return redirect(url_for('staff.staffupdateflightarrival'))
			else:

				q="insert into flighttiming values(null,'%s','%s',curtime(),'arrival')"  %(scheduleid,res[0]['airport_id'])           
				insert(q) 
				flash("Arrived")
				return redirect(url_for('staff.staffupdateflightarrival'))  
	if action=="departure": 
		q="select * from staffallocate where staff_id=(select staff_id from staff where login_id='%s')" %(session['lid']) 
		res=select(q)
		if res:
			q="SELECT * FROM `flighttiming` WHERE `schedule_id`='%s' and type='departure'"%(scheduleid)
			rs1=select(q)
			if rs1:
				flash("Already departure")
				return redirect(url_for('staff.staffupdateflightarrival'))
			else:
				q="insert into flighttiming values(null,'%s','%s',curtime(),'departure')"  %(scheduleid,res[0]['airport_id']) 
				insert(q) 
				flash("Departure")
				return redirect(url_for('staff.staffupdateflightarrival'))   	
	
	q="SELECT * FROM `flight_schedule` INNER JOIN `flights` USING (`flight_id`) INNER JOIN (SELECT * FROM  (SELECT fname,`schedule_id`,`staff_id` AS fstaff FROM (SELECT `airports`.`name` AS fname,`airports`.`airport_id` AS fid,`schedule_id` FROM `flight_schedule` INNER JOIN `airports` ON (`flight_schedule`.`from_airport_id`=`airports`.`airport_id`))temp1 INNER JOIN `staffallocate` ON (`staffallocate`.`airport_id`=temp1.fid))temp5 INNER JOIN (SELECT tname,`schedule_id`,`staff_id` AS tstaff FROM (SELECT `airports`.`name` AS tname,`airports`.`airport_id` AS tid,`schedule_id` FROM `flight_schedule` INNER JOIN `airports` ON (`flight_schedule`.`to_airport_id`=`airports`.`airport_id`))temp2 INNER JOIN `staffallocate` ON (`staffallocate`.`airport_id`=temp2.tid))temp6 USING (`schedule_id`))tem3 USING (`schedule_id`)"   
	res=select(q)
	data['flighttime_id']=res 

	return render_template('staffupdateflightarrival.html',data=data)           	




@staff.route('/staffviewmessage',methods=['get','post']) 
def staffviewmessage():
	data={} 
	lg_id=session['lid']
	q="SELECT * FROM `message` INNER JOIN `users` ON `message`.`sender_id`=`users`.`login_id` WHERE `message`.`receiver_id`='%s'"%(lg_id)
	print(q)
	rs=select(q)
	data['msg']=rs

	j=0
	for i in range(1,len(rs)+1):
		if 'submit'+str(i) in request.form:
			reply=request.form['reply'+str(i)]
			print(rs[j]['message_id'])

			q="UPDATE `message` SET `reply`='%s' WHERE `message_id`='%s'"%(reply,rs[j]['message_id'])
			update(q)
			# flash("message send successfully")
			return redirect(url_for('staff.staffviewmessage'))
		j=j+1


	return render_template('staffviewmessage.html',data=data) 



# @staff.route('/verifyseats',methods=['get','post'])
# def verifyseats():
# 	data={}
# 	uid=request.args['uid']
# 	qa="select * from assignseat inner join seats using(seat_id) inner join type using(type_id) where user_id='%s'"%(uid)
# 	res=select(qa)
# 	data['view']=res
# 	if 'action' in request.args:
#     	action=request.args['action']
# 		id=request.args['id']
# 	else:
#     	action=None
# 	if action=='accept':
#     	q1="update assignseat set status='accept' where assign_id='%s'"%(id)
# 		update(q1)

# 	if action=='reject':
#     	q2="update assignseat set status='reject' where assign_id='%s'"%(id)
# 		update(q2)
# 		return '''<script>alert('updated);window.location=''</script>'''
