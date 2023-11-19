from flask import *
from database import *
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle


admin=Blueprint('admin',__name__)

@admin.route('/adminhome')
def adminhome():
	return render_template('adminhome.html') 


@admin.route('/adminmanagestaff', methods=['GET', 'POST']) 
def adminmanagestaff(): 
    data = {}

    if 'action' in request.args:
        action = request.args['action'] 
        staffid = request.args['id'] 
    else:
        action = None

    if action == "delete":
        q = "DELETE FROM staff WHERE staff_id='%s'" % staffid 
        delete(q)
        return redirect(url_for('admin.adminmanagestaff'))	

    if action == 'update':
        qa = "SELECT * FROM staff WHERE staff_id='%s'" % staffid
        r2 = select(qa)
        data['upd'] = r2

    if 'update' in request.form:
        fname = request.form['fname'] 
        lname = request.form['lname'] 
        gender = request.form['gender'] 
        age = request.form['age']
        phone = request.form['phone'] 
        email = request.form['email'] 
        designation = request.form['designation'] 
        qd = "UPDATE staff SET firstname='%s', lastname='%s', gender='%s', age='%s', phone='%s', email='%s', designation='%s' where staff_id='%s'" % (fname, lname, gender, age, phone, email, designation,staffid)
        update(qd)
        return redirect(url_for('admin.adminmanagestaff'))

    if 'submit' in request.form: 
        fname = request.form['fname'] 
        lname = request.form['lname'] 
        gender = request.form['gender'] 
        age = request.form['age']
        phone = request.form['phone'] 
        email = request.form['email'] 
        designation = request.form['designation'] 
        usern = request.form['username'] 
        passw = request.form['password']  
        q = "INSERT INTO login VALUES(null, '%s', '%s', 'staff')" % (usern, passw)    
        id = insert(q) 
        q = "INSERT INTO staff VALUES(null, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (id, fname, lname, gender, age, phone, email, designation) 
        insert(q) 

    q = "SELECT * FROM staff" 
    res = select(q)
    data['staff'] = res 		

    return render_template('adminmanagestaff.html', data=data)  		


@admin.route('/adminmanagecountries',methods=['get','post']) 
def adminmanagecountries():
	data={}
	if 'action' in request.args:
		action=request.args['action'] 
		countryid=request.args['id'] 
	else:
		action=None
	if action=="delete":
		q="delete from countries where country_id='%s'" %(countryid)   
		delete(q)
		return redirect(url_for('admin.adminmanagecountries'))

	if action=="update":
		q="select * from countries where country_id='%s'" %(countryid) 
		res=select(q)
		data['updatecountries']=res
	if 'update' in request.form:
		countr=request.form['country']	
		q="update countries set country='%s' where country_id='%s'" %(countr,countryid) 
		update(q)
		return redirect(url_for('admin.adminmanagecountries')) 

	if 'submit' in request.form:
		countr=request.form['country']
		q="insert into countries values(null,'%s')" %(countr)   
		insert(q) 
		return redirect(url_for('admin.adminmanagecountries')) 
	q="select * from countries"	
	res=select(q) 
	data['countries']=res 
	return render_template('adminmanagecountries.html',data=data)   


@admin.route('/adminmanageplace',methods=['get','post']) 	
def adminmanageplace():
	data={} 
	if 'action' in request.args:
		action=request.args['action'] 
		placeid=request.args['id'] 
	else:
		action=None
	if action=="delete":
		q="delete from place where place_id='%s'" %(placeid) 
		delete(q)
		return redirect(url_for('admin.adminmanageplace')) 

	if action=="update":
		q="select * from place where place_id='%s'" %(placeid)  
		res=select(q)
		data['updateplace']=res
		q1="SELECT country_id,country,(country_id='%s') AS sel FROM countries ORDER BY sel DESC,country_id ASC" %(res[0]['country_id'])  
		res1=select(q1)
		data['updatecountries']=res1  
	if 'update' in request.form: 
		countryid=request.form['country_id'] 
		place=request.form['place'] 
		q="update place set country_id='%s',state_place='%s' where place_id='%s'" %(countryid,place,placeid)  
		update(q)
		return redirect(url_for('admin.adminmanageplace'))    	

	if 'add' in request.form: 
		countryid=request.form['country_id'] 
		place=request.form['place']
		q="insert into place values(null,'%s','%s')" %(countryid,place)  
		insert(q) 
		return redirect(url_for('admin.adminmanageplace')) 
	q="select * from place INNER JOIN countries using(country_id)" 	 

	res=select(q)
	data['place']=res  
	q="select * from countries"   
	res=select(q)
	data['country_id']=res   
	return render_template('adminmanageplace.html',data=data)   

