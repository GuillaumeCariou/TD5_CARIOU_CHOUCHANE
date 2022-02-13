import logging
import paho.mqtt.client as mqtt


class MQTTClient(mqtt.Client):

    # actuators topics
    TOPIC_MOVE = "alphabot2/actuators/move"
    TOPIC_SERVOS = "alphabot2/actuators/servos"
    TOPIC_MOTORS = "alphabot2/actuators/motors"
    TOPIC_SPEED = "alphabot2/actuators/speed"
    TOPIC_BUZZER = "alphabot2/actuators/buzzer"
    TOPIC_LEDS = "alphabot2/actuators/rgbleds"

    # sensors topics
    TOPIC_JOYSTICK = "alphabot2/sensors/joystick"
    TOPIC_OBSTACLE_LEFT = "alphabot2/sensors/obstacle/left"
    TOPIC_OBSTACLE_RIGHT = "alphabot2/sensors/obstacle/right"
    TOPIC_IRSENSORS = "alphabot2/sensors/irsensors"

    TOPIC_OBSTACLE_AVOIDANCE = "alphabot2/voting/obstacleAvoidance"
    TOPIC_OBSTACLE_LINE_FOLLOWING_LEFT = "alphabot2/voting/lineFollowingLeft"
    TOPIC_OBSTACLE_LINE_FOLLOWING_RIGHT = "alphabot2/voting/lineFollowingRight"


    def __init__(self, client_id, host, port=1883, keepalive=60, qos=0, **kwargs):
        super(MQTTClient, self).__init__(
            client_id=client_id, clean_session=True, **kwargs)
        self.qos = qos
        super().connect(host, port)
        logging.info("Connected to MQTT", flush=True)

    def on_connect(self, client, userdata, flags, rc):
        switcher = {
            1: 'incorrect protocol version',
            2: 'invalid client identifier',
            3: 'server unavailable',
            4: 'bad username or password',
            5: 'not authorised'
        }
        if (rc == 0):
            logging.info("MQTT broker connection OK.")
        else:
            logging.info("MQTT broker bad connection: %s",
                         switcher.get(rc, "Unknown return code"))

    def on_disconnect(self, client, userdata, rc):
        logging.info("MQTT broker disconnecting: " + str(rc))
        logging.info("MQTT broker: will automatically reconnect")

    def message_callback_add(self, topic, callback, qos=None):
        super().message_callback_add(topic, callback)
        if (qos):
            self.subscribe(topic, qos)
        else:
            self.subscribe(topic, self.qos)
