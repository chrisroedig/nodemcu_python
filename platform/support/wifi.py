import network
import time
import json
sta_if = network.WLAN(network.STA_IF)

def connect():
    print('loading wifi configuration')
    wconfig = json.loads(open('support/wifi_config.json').read())
    print('activating wifi station interface')
    sta_if.active(True)
    print('attempting wifi connection')
    sta_if.connect(wconfig['ssid'], wconfig['passphrase'])
    attempts = 1
    while not sta_if.isconnected():
        time.sleep(2)
        print('still waiting for connection')
        if attempts > 5:
            print('failed to connect')
            sta_if.active(False)
            break
        attempts+=1
    print('connected!')
    print('network config:', sta_if.ifconfig())
    return True

def disconnect():
    print('deactivating wifi station interface')
    sta_if.active(False)

def get_config():
    return sta_if.ifconfig()