@admin.route('/adminmanageairports',methods=['get','post'])	
def adminmanageairports():
	data={}
	if 'action' in request.args:
		action=request.args['action'] 
		airportid=request.args['id'] 
	else:
		action=None
	if action=="delete":
		q="delete from airports where airport_id='%s'" %(airportid) 
		delete(q)
		return redirect(url_for('admin.adminmanageairports'))
	if action=="update":
		q="select * from airports where airport_id='%s'" %(airportid)  
		res=select(q)
		data['updateairports']=res
		q1="SELECT place_id,country_id,place,(place_id='%s') AS sel FROM place ORDER BY sel DESC,place_id ASC" %(res[0]['place_id'])  
		res1=select(q1)
		data['updateplace']=res1



	if 'update' in request.form:
		placeid=request.form['place_id']
		name=request.form['name']	
		district=request.form['district'] 
		state=request.form['state'] 
		q="update airports set place_id='%s',name='%s',district='%s',state='%s' where airport_id='%s'" %(placeid,name,district,state,airportid) 
		update(q)
		return redirect(url_for('admin.adminmanageairports'))  


	if 'add' in request.form:
		placeid=request.form['place_id'] 
		name=request.form['name']
		district=request.form['district'] 
		state=request.form['state']
		q="insert into airports values(null,'%s','%s','%s','%s')" %(placeid,name,district,state)    
		insert(q) 
		return redirect(url_for('admin.adminmanageairports')) 
	q="select * from airports INNER JOIN place using(place_id)"  	
	res=select(q) 
	data['airports']=res  
	q="select * from place" 
	res=select(q)
	data['place_id']=res
	return render_template('adminmanageairports.html',data=data) 

	

@admin.route('/adminmanagetypeofseat',methods=['get','post']) 
def adminmanagetypeofseat():
	data={}
	if 'action' in request.args:
		action=request.args['action'] 
		typeid=request.args['id'] 
	else:
		action=None
	if action=="delete":
		q="delete from type where type_id='%s'" %(typeid)  

		delete(q)
		return redirect(url_for('admin.adminmanagetypeofseat')) 

	if action=="update":
		q="select * from type where type_id='%s'" %(typeid) 
		res=select(q)
		data['updatetypeofseat']=res 
	if 'update' in request.form:
		type=request.form['type']	
		q="update type set type='%s' where type_id='%s'" %(type,typeid) 
		update(q)
		return redirect(url_for('admin.adminmanagetypeofseat')) 
	if 'add' in request.form:
		type=request.form['type'] 
		q="insert into type values(null,'%s')" %(type)     
		insert(q) 
		return redirect(url_for('admin.adminmanagetypeofseat')) 
	q="select * from type" 	
	res=select(q) 
	data['type']=res 
	return render_template('adminmanagetypeofseat.html',data=data) 

@admin.route('/adminmanageflights',methods=['get','post'])  
def adminmanageflights():
	data={}
	if 'action' in request.args:
		action=request.args['action'] 
		flightid=request.args['id'] 
	else:
		action=None
	if action=="delete":
		q="delete from flights where flight_id='%s'" %(flightid)  
		delete(q)
		return redirect(url_for('admin.adminmanageflights'))  
	if action=="update":
		q="select * from flights where flight_id='%s'" %(flightid) 
		res=select(q)
		data['updateflights']=res 
	if 'update' in request.form:
		flight=request.form['flight']	
		company=request.form['company']
		noofseats=request.form['noofseats']  
		q="update flights set flight='%s',company='%s', noofseats='%s' where flight_id='%s'" %(flight,company,noofseats,flightid)  
		update(q)
		return redirect(url_for('admin.adminmanageflights')) 
	if 'add' in request.form:
		flight=request.form['flight']
		company=request.form['company']
		noofseats=request.form['noofseats'] 
		q="insert into flights values(null,'%s','%s','%s')" %(flight,company,noofseats)     
		insert(q) 
		return redirect(url_for('admin.adminmanageflights')) 
	q="select * from flights" 	
	res=select(q) 
	data['flights']=res 
	return render_template('adminmanageflights.html',data=data)  	

