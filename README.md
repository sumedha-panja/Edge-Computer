# Edge-Computer
This helps in implementing a edge computing device on a Linux/Windows operated machine

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


