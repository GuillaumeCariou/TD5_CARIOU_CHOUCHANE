import os
import time

from ab2_mqtt import MQTTClient

state_right = "False"
state_leflt = "False"

def left(client, userdata, msg):
    global state_leflt
    msg = msg.payload.decode("utf-8")
    state_leflt = msg

def right(client, userdata, msg):
    global state_right
    msg = msg.payload.decode("utf-8")
    state_right = msg

def common(client):
    global state_right, state_leflt

    if(state_leflt == "True" and state_right == "True"):    #STOP Both on
        stop_action(client)
    elif(state_leflt == "True" and state_right == "False"): #RIGHT left on turn right
        right_action(client)
    elif(state_leflt == "False" and state_right == "True"): #LEFT right on turn left
        left_action(client)
    else:                                                   #FORWARD none one forward
        forward_action(client)

def stop_action(client):
    client.publish(client.TOPIC_OBSTACLE_AVOIDANCE, "stop")
    print("stop")

def right_action(client):
    client.publish(client.TOPIC_OBSTACLE_AVOIDANCE, "turnright")
    print("turnright")

def left_action(client):
    client.publish(client.TOPIC_OBSTACLE_AVOIDANCE, "turnleft")
    print("turnleft")

def forward_action(client):
    client.publish(client.TOPIC_OBSTACLE_AVOIDANCE, "forward")
    print("forward")


client = MQTTClient("obstacleAvoidance", 'localhost' , 1883, 0)
client.loop_start() 

client.message_callback_add(client.TOPIC_OBSTACLE_LEFT, left)
client.message_callback_add(client.TOPIC_OBSTACLE_RIGHT, right)

if __name__ == '__main__':
    while True:
        time.sleep(0.05)
        common(client)