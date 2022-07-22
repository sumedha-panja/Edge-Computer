#This is the main program module for the edge computer

#Consists of all the function definitions required to implement the  edge computer features

import paho.mqtt.client as mqtt_client  #for implementing mqtt publish/subscribe features
import time                             #for implementing time.sleep() for pausing the program for some time
import schedule                         #for publishing messages as per a schedule
import threading                        #for creating a thread to run the scheduled jobs without blocking the main code
import pandas as pd                     #for filtering sensor data
from csv import *                       #to write/read from csv database(s)
from datetime import datetime           #record time of receiving sensor data
from datetime import date               #record date of receiving sensor data
import csv                              #to read/write from csv databases
from ecinterface import *               #import functions that help in sensor interfacing
import json                             #converting the string received from sensors to json object and also converting .csv data

broker = "broker.emqx.io"                       #defining the cloud client,port number and clientID
port = 1883
clientID = "client123456"

#connecting the program to the mqtt broker
#False implies a persistent session where messages from subscribed topics are queued when the system is offline
client =  mqtt_client.Client(clientID,False)  
client.connect(broker,port)                         #connecting to the broker remotely



df = pd.read_csv("sensordatabase.csv")              #creating pandas dataframe of the sensor database


#declaring the topics
Topic1 = "scd-2022-03/climatedata"
Topic2 = "scd-2022-04/illuminationdata"
Topic3 = "scd-2022-05/motiondata"

#selecting a particular topic to publish messages/subcribe to a topic
def selecting_options():
        print("Select options from below:")
        print("1. Climate data")
        print("2. Illumination Data")
        print("3. Motion Data")
        option = input("Enter your choice: ")      #user enters choice and the required topic name is returned to the main program snippet
        if(int(option)== 1):
            return Topic1
        elif(int(option)== 2):
            return Topic2  
        elif(int(option)== 3):
            return Topic3
        else:
            print("Wrong choice entered!")
            return selecting_options()                   

#function to decode messages from the sensors and add it to sensor database
def on_message(client, userdata, msg):
    request = msg.payload.decode()                  #Store the message received from the broker in string format
    print(f"Received {request} from {msg.topic} topic") #Display the message

    now = datetime.now()                            #record the time of receiving the message
    current_time = now.strftime("%H:%M:%S")
    today = date.today()                            #record the date of receiving the message

    #append the control commands received to the database which will keep a track of all the control commands received from the cloud
    list=[f'{msg.topic}',f'{request}',f'{current_time}',f'{today}']
    with open('ControlCommandsdb.csv', 'a') as f_object: 
        writer_object = writer(f_object)            #call the writer function to initiate writing into .csv file
        writer_object.writerow(list)                #adding the control commands received in a row format
        f_object.close()                            #closing the file object 
           
#function to publish messages for topic 1 as per schedule
def pubschedTopic1():
    print("Publishing data...")
    data = udpdatasensor03()      #stores the json string returned by the udpdatasensor03() function imported from ecinterface.py program
    client.publish(Topic1,data,1)    #publishing the data to Topic 1. Here qos is set 1 to implement persistant session    
    json_object = json.loads(data)   #convert string received into dictionary format
    print("Data sent!")
    temp_df = pd.DataFrame(json_object)      #creating a temporary dataframe of the json_object created
    now = datetime.now()                     #record the time of receiving the message
    current_time = now.strftime("%H:%M:%S")
    today = date.today()                            #record the date of receiving the message 
    timestamp = [f'{current_time}',f'{current_time}',f'{current_time}']
    daterec = [f'{today}',f'{today}',f'{today}']
    temp_df['Timestamp'] = timestamp                #adding the timestamp and date columns to the temporary dataframe
    temp_df['Date'] = daterec
    temp_df.to_csv('sensordatabase.csv', mode='a', index=False, header=False)   #append the data
    print("Data added to the central database successfully.")
    
