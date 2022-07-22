# Edge-Computer
This repository helps in implementing a edge computing device on a Linux/Windows operated machine

------------------------------------------
APPLICATION OVERVIEW:
------------------------------------------
Edge Computer essentially will acquire data from the sensor nodes/sensors networks present at the Industrial Shop Floor and then process the raw data obtained from the sensors and ship it to cloud servers/clients for superior cloud computation, evaluation and visualization. The edge computer can also receive control commands from the clients on the cloud facet and relay them to the respective sensor node/sensor network. The edge computer is a Linux Operated machine and the programming language utilized for implementing the edge computer is Python. To ensure edge computing functions are applied, an application layer IoT protocol, referred to as the MQTT Protocol (Message Queue Telemetry Transport) Protocol is utilized. MQTT protocol is implemented by using an MQTT Broker that will help to subscribe to topics or publish messages to subscribed topics.  In the given project the task was to do the necessary sensor interfacings to receive sensor data, store the sensor data in a database, publish sensor data to the clients on the cloud side whenever required and subscribe to a topic so that the edge computer can receive control commands from the cloud side and relay the control commands received from the cloud side to necessary sensor nodes/sensor networks.


------------------------------------------------------------
FEATURES IN THE APPLICATION
------------------------------------------------------------
The application is a menu driven application. User gets to select an option out of the various options available from the main menu. Upon selecting the option, the required task is carried out by calling required functions. The user can select from the following options:
1.  Publish the sensor database to the cloud client(s): In this feature, the user of the edge computer can publish sensor data stored in the central sensor database to the required client on the cloud side. The sensor database stores the data of all the sensors. Hence when the data is being published to a particular topic to the client on the cloud side the data is filtered and then sent to the cloud in JSON format.
2.  Publish sensor data received according to a particular schedule as defined by the user: In this feature, a schedule is being set as defined by the user. This schedule will be followed by the edge computer to receive data from the sensors which are interfaced with the system and then publish it to the required clients on the cloud side. Whenever the data is being scheduled and sent to the clients on the cloud side, the data is automatically collected and stored in the sensor database as well so that it can be referred to in the future if the need arises. The data sent to the cloud will be in JSON Format.
3.  View the list of topics to which the user is subscribed to: In this feature, the user can view the list of topics to which the edge computer is currently subscribed to. This list gets dynamically updated as and when a topic is subscribed/unsubscribed.
4.  Subscribe to a new topic to send control commands to the respective sensors: In this feature, the user can view the list of topics which are available for subscriptions and choose and subscribe to the same. The main aim of subscribing to these topics will be to receive control commands from the cloud side and relay it to the required sensors. This list of topics available for subscription gets dynamically updated as and when a topic is subscribed/unsubscribed.
5.  View the queued messages received from the subscribed topics when the system was offline: In this feature, the user will be able to view the queued messages that were received from the subscribed topics when the system was offline. In other words the user won't miss any updates/messages from the subscribed topics even when it was offline. As soon as the system is back online the user will be able to to view all these messages that were queued.
6.  Unsubscribe from a particular topic: In this feature, the user can choose to unsubscribe from a topic. The user has to choose one topic out of the list of subscriptions to unsubscribe from. The list gets dynamically updated whenever a topic is subscribed/unsubscribed.
7.  Exit from the main program: In this feature, the user can exit from the main program. This terminates the program completely.


------------------------------------------------------------
PREREQUISITES FOR RUNNING THE SOURCE CODE FOR EDGE COMPUTER
------------------------------------------------------------
1. Install latest version of Python, Visual Studio Code and the python extension available in Visual Studio Code.

2. Need to install the paho MQTT Library using the following command - pip install paho-mqtt

3. Need to install the schedule library using the following command - pip install schedule

4. Need to install the pandas library using the following command - pip install pandas

5. Need to install the pyserial library using the following command - pip install pyserial

6. Need to install software to implement MQTTBroker(can be MQTTBox or MQTTfx or any equivalent)

7. Need to declare the topics under publish option in the software that will be used to test the MQTT 
Connectivity Protocols such as MQTTBox(used for this project).This is done so that the control commands can be sent
to the edge computer accordingly. The topics are as follows:
a) scd-2022-03/climatedata
b) scd-2022-04/illuminationdata
c) scd-2022-05/motiondata

8. For all the new topics that will be added under the publish and subscribe option of the MQTT Broker(eg. MQTTBox)
the Quality of Service(QoS) needs to set to 1. This is done to ensure persistent session which will ensure all the
queued messages that were received when the system was offline are displayed when the system is online again.

9. All the 4 databases are also required to be imported to the project where the Python scripts will be executed so
that no error arises.

10. UDP client is also required to be set up on the sensor side for proper interfacing of the edge computer and sensor-03.
Edge computer serves as the UDP Server and sensor-03 serves as the UDP Client.

11. If the edge computer is being tested remotely, need to install virutal serial port driver to implement 
sensor-04 and sensor-05 serial communication.Two pairs need to be defined:
COM1-COM2: For Sensor-04
COM3-COM4: For Sensor-05

----------------------------------------------------------------
PYTHON PROGRAMS AND MODULES TO IMPLEMENT EDGE COMPUTER FEATURES
----------------------------------------------------------------
1. scd-grp1-main.py - This program consists of the main program snippet of the menu driven program and all the related function definitions.

2. ecinterface.py - This module consists of the functions that will aide in sensor interfacing of the sensor to the edge computer.


------------------------------------------------------------
DATABASES IMPLEMENTED FOR THIS PROJECT
------------------------------------------------------------
1.  sensordatabase.csv- This database will store all the values received from the sensors. The fields of this database are:
  a. 	Action: Stores the name of the sensor from which the data has been received.
  b. 	Result: Stores whether the sensor is working properly or not and whether it is being able to send across the values.
  c. 	Data: Stores the main sensor data received.
  d. 	Timestamp: Stores the time of receiving the data.
  e. 	Date: Stores the date of receiving the data.
2.  ControlCommandsdb.csv- This database will store the control commands received from the cloud server(client) side. The fields of this database are:
  a. 	Topic: Stores the name of the topic from which the control command was received.
  b. 	Data: Stores the control command received.
  c. 	Timestamp: Stores the time of receiving the control command.
  d. 	Date: Stores the date of receiving the control command.
3.  OptionsforTopicSubs.csv- This database will store the list of topics to which the user can subscribe to. The fields of this database are:
  a. 	Topic: Stores the names of the topics to which the user is not subscribed to.
4.  DataTopics.csv- This database will store the list of topics to which the user is currently subscribed to. The fields of this database are:
  a. 	Topic: Stores the names of the topics to which the user is currently subscribed to.

