import os
import requests


GRAPH_URL = "https://graph.facebook.com/v2.6"
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']


def send_text_message(id, text):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message": {"text": text}
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response

def send_image_url(id, img_path, img_type):
    fb_url = GRAPH_URL + '/me/messages'
    data = {
        'recipient': '{"id":'+ id + '}',
        'message': '{"attachment":{"type":"image", "payload":{}}}'
    }
    files = {
        'filedata': (os.path.basename(img_path), open(img_path, 'rb'), 'image/'+img_type)}
    params = {'access_token': ACCESS_TOKEN}
    response = requests.post(fb_url, params=params, data=data, files=files)
    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response



def send_button_message(id, text, buttons):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message": {"attachment":{
          "type":"template",
          "payload":{
            "template_type":"button",
            "text": text,
            "buttons":buttons
          }
        }}
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response
"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
