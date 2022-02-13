from email.policy import default
import os
import time

from ab2_mqtt import MQTTClient

ir_sensors = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
threshold = 500
ir1State = False
ir2State = False
ir3State = False

def ir(client, userdata, msg):
    global ir_sensors , threshold, fast, slow, ir1State, ir2State, ir3State
    msg = msg.payload.decode("utf-8")
    msg2 = msg.split(" ")
    for i in range(len(msg2)):
        msg2[i] = msg2[i].replace('[', '')
        msg2[i] = msg2[i].replace(',', '')
        msg2[i] = msg2[i].replace(']', '')
        ir_sensors[i] = float(msg2[i])

    ir1 = ir_sensors[3]
    ir2 = ir_sensors[4]
    ir3 = ir_sensors[5]

    ir1State = ir1 > threshold
    ir2State = ir2 > threshold
    ir3State = ir3 > threshold
    #print(str(ir1State) + "    " + str(ir2State) + "    " + str(ir3State)+ "       ",end = "\r")

#WHITE == TRUE

line_is_black = False #True if line is black and floor white

def running(client):
    global ir1State, ir2State, ir3State
    left = 60
    right = 60

    if(ir1State == line_is_black):
        right -= 20
        if(ir2State == line_is_black):
            right -= 20
            if(ir3State == line_is_black):
                right = 0

    if(ir3State == line_is_black):
        left -= 20
        if(ir2State == line_is_black):
            left -= 20
            if(ir1State == line_is_black):
                left = 0

    client.publish(client.TOPIC_OBSTACLE_LINE_FOLLOWING_RIGHT, str(left) + " " + str(right))
    #print(str(left) + "      " + str(right) + "       ",end = "\r")


client = MQTTClient("LineFollowingRight", 'localhost' , 1883, 0)
client.loop_start() 

client.message_callback_add(client.TOPIC_IRSENSORS, ir)


if __name__ == '__main__':
    while True:
        running(client)
        time.sleep(0.05)