@admin.route('/adminmanageseats',methods=['get','post'])  	
def adminmanageseats():
	data={}
	if 'action' in request.args:
		action=request.args['action'] 
		seatid=request.args['id'] 
	else:
		action=None
	if action=="delete":
		q="delete from seats where seat_id='%s'" %(seatid)  
		delete(q)
		return redirect(url_for('admin.adminmanageseats'))  
	if action=="update":
		q="select * from seats where seat_id='%s'" %(seatid)  
		res=select(q)
		data['updateseats']=res 
		q1="SELECT flight_id,flight,company,noofseats,(flight_id='%s') AS sel FROM flights ORDER BY sel DESC,flight_id ASC" %(res[0]['flight_id'])  
		res1=select(q1) 
		data['updateflights']=res1 
		q2="SELECT type_id,type,(type_id='%s') AS sel FROM type ORDER BY sel DESC,type_id ASC" %(res[0]['type_id'])  
		res2=select(q2) 
		data['updatetype']=res2
	if 'update' in request.form:
		typeid=request.form['type_id']	
		flightid=request.form['flight_id'] 
		seatno=request.form['seatno']  
		q="update seats set type_id='%s',flight_id='%s',seatno='%s' where seat_id='%s'" %(typeid,flightid,seatno,seatid)  
		update(q)
		return redirect(url_for('admin.adminmanageseats')) 
	if 'add' in request.form:
		typeid=request.form['type_id']
		flightid=request.form['flight_id']
		seatno=request.form['seatno'] 
		q="insert into seats values(null,'%s','%s','%s')" %(typeid,flightid,seatno)     
		insert(q) 
		return redirect(url_for('admin.adminmanageseats')) 
	q="select * from seats INNER JOIN flights using(flight_id) inner join type using(type_id)" 	 
	res=select(q) 
	data['seats']=res 	
	q="select * from flights"   
	res=select(q)
	data['flight_id']=res  
	q="select * from type"
	res=select(q)
	data['type_id']=res 
	return render_template('adminmanageseats.html',data=data)  	

@admin.route('/adminmanagescheduleflight',methods=['get','post'])  	
def adminmanagescheduleflight():
	data={}
	if 'action' in request.args:
		action=request.args['action'] 
		scheduleid=request.args['id'] 
	else:
		action=None
	if action=="delete":
		q="delete from flight_schedule where schedule_id='%s'" %(scheduleid)  
		delete(q)
		return redirect(url_for('admin.adminmanagescheduleflight'))  
	
	if 'add' in request.form:
		flightid=request.form['flight_id']
		fromairportid=request.form['from_airport_id'] 
		toairportid=request.form['to_airport_id'] 
		startdatetime=request.form['start_date_time'] 
		enddatetime=request.form['end_date_time']
		amount=request.form['amount']
		if  fromairportid==toairportid:
			flash("From Airport and To Airport Are Same")
		else:
			
			q="insert into flight_schedule values(null,'%s','%s','%s','%s','%s','%s')" %(flightid,fromairportid,toairportid,startdatetime,enddatetime,amount) 
			insert(q) 
			return redirect(url_for('admin.adminmanagescheduleflight')) 
	q="SELECT *,a1.`name` AS fname,a2.`name` AS tname FROM `flight_schedule` f,`airports` a1,`airports` a2,`flights` ff WHERE f.`flight_id`= ff.flight_id AND f.`from_airport_id`=a1.`airport_id` AND f.`to_airport_id`=a2.`airport_id`" 	 
	res=select(q) 
	data['flight_schedule']=res 	
	q="select * from flights"
	res=select(q)
	data['flight_id']=res 
	q="select * from airports" 
	res=select(q)
	data['to_airport_id']=res
	q="select * from airports" 
	res=select(q)

	data['from_airport_id']=res 


	
	return render_template('adminmanagescheduleflight.html',data=data)  	

