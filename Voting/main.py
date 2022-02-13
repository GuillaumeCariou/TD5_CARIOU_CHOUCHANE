from ab2_mqtt import MQTTClient
import time

oa = "stop"
lfl = [30,60]
lfr= [60,30]

def obstacleAvoidance(client, userdata, msg):
    global oa
    oa = msg.payload.decode("utf-8")

def lineFollowingLeft(client, userdata, msg):
    global lfl
    msg = msg.payload.decode("utf-8")
    msg2 = msg.split(" ")
    lfl[0] = int(msg2[0])
    lfl[1] = int(msg2[1])

def lineFollowingRight(client, userdata, msg):
    global lfr
    msg = msg.payload.decode("utf-8")
    msg2 = msg.split(" ")
    lfr[0] = int(msg2[0])
    lfr[1] = int(msg2[1])

client = MQTTClient('Voting', '0.0.0.0' , 1883, 0)
client.loop_start()

client.message_callback_add(client.TOPIC_OBSTACLE_AVOIDANCE, obstacleAvoidance)
client.message_callback_add(client.TOPIC_OBSTACLE_LINE_FOLLOWING_LEFT, lineFollowingLeft)
client.message_callback_add(client.TOPIC_OBSTACLE_LINE_FOLLOWING_RIGHT, lineFollowingRight)

def mean(tab1,tab2):
    #print(str(tab1) + "         " + str(tab2)+"        " + str(int((tab1[0] + tab2[0])/2)) + "         " + str(int((tab1[1] + tab2[1])/2)) +"        ",end="\r")
    return [int((tab1[0] + tab2[0])/2),int((tab1[1] + tab2[1])/2)]

def oa_action():
    global client, oa

    if oa == "stop":
        client.publish(client.TOPIC_MOVE, "stop")
        client.publish(client.TOPIC_MOTORS, str(0.0) + " " + str(0.0))
        return True
    elif oa == "turnright":
        #Do something
        return True
    elif oa == "turnleft":
        #Do something
        return True
    else:
        #Just Forward
        return False

vitesse = 3
def main():
    global client, lfl, lfr, vitesse
    if oa_action():
        return
    
    l = int(int((lfl[0] + lfr[0])/2)/vitesse)
    r = int(int((lfl[1] + lfr[1])/2)/vitesse)
    direction = [l,r]
    #print(str(l) + "         " + str(r)+"        ",end="\r")
    #print(str(direction[0])  + "         " + str(direction[1]) + "        ",end="\r")
    if direction[0] == 0 and direction[1] == 0:
        client.publish(client.TOPIC_MOVE, "stop")
        client.publish(client.TOPIC_MOTORS, str(direction[0]) + " " + str(direction[1]))
        #print(str(lfl) + "         " + str(lfr)+"        " + str(direction[0]) + "         " + str(direction[0])+"        stop         " ,end="\r")
    else:
        client.publish(client.TOPIC_MOVE, "forward")
        client.publish(client.TOPIC_MOTORS, str(direction[0]) + " " + str(direction[1]))
        #print(str(lfl) + "         " + str(lfr)+"        " + str(direction[0]) + "         " + str(direction[0])+"        forward      ",end="\r")
    
    


if __name__ == '__main__':
    print("Voting Running")
    while True:
        time.sleep(0.05)
        main()