#function to publish messages for topic 2 as per schedule and add data received to sensor database
def pubschedTopic2():
    print("Publishing data...")
    data=serialdatasensor04()       #stores the json string returned by the serialsensor04() function imported from ecinterface.py program
    client.publish(Topic2,data,1)   #publishing the data to Topic 2. Here qos is set 1 to implement persistant session
    json_object = json.loads(data)  #convert it into dictionary format
    print("Data sent!")
    temp_df = pd.DataFrame(json_object)             #creating a temporary dataframe of the json_object created             
    now = datetime.now()                            #record the time of receiving the message
    current_time = now.strftime("%H:%M:%S")
    today = date.today()                            #record the date of receiving the message 
    timestamp = [f'{current_time}',f'{current_time}',f'{current_time}']
    daterec = [f'{today}',f'{today}',f'{today}']
    temp_df['Timestamp'] = timestamp                #adding the timestamp and date columns to the temporary dataframe
    temp_df['Date'] = daterec
    temp_df.to_csv('sensordatabase.csv', mode='a', index=False, header=False)   #append the data
    print("Data added to the central database successfully.")

#function to publish messages for topic 3 as per schedule and add data received to sensor database
def pubschedTopic3():  
    print("Publishing data...")
    data=serialdatasensor05()       #stores the json string returned by the serialsensor05() function imported from ecinterface.py program
    client.publish(Topic3,data,1)   #publishing the data to Topic 3. Here qos is set 1 to implement persistant session
    json_object = json.loads(data)  #convert it into dictionary format
    print("Data sent!")
    temp_df = pd.DataFrame(json_object)    #creating a temporary dataframe of the json_object created
    now = datetime.now()                   #record the time of receiving the message
    current_time = now.strftime("%H:%M:%S")
    today = date.today()                            #record the date of receiving the message 
    timestamp = [f'{current_time}',f'{current_time}',f'{current_time}',f'{current_time}',f'{current_time}',f'{current_time}']
    daterec = [f'{today}',f'{today}',f'{today}',f'{today}',f'{today}',f'{today}']
    temp_df['Timestamp'] = timestamp                #adding the timestamp and date columns to the temporary dataframe
    temp_df['Date'] = daterec
    temp_df.to_csv('sensordatabase.csv', mode='a', index=False, header=False)       #append the data
    print("Data added to the central database successfully.")          

#function to choose the time period for scheduling
def schedule_function(Topic):
    #print the choices of scheduling jobs
    print("Choose the time interval for scheduling:")   
    print("1. After every particular interval of minutes") 
    print("2. After every particular interval of hours") 
    print("3. On weekdays(Monday-Friday) at a particluar time")
    opt=int(input("Enter your choice: "))
    if(opt==1 and Topic==Topic1):
        t1= input("After how many minutes you would like to publish messages: ")
        schedule.every(int(t1)).minutes.do(pubschedTopic1)

    elif(opt==2 and Topic==Topic1):
        t1= input("After how many hours you would like to publish messages: ")
        schedule.every(int(t1)).hours.do(pubschedTopic1)

    elif(opt==3 and Topic==Topic1):
        t1= input("What time would you like to schedule this message[Enter in HH:MM format]:")
        schedule.every().monday.at(t1).do(pubschedTopic1)    
        schedule.every().tuesday.at(t1).do(pubschedTopic1)
        schedule.every().wednesday.at(t1).do(pubschedTopic1)
        schedule.every().thursday.at(t1).do(pubschedTopic1)
        schedule.every().friday.at(t1).do(pubschedTopic1)

    elif(opt==1 and Topic==Topic2):
        t1= input("After how many minutes you would like to publish messages: ")
        schedule.every(int(t1)).minutes.do(pubschedTopic2)

    elif(opt==2 and Topic==Topic2):
        t1= input("After how many hours you would like to publish messages: ")
        schedule.every(int(t1)).hours.do(pubschedTopic2)

    elif(opt==3 and Topic==Topic2):
        t1= input("What time would you like to schedule this message[Enter in HH:MM format]:")
        schedule.every().monday.at(t1).do(pubschedTopic2)    
        schedule.every().tuesday.at(t1).do(pubschedTopic2)
        schedule.every().wednesday.at(t1).do(pubschedTopic2)
        schedule.every().thursday.at(t1).do(pubschedTopic2)
        schedule.every().friday.at(t1).do(pubschedTopic2)

    elif(opt==1 and Topic==Topic3):
        t1= input("After how many minutes you would like to publish messages: ")
        schedule.every(int(t1)).minutes.do(pubschedTopic3)

    elif(opt==2 and Topic==Topic3):
        t1= input("After how many hours you would like to publish messages: ")
        schedule.every(int(t1)).hours.do(pubschedTopic3)

    elif(opt==3 and Topic==Topic3):
        t1= input("What time would you like to schedule this message[Enter in HH:MM format]:")
        schedule.every().monday.at(t1).do(pubschedTopic3)    
        schedule.every().tuesday.at(t1).do(pubschedTopic3)
        schedule.every().wednesday.at(t1).do(pubschedTopic3)
        schedule.every().thursday.at(t1).do(pubschedTopic3)
        schedule.every().friday.at(t1).do(pubschedTopic3)

    else:
        print("Wrong choice!")
        return schedule_function()   