@admin.route('/adminviewusers',methods=['get','post']) 
def adminviewusers(): 
	data={}
	if 'action' in request.args:
		action=request.args['action'] 
		userid=request.args['id'] 
	else:
		action=None	

	if action=="approve": 
		q="update login set usertype='users' where login_id='%s'" %(userid)  
		print(q)
		update(q)
		return redirect(url_for('admin.adminviewusers'))
		
	if action=="reject": 
		q="delete from login where login_id='%s'" %(userid)  
		delete(q)
		return redirect(url_for('admin.adminviewusers')) 
		
    	

	q="SELECT * FROM `users` INNER JOIN `login` USING(`login_id`) WHERE `usertype`='pending'"
	   
	res=select(q)
	data['users']=res
	print(res) 	

	return render_template('adminviewusers.html',data=data)  

@admin.route('/adminverifyusers',methods=['get','post']) 
def adminverifyusers(): 
	data={}
	q="SELECT * FROM `users` INNER JOIN `login` USING(`login_id`) WHERE `usertype`='users'" 
	res=select(q)
	data['users']=res 		

	return render_template('adminverifyusers.html',data=data)  	 
@admin.route('/adminviewfeedback',methods=['get','post']) 
def adminviewfeedback(): 
	data={}
	q="select * from feedback INNER JOIN users using(user_id)" 
	res=select(q)
	print(res)
	data['feedback']=res 	
	
	return render_template('adminviewfeedback.html',data=data) 

@admin.route('/adminmanagehotels',methods=['get','post'])  	
def adminmanagehotels():
	data={}
	if 'action' in request.args:
		action=request.args['action'] 
		hotelid=request.args['id'] 
	else:
		action=None
	if action=="delete":
		q="delete from hotels where hotel_id='%s'" %(hotelid)  
		delete(q)
		return redirect(url_for('admin.adminmanagehotels'))  
	
	if 'add' in request.form:
		placeid=request.form['place_id']
		hotel=request.form['hotel'] 
		pincode=request.form['pincode'] 
		q="insert into hotels values(null,'%s','%s','%s')" %(placeid,hotel,pincode)  
		insert(q) 
		return redirect(url_for('admin.adminmanagehotels')) 
	q="select * from hotels INNER JOIN place using(place_id)" 
	res=select(q) 
	data['hotels']=res 	
	q="select * from place"  
	res=select(q) 
	data['place']=res
	return render_template('adminmanagehotels.html',data=data)   

@admin.route('/adminmanagerooms',methods=['get','post'])  	
def adminmanagerooms():
	data={}
	if 'action' in request.args: 
		action=request.args['action'] 
		roomid=request.args['id'] 
	else:
		action=None
	if action=="delete":
		q="delete from rooms where room_id='%s'" %(roomid)  
		delete(q)
		return redirect(url_for('admin.adminmanagerooms'))  
	
	if 'add' in request.form:
		hotelid=request.form['hotel_id']
		roomnumber=request.form['roomnumber'] 
		rate=request.form['rate'] 
		
	 
		q="insert into rooms values(null,'%s','%s','%s')" %(hotelid,roomnumber,rate)  
		insert(q) 
		return redirect(url_for('admin.adminmanagerooms')) 
	
	q="select * from rooms INNER JOIN hotels using(hotel_id)" 	 

	res=select(q)
	data['rooms']=res  
	q="select * from hotels"   
	res=select(q)
	data['hotel_id']=res   
	return render_template('adminmanagerooms.html',data=data) 
	
		
@admin.route('/adminstaffallocate',methods=['get','post']) 
def adminstaffallocate():
	data={}  
	if 'action' in request.args:
		action=request.args['action'] 
		allocateid=request.args['id'] 
	else:
		action=None
	if action=="delete": 
		q="delete from staffallocate where allocate_id='%s'" %(allocateid) 
		delete(q) 
		return redirect(url_for('admin.adminstaffallocate'))	

	if 'submit' in request.form: 
		staffid=request.form['staff_id'] 
		airportid=request.form['airport_id'] 
		q="insert into staffallocate values(null,'%s','%s','accept')" %(staffid,airportid)  
		print(q)
		insert(q) 
		return redirect(url_for('admin.adminstaffallocate')) 

	

	q="select *,CONCAT(`firstname`,' ',`lastname`)as names from staffallocate INNER JOIN staff using(staff_id) INNER JOIN airports using(airport_id)"   
	res=select(q) 
	print(res)
	data['allocate']=res   
	q="select *,CONCAT(`firstname`,' ',`lastname`)as names from staff" 
	res=select(q) 
	data['staff_id']=res 
	q="select * from airports" 
	res=select(q)
	data['airport_id']=res  
	return render_template('adminstaffallocate.html',data=data)   


