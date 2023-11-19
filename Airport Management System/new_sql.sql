/*
SQLyog Community v13.1.6 (64 bit)
MySQL - 10.4.27-MariaDB : Database - airline
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`airline` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;

USE `airline`;

/*Table structure for table `airports` */

DROP TABLE IF EXISTS `airports`;

CREATE TABLE `airports` (
  `airport_id` int(11) NOT NULL AUTO_INCREMENT,
  `place_id` int(11) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `district` varchar(100) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`airport_id`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `airports` */

insert  into `airports`(`airport_id`,`place_id`,`name`,`district`,`state`) values 
(3,5,'Trivandrum International Airport','Thiruvanthpuram','kerala'),
(9,10,'Calicut International Airport','Kozhikode','Kerala '),
(7,8,'Cochin International Airport','Ernakulam ','Kerala'),
(8,9,'Kannur International Airport','Kannur ','kerala');

/*Table structure for table `assignseat` */

DROP TABLE IF EXISTS `assignseat`;

CREATE TABLE `assignseat` (
  `assign_id` int(11) NOT NULL AUTO_INCREMENT,
  `passengers_id` int(11) DEFAULT NULL,
  `seat_id` int(11) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`assign_id`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `assignseat` */

insert  into `assignseat`(`assign_id`,`passengers_id`,`seat_id`,`status`) values 
(7,2,10,'accept'),
(3,3,9,'accept'),
(4,4,11,'accept'),
(5,1,9,'pending'),
(6,1,11,'pending'),
(8,3,13,'pending');

/*Table structure for table `bookroom` */

DROP TABLE IF EXISTS `bookroom`;

CREATE TABLE `bookroom` (
  `broom_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `room_id` int(11) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  `fromdate` varchar(100) DEFAULT NULL,
  `todate` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`broom_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `bookroom` */

insert  into `bookroom`(`broom_id`,`user_id`,`room_id`,`status`,`fromdate`,`todate`) values 
(1,1,2,'pending','2021-01-13','2021-01-16'),
(2,1,4,'pending','2021-02-02','2021-02-03');

/*Table structure for table `countries` */

DROP TABLE IF EXISTS `countries`;

CREATE TABLE `countries` (
  `country_id` int(11) NOT NULL AUTO_INCREMENT,
  `country` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`country_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `countries` */

insert  into `countries`(`country_id`,`country`) values 
(1,'Qatar'),
(2,'India'),
(3,'china');

/*Table structure for table `feedback` */

DROP TABLE IF EXISTS `feedback`;

CREATE TABLE `feedback` (
  `feedback_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `feedback` varchar(100) DEFAULT NULL,
  `date` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`feedback_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `feedback` */

insert  into `feedback`(`feedback_id`,`user_id`,`feedback`,`date`) values 
(1,1,'good','2021-01-31 00:18:11'),
(2,1,'good customer service','2021-02-11 15:00:36');

/*Table structure for table `flight_schedule` */

DROP TABLE IF EXISTS `flight_schedule`;

CREATE TABLE `flight_schedule` (
  `schedule_id` int(11) NOT NULL AUTO_INCREMENT,
  `flight_id` int(11) DEFAULT NULL,
  `from_airport_id` int(11) DEFAULT NULL,
  `to_airport_id` int(11) DEFAULT NULL,
  `start_date_time` varchar(100) DEFAULT NULL,
  `end_date_time` varchar(100) DEFAULT NULL,
  `t_amount` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`schedule_id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `flight_schedule` */

insert  into `flight_schedule`(`schedule_id`,`flight_id`,`from_airport_id`,`to_airport_id`,`start_date_time`,`end_date_time`,`t_amount`) values 
(3,3,3,9,'2021-10-02T00:30','2021-10-02T17:00','9000'),
(5,5,9,3,'2023-05-11T10:52','2023-05-12T10:53','5000');

/*Table structure for table `flights` */

DROP TABLE IF EXISTS `flights`;

CREATE TABLE `flights` (
  `flight_id` int(11) NOT NULL AUTO_INCREMENT,
  `flight` varchar(100) DEFAULT NULL,
  `company` varchar(100) DEFAULT NULL,
  `noofseats` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`flight_id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `flights` */

insert  into `flights`(`flight_id`,`flight`,`company`,`noofseats`) values 
(4,'Airasia','Malaysian','150'),
(3,'Eva Air','Taipei','200'),
(5,'Indigo Airlines','Interglobe Enterprises','100');

/*Table structure for table `flighttiming` */

DROP TABLE IF EXISTS `flighttiming`;

CREATE TABLE `flighttiming` (
  `flighttime_id` int(11) NOT NULL AUTO_INCREMENT,
  `schedule_id` int(11) DEFAULT NULL,
  `airport_id` int(11) DEFAULT NULL,
  `time` varchar(100) DEFAULT NULL,
  `type` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`flighttime_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `flighttiming` */

insert  into `flighttiming`(`flighttime_id`,`schedule_id`,`airport_id`,`time`,`type`) values 
(1,3,3,'16:15:38','departure'),
(2,3,3,'16:16:13','arrival');

/*Table structure for table `hotels` */

DROP TABLE IF EXISTS `hotels`;

CREATE TABLE `hotels` (
  `hotel_id` int(11) NOT NULL AUTO_INCREMENT,
  `place_id` int(11) DEFAULT NULL,
  `hotel` varchar(100) DEFAULT NULL,
  `pincode` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`hotel_id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `hotels` */

insert  into `hotels`(`hotel_id`,`place_id`,`hotel`,`pincode`) values 
(3,10,'ARYAS HOTEL','673001'),
(4,8,'MALABAR HOTEL ','682011'),
(5,9,'ARYABHAVAN ','670702'),
(6,11,'Vrinda ','695542');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `usertype` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `login` */

insert  into `login`(`login_id`,`username`,`password`,`usertype`) values 
(1,'admin','admin','admin'),
(2,'manju','manju','staff'),
(3,'radhu','radhu','users'),
(4,'radhu','radhu','pending'),
(5,'athira','athirakm45','staff'),
(6,'karthika','karthika','staff'),
(7,'vacoviwyc','1234','users');

/*Table structure for table `luggage_info` */

DROP TABLE IF EXISTS `luggage_info`;

CREATE TABLE `luggage_info` (
  `luggage_id` int(11) NOT NULL AUTO_INCREMENT,
  `booked_id` int(11) DEFAULT NULL,
  `total_weight` varchar(100) DEFAULT NULL,
  `details` varchar(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`luggage_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `luggage_info` */

insert  into `luggage_info`(`luggage_id`,`booked_id`,`total_weight`,`details`,`status`) values 
(1,2,'32 kg','bags','approve');

/*Table structure for table `message` */

DROP TABLE IF EXISTS `message`;

CREATE TABLE `message` (
  `message_id` int(11) NOT NULL AUTO_INCREMENT,
  `sender_id` int(11) DEFAULT NULL,
  `receiver_id` int(11) DEFAULT NULL,
  `message` varchar(100) DEFAULT NULL,
  `reply` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`message_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `message` */

insert  into `message`(`message_id`,`sender_id`,`receiver_id`,`message`,`reply`) values 
(1,3,2,'hiii\r\n','hi'),
(2,3,2,'zsxcszCszczs czxd cxc ','fsdfsdfvdsfv');

/*Table structure for table `passengers` */

DROP TABLE IF EXISTS `passengers`;

CREATE TABLE `passengers` (
  `passengers_id` int(11) NOT NULL AUTO_INCREMENT,
  `booked_id` int(11) DEFAULT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `dob` varchar(100) DEFAULT NULL,
  `gender` varchar(100) DEFAULT NULL,
  `house_name` varchar(100) DEFAULT NULL,
  `place` varchar(100) DEFAULT NULL,
  `country` varchar(100) DEFAULT NULL,
  `passport_no` varchar(100) DEFAULT NULL,
  `validity_date` varchar(100) DEFAULT NULL,
  `image1` varchar(250) DEFAULT NULL,
  `image2` varchar(250) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`passengers_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `passengers` */

insert  into `passengers`(`passengers_id`,`booked_id`,`first_name`,`last_name`,`phone`,`email`,`dob`,`gender`,`house_name`,`place`,`country`,`passport_no`,`validity_date`,`image1`,`image2`,`status`) values 
(1,1,'Radhu','K','9444467784','radhu6777@gmail.com','2014-12-05','Female','kfhfhh','Ernakulam','India','5788889786 ','2021-02-02','static/uploadimages/d1ff3db8-afbc-4e9a-9ace-7b615894f2f9de module 2.JPG','static/uploadimages/ebfc1cdc-d316-4862-9def-f88dbbbb7875r1.JPG','pending'),
(2,2,'Radhu','K','9444467784','radhu6777@gmail.com','1984-02-02','Female','Madathil house','Trivandrum','India','A2096457','2022-01-31','static/uploadimages/8335b832-69bf-4a14-82d2-a6db1dee4b73re.JPG','static/uploadimages/afaf5d11-c09b-481d-b6be-31b5082bbc1fr2.JPG','approve'),
(3,4,'Malavika','S','8452311905','malavikass2375@gmail.com','1980-04-09','Female','Madathil house','Trivandrum','India','A5095672','2021-12-31','static/uploadimages/7f3d5302-134c-4928-9f37-7b3dab94ae82dedekind,orde.JPG','static/uploadimages/e69a3d44-7de8-4467-96c3-71f1506e0c1fdedekinds prop.JPG','approve'),
(4,3,'Anamika','K','6483400268','anamika6348@gmail.com','1997-09-09','Female','Thekedath House','Trivandrum','India','B2378214','2022-02-28','static/uploadimages/8cc3f613-9562-4e21-899f-bb55884d72ffded1.JPG','static/uploadimages/c1a72832-1215-462f-8c7d-31e1b2b63112r2.JPG','approve');

/*Table structure for table `payment` */

DROP TABLE IF EXISTS `payment`;

CREATE TABLE `payment` (
  `payment_id` int(11) NOT NULL AUTO_INCREMENT,
  `booked_id` int(11) DEFAULT NULL,
  `amount` varchar(100) DEFAULT NULL,
  `date` varchar(50) DEFAULT NULL,
  `type` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`payment_id`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `payment` */

insert  into `payment`(`payment_id`,`booked_id`,`amount`,`date`,`type`) values 
(1,2,'27000','2021-02-11','ticket'),
(2,3,'27000','2023-05-02','ticket'),
(3,4,'45000','2023-05-02','ticket'),
(4,2,'27000','2023-05-03','ticket'),
(5,5,'10000','2023-05-11','ticket'),
(6,5,'10000','2023-05-11','ticket'),
(7,5,'10000','2023-05-11','ticket'),
(8,5,'10000','2023-05-11','ticket');

/*Table structure for table `place` */

DROP TABLE IF EXISTS `place`;

CREATE TABLE `place` (
  `place_id` int(11) NOT NULL AUTO_INCREMENT,
  `country_id` int(11) DEFAULT NULL,
  `state_place` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`place_id`)
) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `place` */

insert  into `place`(`place_id`,`country_id`,`state_place`) values 
(9,2,'Mattanur'),
(8,2,'Nedumbaserry '),
(11,2,'Chacka'),
(10,2,'Karipur'),
(13,2,'kerala-kollam'),
(14,2,'kerala-thrissur');

/*Table structure for table `rooms` */

DROP TABLE IF EXISTS `rooms`;

CREATE TABLE `rooms` (
  `room_id` int(11) NOT NULL AUTO_INCREMENT,
  `hotel_id` int(11) DEFAULT NULL,
  `roomnumber` varchar(100) DEFAULT NULL,
  `rate` int(11) DEFAULT NULL,
  PRIMARY KEY (`room_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `rooms` */

insert  into `rooms`(`room_id`,`hotel_id`,`roomnumber`,`rate`) values 
(1,1,'19',4000),
(2,2,'34',2500),
(3,6,'5',10000),
(4,3,'12',2000);

/*Table structure for table `seats` */

DROP TABLE IF EXISTS `seats`;

CREATE TABLE `seats` (
  `seat_id` int(11) NOT NULL AUTO_INCREMENT,
  `type_id` int(11) DEFAULT NULL,
  `flight_id` int(11) DEFAULT NULL,
  `seatno` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`seat_id`)
) ENGINE=MyISAM AUTO_INCREMENT=14 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `seats` */

insert  into `seats`(`seat_id`,`type_id`,`flight_id`,`seatno`) values 
(1,2,4,'1'),
(2,3,4,'2'),
(3,1,4,'3'),
(10,3,3,'1'),
(8,3,4,'5'),
(9,1,3,'2'),
(7,1,4,'4'),
(11,2,3,'3'),
(12,1,5,'1'),
(13,3,5,'2');

/*Table structure for table `staff` */

DROP TABLE IF EXISTS `staff`;

CREATE TABLE `staff` (
  `staff_id` int(11) NOT NULL AUTO_INCREMENT,
  `login_id` int(11) DEFAULT NULL,
  `firstname` varchar(100) DEFAULT NULL,
  `lastname` varchar(100) DEFAULT NULL,
  `gender` varchar(100) DEFAULT NULL,
  `age` varchar(100) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `designation` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`staff_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `staff` */

insert  into `staff`(`staff_id`,`login_id`,`firstname`,`lastname`,`gender`,`age`,`phone`,`email`,`designation`) values 
(1,2,'sdzfsdgvsdffv','S','Male','38','9956678787','manju7774@gmail.com','worker'),
(2,5,'Manju dddddddddd','S','Male','38','9956678787','manju7774@gmail.com','worker'),
(3,6,'Manju dddddddddd','S','Male','38','9956678787','manju7774@gmail.com','worker');

/*Table structure for table `staffallocate` */

DROP TABLE IF EXISTS `staffallocate`;

CREATE TABLE `staffallocate` (
  `allocate_id` int(11) NOT NULL AUTO_INCREMENT,
  `staff_id` int(11) DEFAULT NULL,
  `airport_id` int(11) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`allocate_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `staffallocate` */

insert  into `staffallocate`(`allocate_id`,`staff_id`,`airport_id`,`status`) values 
(1,1,3,'accept'),
(2,1,9,'accept'),
(3,2,3,'accept'),
(4,3,8,'accept');

/*Table structure for table `ticketsbooked` */

DROP TABLE IF EXISTS `ticketsbooked`;

CREATE TABLE `ticketsbooked` (
  `booked_id` int(11) NOT NULL AUTO_INCREMENT,
  `schedule_id` int(11) DEFAULT NULL,
  `amount` varchar(100) DEFAULT NULL,
  `noofpassengers` varchar(100) DEFAULT NULL,
  `booked_status` varchar(100) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`booked_id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `ticketsbooked` */

insert  into `ticketsbooked`(`booked_id`,`schedule_id`,`amount`,`noofpassengers`,`booked_status`,`user_id`) values 
(1,1,'6000','3','pending',3),
(5,5,'10000','2','Paid',7),
(4,3,'45000','5','Approve',3);

/*Table structure for table `type` */

DROP TABLE IF EXISTS `type`;

CREATE TABLE `type` (
  `type_id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `type` */

insert  into `type`(`type_id`,`type`) values 
(1,'middle '),
(2,'aside '),
(3,'window ');

/*Table structure for table `users` */

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `login_id` int(11) DEFAULT NULL,
  `fname` varchar(100) DEFAULT NULL,
  `lname` varchar(100) DEFAULT NULL,
  `place` varchar(100) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `path` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `users` */

insert  into `users`(`user_id`,`login_id`,`fname`,`lname`,`place`,`phone`,`email`,`path`) values 
(1,3,'Radhu','K','Ernakulam','9444467784','syamraj310@gmail.com','static/uploadimages/62e56ea2-0ebd-486b-be84-ead3f1422566dedekinds prop.JPG'),
(3,7,'Noelle Huber','Zachary Sosa','Eum dolore mollitia ','9999999999','sepez@mailinator.com','static/uploadimages/d979e1d5-17d3-4102-b6da-691c6ff3f7fc2.png');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
