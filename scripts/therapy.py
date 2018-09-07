#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import time
import datetime

import os, sys
from sound_play.msg import SoundRequest
from sound_play.libsoundplay import SoundClient
import cv2
import cv_bridge
from sensor_msgs.msg import (
    Image,
)
import baxter_interface
from baxter_interface import CHECK_VERSION
import subprocess


class demo_baxter_interface:
	def __init__(self):

		#some flags to describe the current state of the interaction
		self.speechRecognitionFlag = False
		self.personHasSaidWeAreDone = False
		self.emergencyDetected = False
		self.askedMeAboutMyPainting = False
		self.saveAPhoto = False
		self.personHasSaidYes = False
		self.personHasSaidNo = False
		self.personHasSaidHappy = False
		self.personHasSaidAngry = False
		self.personHasSaidSad = False
		self.personHasSaidRelaxed = False
		self.okayToTakeAPhoto = False

		#subscribers and publishers
		self.sub = rospy.Subscriber('to_baxter', String, self.buttonClickedCallback)
		self.subSpeech = rospy.Subscriber('/recognizer/output', String, self.speechRecognitionCallback)
		image_topic = "/cameras/left_hand_camera/image" #image_topic = "/cameras/head_camera/image"
		self.subCam = rospy.Subscriber(image_topic, Image, self.image_callback)	
		self.bridge = cv_bridge.CvBridge()

		#timing
		self.r=rospy.Rate(10)
		self.r.sleep()

		#sounds
		self.soundhandle = SoundClient()

		#for the robot's display
		#Please change all paths to where the files are on your computer
		self.face_pub = rospy.Publisher('/robot/xdisplay', Image, latch=True, queue_size=1)
		img = cv2.imread("/home/turtlebot/robot_faces/baxter_neutral.png")		
		self.neutralFace = cv_bridge.CvBridge().cv2_to_imgmsg(img, encoding="bgr8")
		img = cv2.imread("/home/turtlebot/robot_faces/baxter_happy.png")		
		self.happyFace = cv_bridge.CvBridge().cv2_to_imgmsg(img, encoding="bgr8")
		img = cv2.imread("/home/turtlebot/ros_ws/src/baxter_examples/share/images/comm_dep_faces/comm_dep_baxter_1_angry2.png")
		self.angryFace = cv_bridge.CvBridge().cv2_to_imgmsg(img, encoding="bgr8")
		img = cv2.imread("/home/turtlebot/robot_faces/blink.png")		
		self.blinkFace = cv_bridge.CvBridge().cv2_to_imgmsg(img, encoding="bgr8")
		self.face_pub.publish(self.blinkFace) #the robot starts asleep (so a human can wake the robot)

		#define arm poses so the robot can greet
		self.rs = baxter_interface.RobotEnable(CHECK_VERSION) 
		self.rightArmNeutralPose = {'right_s0': 0.8053399136398423, 'right_s1': -0.1622184683188825, 'right_w0': -0.13077186216723152, 'right_w1': -0.22012624306155687, 'right_w2': 0.02032524543948173, 'right_e0': -0.017640779060682257, 'right_e1': 1.7437526606287441}
		self.leftArmNeutralPose = {'left_w0': -0.33555829734993425, 'left_w1': -0.1580000211521976, 'left_w2': 0.06634466907604414, 'left_e0': -0.051004861197190006, 'left_e1': 1.5957235145978017, 'left_s0': -0.9503010980950138, 'left_s1': -0.060975736318445196}
		self.leftArmGreetingPose = {'left_w0': -2.1736507764336315, 'left_w1': -0.26422819071326253, 'left_w2': 0.09664078963678106, 'left_e0': 0.21935925266761416, 'left_e1': -0.051004861197190006, 'left_s0': -0.2956747968649135, 'left_s1': -0.8782040010643993}
		self.right_limb = baxter_interface.Limb('right')
		self.left_limb = baxter_interface.Limb('left')

	#record the session with a photo (if the right time and it is permitted)
	def image_callback(self, msg):
		if(self.saveAPhoto == True and self.okayToTakeAPhoto == True): 
    			try:
				print 'trying to save a photo'
            			cv2_img = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            			cv2.imwrite('art_therapy_record.jpeg', cv2_img)
				self.saveAPhoto = False
        		except cv_bridge.CvBridgeError, e:
            			print(e)
		self.r.sleep()


	#speech recognition callback
	def speechRecognitionCallback(self, data):
		if(self.speechRecognitionFlag == True):
			if("done" in data.data or "stop" in data.data): 
				print "heard done!"
				self.personHasSaidWeAreDone = True
			elif(data.data=='help'): 
				print "heard help!"
				self.emergencyDetected = True
			elif(data.data=='what are you painting'):
				print "heard what are you painting!"
				self.askedMeAboutMyPainting = True
			elif(data.data=='yes'): 
				print "heard yes!"
				self.personHasSaidYes = True
			elif(data.data=='no'):
				print "heard no!"
				self.personHasSaidNo = True
			elif(data.data=='happy'): 
				print "heard happy!"
				self.personHasSaidHappy = True
			elif(data.data=='angry'):
				print "heard angry!"
				self.personHasSaidAngry = True
			elif(data.data=='sad'): 
				print "heard sad!"
				self.personHasSaidSad = True
			elif(data.data=='relaxed'):
				print "heard relaxed!"
				self.lastHeard = data.data
				self.personHasSaidRelaxed = True
			else:
				print "heard something else"
				print data.data

	def buttonClickedCallback(self, data):
		if(data.data=='06'):				#when we press on button 6 in the GUI, start the demo
			self.personHasSaidWeAreDone = False
			self.emergencyDetected = False
			self.askedMeAboutMyPainting = False

			if not self.rs.state().enabled:
            			print("Enabling robot...")
            			self.rs.enable()

			self.left_limb.move_to_joint_positions(self.leftArmNeutralPose)
    			self.right_limb.move_to_joint_positions(self.rightArmNeutralPose)

			self.face_pub.publish(self.happyFace)
			self.soundhandle.say('Hey!')
			time.sleep(2)

			self.soundhandle.say('Welcome!')
			self.left_limb.move_to_joint_positions(self.leftArmGreetingPose)
			time.sleep(2)
			self.face_pub.publish(self.blinkFace) 
			time.sleep(0.2)
			self.face_pub.publish(self.happyFace)

			self.soundhandle.say("My name is Baxter and I am learning how to interact with humans. Please don't be disappointed if I don't understand what you say.")
			self.left_limb.move_to_joint_positions(self.leftArmNeutralPose)
    			self.right_limb.move_to_joint_positions(self.rightArmNeutralPose)
			time.sleep(12)

			#turn off the robot's motors so it can hear better
			if self.rs.state().enabled: 
            			print("Disabling robot...")
            			self.rs.disable()

			self.face_pub.publish(self.blinkFace) #blink
			time.sleep(0.2)
			self.face_pub.publish(self.happyFace)
			self.soundhandle.say("Do you feel like doing some painting today, yes or no? It's fine to say 'no'.")
			time.sleep(6)
			self.face_pub.publish(self.blinkFace) #blink
			time.sleep(0.2)
			self.face_pub.publish(self.happyFace)
			print("Listening...")
        		self.speechRecognitionFlag = True
			while (not rospy.is_shutdown()):

				if (self.personHasSaidYes == True):
					self.speechRecognitionFlag = False
					self.personHasSaidYes = False
					time.sleep(0.5) 
					self.soundhandle.say("You said yes. Great, let's explore our feelings with art!")
					time.sleep(7)
					break
				elif (self.personHasSaidNo == True):
					self.speechRecognitionFlag = False 
					self.personHasSaidNo = False
					time.sleep(0.5)
					self.soundhandle.say("You said no. Okay, I will do something else. Have a nice day.")
					self.face_pub.publish(self.blinkFace) 
					time.sleep(7)
					return -1		
				time.sleep(0.5)

			self.personHasSaidYes = False
			self.personHasSaidNo = False
			self.soundhandle.say('Is it okay if I let your care provider know that you have painted with me today, and take a photo of your painting to show them?')
			time.sleep(10)
			self.face_pub.publish(self.blinkFace) #blink
			time.sleep(0.2)
			self.face_pub.publish(self.happyFace)
			print("Listening...")
        		self.speechRecognitionFlag = True
			while (not rospy.is_shutdown()):

				if (self.personHasSaidYes == True): 
					self.speechRecognitionFlag = False 
					self.personHasSaidYes = False
					self.okayToTakeAPhoto = True
					time.sleep(0.5)
					self.soundhandle.say("You said yes. Okay I will keep a record")
					time.sleep(6)
					self.face_pub.publish(self.blinkFace) #blink
					time.sleep(0.2)
					self.face_pub.publish(self.happyFace)
					break
				elif (self.personHasSaidNo == True):
					self.speechRecognitionFlag = False 
					self.personHasSaidNo = False
					time.sleep(0.5)
					self.soundhandle.say("You said no. Okay, this is off the record.")
					time.sleep(6)
					self.face_pub.publish(self.blinkFace) #blink
					time.sleep(0.2)
					self.face_pub.publish(self.happyFace)
					break	
				time.sleep(0.5)

			self.personHasSaidYes = False
			self.personHasSaidNo = False


			self.soundhandle.say("By the way I hope you know that you can stop my arm at any time, or push the emergency button to turn me off. I'm completely safe")
			time.sleep(13)
			self.soundhandle.say("Let's get started. Please paint whatever you like, and I will do the same.")
			time.sleep(7)

			#loop (listening to what person has said): 
			#if person says they are done or the robot hears help, break
			#also check if time to speak, then ask person about something or comment about its own artwork
			
        		self.speechRecognitionFlag = True
			self.currentTime = datetime.datetime.now()
			lastTimeSpoke=self.currentTime 
			while (not rospy.is_shutdown()):

				self.currentTime = datetime.datetime.now()
				timeDifference = self.currentTime - lastTimeSpoke

				if (self.personHasSaidWeAreDone == True): 
					self.soundhandle.say("You're done? Okay, then I'm done too.")
					time.sleep(4)
					self.soundhandle.say("Thank you for painting with me, and showing me your wonderful artwork, goodbye!")
					#take photo
					self.saveAPhoto = True
					time.sleep(4)
					break
				elif (self.emergencyDetected == True):
					self.face_pub.publish(self.angryFace) 
					self.soundhandle.say("Emergency detected. Contacting care givers. Please wait")
					time.sleep(10)
					break		
				elif (self.askedMeAboutMyPainting == True): 
        				self.speechRecognitionFlag = False
					self.soundhandle.say("Thank you for asking about my painting. I have decided to paint something happy with yellow.")
					time.sleep(14)
					self.face_pub.publish(self.blinkFace) #blink
					time.sleep(0.2)
					self.face_pub.publish(self.happyFace)
					self.askedMeAboutMyPainting = False
	        			self.speechRecognitionFlag = True				
			 
				elif (timeDifference.seconds > 17):
        				self.speechRecognitionFlag = False
					self.soundhandle.say('What feeling are you showing in your painting?')
					time.sleep(5)
					self.face_pub.publish(self.blinkFace) #blink
					time.sleep(0.2)
					self.face_pub.publish(self.happyFace)
					print("Listening...")
        				self.speechRecognitionFlag = True
 
					while (not rospy.is_shutdown()):
						if (self.personHasSaidHappy== True): 
							self.speechRecognitionFlag = False 
							self.personHasSaidHappy = False
							time.sleep(0.5)
							self.soundhandle.say("You said happy. Why do you feel happy?")
							time.sleep(6)
							self.face_pub.publish(self.blinkFace) #blink
							time.sleep(0.2)
							self.face_pub.publish(self.happyFace)
							self.speechRecognitionFlag = True
							break
						elif (self.personHasSaidAngry == True):
							self.speechRecognitionFlag = False 
							self.personHasSaidAngry = False
							time.sleep(0.5)
							self.soundhandle.say("You said angry. Why do you feel angry?")
							self.face_pub.publish(self.blinkFace) #blink
							time.sleep(0.2)
							self.face_pub.publish(self.happyFace)
							time.sleep(6)
							self.speechRecognitionFlag = True
							break	
						#responses to other emotions can be added here
						time.sleep(0.5)

					self.currentTime = datetime.datetime.now()
					lastTimeSpoke=self.currentTime
	
				time.sleep(0.5)

			print 'Ending interaction'
			self.face_pub.publish(self.blinkFace)
        		self.speechRecognitionFlag = False
			time.sleep(7)

		time.sleep(0.01)

def sleep(t):
	try:
        	rospy.sleep(t)
	except KeyboardInterrupt:
		sys.exit()
	except:
		pass

if __name__== '__main__':

    	print '------------------------------------------------------'
    	print '-   Baxter simplified art therapy interaction demo   -'
    	print '-               JULY 2018, HH, Martin                -'
    	print '------------------------------------------------------'

	try:
		rospy.init_node('artTherapyDemo', anonymous=True)
		my_baxter_interface = demo_baxter_interface()
		while not rospy.is_shutdown():
			my_baxter_interface.r.sleep()
	except rospy.ROSInterruptException:
		pass
	finally:
		pass