@admin.route('/predict_flight',methods=['get','post'])
def predict_flight():
    data = pd.read_csv("airline_crash_data.csv")

    # One-hot encode the categorical features
    data = pd.get_dummies(data, columns=["Aircraft Maintenance", "Weather Conditions", "Pilot Experience", "Air Traffic Control", "Human Factors", "Flight Operations", "Security"])

    # Split the data into training and testing sets
    X = data.drop(columns=["Crash or Not"])
    y = data["Crash or Not"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a random forest classifier on the data
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    # Evaluate the model on the test set
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)

    # Save the model to a file
    with open("airline_crash_model.pkl", "wb") as f:
        pickle.dump(clf, f)

    # Load the trained model from the file
    with open("airline_crash_model.pkl", "rb") as f:
        clf = pickle.load(f)

    if 'submit' in request.form:
        # Prompt the user for input values for each feature
        aircraft_maintenance = request.form['Aircraft Maintenance']
        weather_conditions = request.form['Weather Conditions']
        pilot_experience = request.form['Pilot Experience']
        air_traffic_control = request.form['Air Traffic Control']
        human_factors = request.form['Human Factors']
        flight_operations = request.form['Flight Operations']
        security = request.form['Security']

        # Create a data frame with the user inputs
        user_data = pd.DataFrame({
            "Aircraft Maintenance_" + aircraft_maintenance: [1],
            "Weather Conditions_" + weather_conditions: [1],
            "Pilot Experience_" + pilot_experience: [1],
            "Air Traffic Control_" + air_traffic_control: [1],
            "Human Factors_" + human_factors: [1],
            "Flight Operations_" + flight_operations: [1],
            "Security_" + security: [1]
        })

        # Encode the user inputs using the same one-hot encoding as the training data
        for col in X.columns:
            if col not in user_data.columns:
                user_data[col] = 0
        user_data = user_data[X.columns]

        # Make a prediction using the trained model
        prediction = clf.predict(user_data)

        if prediction[0] == 0:
            return redirect(url_for('admin.view_positive'))
        else:
            return redirect(url_for('admin.view_negative'))

    return render_template('predict_flight.html')

@admin.route('/view_positive')
def view_positive():
    return render_template('view_positive.html')


@admin.route('/view_negative')
def view_negative():
    return render_template('view_negative.html')



@admin.route('/view_booking',methods=['get','post'])
def view_booking():
    data={}
    q = "SELECT `ticketsbooked`.*, `flight_schedule`.*,flights.*,passengers.*, `from_airport`.`name` AS `from_airport_name`, `to_airport`.`name` AS `to_airport_name` FROM ticketsbooked INNER JOIN flight_schedule USING(schedule_id)INNER JOIN `airports` AS `from_airport` ON `flight_schedule`.`from_airport_id` = `from_airport`.`airport_id` INNER JOIN `airports` AS `to_airport` ON `flight_schedule`.`to_airport_id` = `to_airport`.`airport_id` INNER JOIN passengers USING(booked_id) INNER JOIN flights USING(flight_id)"
    res = select(q)
    data['ticketsbooked'] = res 
    return render_template('admin_view_booking.html', data=data)



@admin.route('/view_passengers', methods=['GET', 'POST'])
def view_passengers():
    data={}
    bid = request.args['bid'] 
    data['bid'] = bid
    fid = request.args['fid']
    data['fid'] = fid
    q = "SELECT *, CONCAT(first_name, ' ', last_name) AS names FROM passengers WHERE booked_id='%s'" % (bid)
    res = select(q)
    data['passengers'] = res 		
    return render_template('adminviewpassengersdetails.html',data=data)




		

	



	

		



	

	 
	

	