import os
from bottle import Bottle, route, request, abort, static_file
from utils import send_text_message
from fsm import TocMachine

app = Bottle()
 
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
PORT = os.environ['PORT']

machine = TocMachine(
    states=[
        'user',
        'state1',
        'state2'
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'state1',
            'conditions': 'is_going_to_state1'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'state2',
            'conditions': 'is_going_to_state2'
        },
        {
            'trigger': 'go_back',
            'source': [
                'state1',
                'state2'
            ],
            'dest': 'user'
        }
    ],
    initial='user',
    auto_transitions=False,
)

@app.route("/webhook", method="GET")
def setup_webhook():
    mode = request.GET.get("hub.mode")
    token = request.GET.get("hub.verify_token")
    challenge = request.GET.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("WEBHOOK_VERIFIED")
        return challenge

    else:
        abort(403)

@app.route("/webhook", method="POST")
def webhook_handler():
    body = request.json
    print('\nFSM STATE: ' + machine.state)
    print('REQUEST BODY: ')
    print(body)

    if body['object'] == "page":
        event = body['entry'][0]['messaging'][0]
        machine.advance(event)
        return 'OK'
    # body = request.json
    # print('REQUEST BODY: ')
    # print(body)

    # if body['object'] == "page":
    #     event = body['entry'][0]['messaging'][0]
    #     if event.get("message"):
    #         text = event['message']['text']
    #         sender_id = event['sender']['id']
    #         send_text_message(sender_id, text)
    #     return 'OK'


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True, reloader=True)