#to create a thread for running the scheduled jobs without blocking the main code. 
#Reference for the below function-https://schedule.readthedocs.io/en/stable/background-execution.html
def run_continuously(interval=1):
    """Continuously run, while executing pending jobs at each
    elapsed time interval.
    @return cease_continuous_run: threading. Event which can
    be set to cease continuous run. Please note that it is
    *intended behavior that run_continuously() does not run
    missed jobs*. For example, if you've registered a job that
    should run every minute and you set a continuous run
    interval of one hour then your job won't be run 60 times
    at each interval but only once.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run

#function to publish messages to client and display the sesnor data in json format
def publish_msg(Topic):
    if Topic == Topic1:
        sensordataframe= df[df['action']=='sensor-03']    #filter data and store only sensor-03 in the dataframe      
    elif Topic == Topic2:
        sensordataframe= df[df['action']=='sensor-04']    #filter data and store only sensor-04 in the dataframe     
    elif Topic == Topic3:
        sensordataframe= df[df['action']=='sensor-05']    #filter data and store only sensor-05 in the dataframe
    else:
        print("Something wrong! Try again")
        return        
    msg = sensordataframe.to_json(orient ='records')  #convert the .csv file data to json format in records orientation
    client.publish(Topic,msg,1)                       #Publish messages to required topics. qos is set to 1 to implement persistant session
    print("Message sent")                             #Confirmation that message has been published 
  
def subscribe_topic():
    try:
        filename = "OptionsforTopicSubs.csv"
        Topic_Data=pd.read_csv(filename)
        topics = Topic_Data['Topic'].to_list() #convert csv database to list format
        if(len(topics)==0):                    #to check if there are any topics available for subscription
            print("All topics have been already subscribed!")
            time.sleep(1)
            return
        print("Which topic do you wish to subscribe?")    
        for i in range(len(topics)):   #print topics to which the user is currently not subscribed to
            print(f"{i+1}. {topics[i]}")  
        val=int(input("Enter your choice:")) #user enters the choice
        topic=topics[val-1]     #the topic to be subscribed is stored
        client.subscribe(topic,1) #topic is subscribed, qos is set to 1 to implement persistant session
        client.on_message= on_message  #start receiving the messages
        client.loop_start()     #start the loop to receive messages from the broker
        topics.remove(topic)    #removed from the list of unsubscribed topics
        f = open(filename, "w+") #csv file is completely cleared
        csvr = csv.writer(f)
        csvr.writerow(['Topic'])   #Header row described
        f.close()                  #file object closed
        for i in range(len(topics)):               
            list = [topics[i]]
            with open('OptionsforTopicSubs.csv', 'a') as f_object:  #update the .csv file which stores list of unsubscribed topics
                writer_object = writer(f_object)     #creating a writer object to write data into the file
                writer_object.writerow(list)         #append data to the file
                f_object.close()                     #close the file object 
        list1 = [topic]
        with open('DataTopics.csv', 'a') as f_object: #update the .csv file which stores list of subscribed topics by using a file object
            writer_object = writer(f_object)   #creating a writer object to write data into the file
            writer_object.writerow(list1)     #append data to the file
            f_object.close()         #close the file object     
        print(f"Subscribed to {topic} successfully!")
        time.sleep(1)
    except: 
        print("Something wrong! Try again")   #if user enters a random number instead of the choices 
        time.sleep(1) 

def viewoffline_msg():
    dftopic = pd.read_csv("DataTopics.csv")
    topics = dftopic['Topic'].to_list()             #convert .csv file data to list format
    for i in range(len(topics)):
        #reconnect to the topics which have been already subscribed.Qos is set to 1 for persistent session
        client.subscribe(topics[i],1)  
    client.on_message = on_message     #print the queued messages
    client.loop_start()
    time.sleep(2)

def unsubscribe_topic():
    try:
        filename = "DataTopics.csv"
        Topic_Data=pd.read_csv(filename)
        topics = Topic_Data['Topic'].to_list()      #convert csv database to list format
        if(len(topics)==0):                         #to check if there are any subscribed topics available or not
            print("No subscribed topics available at the moment!")
            time.sleep(1)
            return
        print("From which topic do you wish to unsubscribe?")    
        for i in range(len(topics)):                #print topics to which the user is currently subscribed to
            print(f"{i+1}. {topics[i]}")  
        val=int(input("Enter your choice:"))        #user enters the choice
        deletetopic=topics[val-1]                   #the topics to be unsubscribed is stored
        client.unsubscribe(deletetopic)             #topic is unsubscribed
        topics.remove(deletetopic)                  #removed from the list
        f = open(filename, "w+")                    #csv file is cleared comppetely
        csvr = csv.writer(f)
        csvr.writerow(['Topic'])                    #Header row described
        f.close()
        list = [deletetopic]
        with open('OptionsforTopicSubs.csv', 'a') as f_object:    #update the .csv file which stores list of unsubscribed topics
            writer_object = writer(f_object)
            writer_object.writerow(list)
            f_object.close() 
        for i in range(len(topics)):                
            list1 = [topics[i]]
            with open('DataTopics.csv', 'a') as f_object:         #update the .csv file which stores list of subscribed topics
                writer_object = writer(f_object)
                writer_object.writerow(list1)
                f_object.close()    
        print(f"Unsubscribed from {deletetopic} successfully!")
        time.sleep(1)
    except:
        print("Something wrong! Try again")
        time.sleep(1)   

#View the list of topics which have been subscribed to currently             
def viewsubtopics():
    filename = "DataTopics.csv"
    Topic_Data=pd.read_csv(filename)
    topics = Topic_Data['Topic'].to_list()      #convert csv database to list format
    if(len(topics)==0):                         #to check if there are any subscribed topics available or not
        print("No topics subscribed at the moment!")
        time.sleep(1)
        return
    print("Current subscriptions:")    
    for i in range(len(topics)):                #print topics to which the user is currently subscribed to
        print(f"{i+1}. {topics[i]}")
    time.sleep(1)        
        
#the main program snippet-menu driven program that calls the defined functions accordingly
while True:    
    print("Select options from below:")
    print("1. Publish sensor database ") 
    print("2. Publish sensor data as per user-defined schedule") 
    print("3. View the list of subscribed topics") 
    print("4. Subscribe to a topic to send required control commands to sensors") 
    print("5. View messages received from the subscribed topics when system was offline") 
    print("6. Unsubscribe from a topic ")
    print("7. Exit")
    val = int(input("Enter your choice:\n"))
    if(val==1):
        Topic = selecting_options()
        publish_msg(Topic)
    elif(val==2):
        Topic = selecting_options()
        schedule_function(Topic)  
        stop_run_continuously = run_continuously()  
    elif(val==3):
        viewsubtopics()
    elif(val==4):
        subscribe_topic()
    elif(val==5):
        viewoffline_msg()
    elif(val==6):
        unsubscribe_topic()             
    elif(val==7):
        #error/exception handling
        try:
            client.disconnect()                 #to disconnect to the broker
            UDPServerSocket.close()             #closed the UDPServer connection
            stop_run_continuously.set()         #stop the running of the thread that executes the scheduled jobs
            print("Exited from the program successfully!")
        except:
            print("Exited from the program successfully!")
        break    
    else:
        print("Wrong choice entered!")  