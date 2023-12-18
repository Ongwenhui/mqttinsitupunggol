import sys
import logging
from datetime import datetime as dt
import time
import csv
import json
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
from awsiot import iotshadow
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
from uuid import uuid4

# for value in values:
#     print(value)
ID = values[0]
onoff = values[1]
unixtime = str(dt.now())
# # location_id = 'PCP_820222'
# location_id = 'NTU_YNG_639798'
# # location_id = 'PWP'
location_id= 'demo'
#onoff = 1.0
shadow_value = {"ID": ID, "onoff" : onoff, "unixtime": unixtime, "location_id": location_id}
#shadow_value = {"ID": 9999, "onoff" : onoff, "unixtime": str(dt.now()), "location_id": "demo"}
# print(dict)

def change_shadow_value(value, update_desired=True):
    token = str(uuid4())
    if update_desired == True:
        request = iotshadow.UpdateNamedShadowRequest(
            shadow_name = shadow_name,
            thing_name = thing_name,
                state=iotshadow.ShadowState(
                    reported=value,
                    desired=value
                ),
            client_token=token
        )
    print(request)
    shadow_client.publish_update_named_shadow(request, mqtt.QoS.AT_LEAST_ONCE)
    
def statereturncheckcallback(topic, payload, retain=True):
    if payload:
        print(payload)
        global state
        state = float((str(payload).split("state")[1]).split(" ")[1].split("}")[0])
        print(state)
    


ENDPOINT = "a5i03kombapo4-ats.iot.ap-southeast-1.amazonaws.com"
CLIENT_ID = "enviropluspi"
PATH_TO_CERTIFICATE = "/Users/ongwenhui/Desktop/certs/testcode/nbsiot/9972587da4767d10db7001fc18bab5b9124945c4762ebf246b6266e08352970b-certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "/Users/ongwenhui/Desktop/certs/testcode/nbsiot/9972587da4767d10db7001fc18bab5b9124945c4762ebf246b6266e08352970b-private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "/Users/ongwenhui/Desktop/certs/testcode/nbsiot/root.pem"
TOPIC = "test/nbs"

state = None
thing_name = "WenhuiAWSthing"
shadow_name = "mqttnbs"
statereturn_topic = "mqtt/statereturn"

event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=ENDPOINT,
            cert_filepath=PATH_TO_CERTIFICATE,
            pri_key_filepath=PATH_TO_PRIVATE_KEY,
            client_bootstrap=client_bootstrap,
            ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
            client_id=CLIENT_ID,
            clean_session=False,
            keep_alive_secs=6
            )
connected_future = mqtt_connection.connect()
shadow_client = iotshadow.IotShadowClient(mqtt_connection)
print("Connecting to {} with client ID '{}'...".format(
        ENDPOINT, CLIENT_ID))
connected_future.result()
# Make the connect() call
print("Connected!")
change_shadow_value(shadow_value)
backoff_time = int(time.time())
num_retries = 5
print(f'current time is {backoff_time}, will send a request every 5 seconds and timeout after {num_retries} retries.')
while True:
    
    mqtt_connection.subscribe(
        topic=statereturn_topic,
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=statereturncheckcallback
    )
    time.sleep(0.5)
    if state == onoff:
        break
# Publish message to server desired number of times.
#iotClient.publishAsync(TOPIC, json.dumps(dict), 1)
print('done')
