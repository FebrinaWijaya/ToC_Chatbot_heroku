import os
from bottle import Bottle, route, request, abort, static_file
from utils import send_text_message
from fsm import TocMachine

app = Bottle()
 
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
PORT = os.environ['PORT']

machine = TocMachine(
    states=[
        'init',
        'purpose',
        'adventure',
            'raja_ampat',
            'gili_island',
            'mount_bromo',
            #'mount_rinjani',
        'historical',
            'borobudur',
            'prambanan',
            'old_town',
            #'monument_of_people',
        'naturals',
            'bali',
            'lake_toba',
            'dieng_plateau',
            #'komodo_nat_park',
        'local_food',
            'satay',
            'rendang',
            'fried_rice'
            #'nasi_uduk',
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'init',
            'dest': 'purpose',
            'conditions': 'user_sent_something'
        },

        {
            'trigger': 'advance',
            'source': 'purpose',
            'dest': 'adventure',
            'conditions': 'is_travelling_for_adventure'
        },
        {
            'trigger': 'advance',
            'source': 'purpose',
            'dest': 'historical',
            'conditions': 'is_travelling_for_historical'
        },
        {
            'trigger': 'advance',
            'source': 'purpose',
            'dest': 'naturals',
            'conditions': 'is_travelling_for_naturals'
        },
        {
            'trigger': 'advance',
            'source': 'purpose',
            'dest': 'local_food',
            'conditions': 'is_travelling_for_local_food'
        },
        {
            'trigger': 'advance',
            'source': 'adventure',
            'dest': 'raja_ampat',
            'conditions': 'is_adventure_to_raja_ampat'
        },
        {
            'trigger': 'advance',
            'source': 'adventure',
            'dest': 'gili_island',
            'conditions': 'is_adventure_to_gili_island'
        },
        {
            'trigger': 'advance',
            'source': 'adventure',
            'dest': 'mount_bromo',
            'conditions': 'is_adventure_to_mount_bromo'
        },
        {
            'trigger': 'advance',
            'source': 'historical',
            'dest': 'borobudur',
            'conditions': 'is_historical_to_borobudur'
        },
        {
            'trigger': 'advance',
            'source': 'historical',
            'dest': 'prambanan',
            'conditions': 'is_historical_to_prambanan'
        },
        {
            'trigger': 'advance',
            'source': 'historical',
            'dest': 'old_town',
            'conditions': 'is_historical_to_old_town'
        },
        {
            'trigger': 'advance',
            'source': 'naturals',
            'dest': 'bali',
            'conditions': 'is_naturals_in_bali'
        },
        {
            'trigger': 'advance',
            'source': 'naturals',
            'dest': 'lake_toba',
            'conditions': 'is_naturals_in_lake_toba'
        },
        {
            'trigger': 'advance',
            'source': 'naturals',
            'dest': 'dieng_plateau',
            'conditions': 'is_naturals_in_dieng_plateau'
        },
        {
            'trigger': 'advance',
            'source': 'local_food',
            'dest': 'satay',
            'conditions': 'is_local_food_satay'
        },
        {
            'trigger': 'advance',
            'source': 'local_food',
            'dest': 'rendang',
            'conditions': 'is_local_food_rendang'
        },
        {
            'trigger': 'advance',
            'source': 'local_food',
            'dest': 'fried_rice',
            'conditions': 'is_local_fried_rice'
        },

        {
            'trigger': 'advance',
            'source': 'raja_ampat',
            'dest': 'gili_island',
            'conditions': 'is_next'
        },
        {
            'trigger': 'advance',
            'source': 'gili_island',
            'dest': 'mount_bromo',
            'conditions': 'is_next'
        },
        {
            'trigger': 'advance',
            'source': 'borobudur',
            'dest': 'prambanan',
            'conditions': 'is_next'
        },
        {
            'trigger': 'advance',
            'source': 'prambanan',
            'dest': 'old_town',
            'conditions': 'is_next'
        },
        {
            'trigger': 'advance',
            'source': 'bali',
            'dest': 'lake_toba',
            'conditions': 'is_next'
        },
        {
            'trigger': 'advance',
            'source': 'lake_toba',
            'dest': 'dieng_plateau',
            'conditions': 'is_next'
        },
        {
            'trigger': 'advance',
            'source': 'satay',
            'dest': 'rendang',
            'conditions': 'is_next'
        },
        {
            'trigger': 'advance',
            'source': 'rendang',
            'dest': 'fried_rice',
            'conditions': 'is_next'
        },
        {
            'trigger': 'advance',
            'source': [
                'raja_ampat',
                'gili_island',
                'mount_bromo',
                'borobudur',
                'prambanan',
                'old_town',
                'bali',
                'lake_toba',
                'dieng_plateau',
                'satay',
                'rendang',
                'fried_rice'
                ],
            'dest': 'purpose',
            'conditions': 'is_change_travel_purpose'
        },
        {
            'trigger': 'advance',
            'source': [
                'raja_ampat',
                'gili_island',
                'mount_bromo'
                ],
            'dest': 'adventure',
            'conditions': 'is_select_another_place'
        },
        {
            'trigger': 'advance',
            'source': [
                'borobudur',
                'prambanan',
                'old_town'
                ],
            'dest': 'historical',
            'conditions': 'is_select_another_place'
        },
        {
            'trigger': 'advance',
            'source': [
                'bali',
                'lake_toba',
                'dieng_plateau'
                ],
            'dest': 'naturals',
            'conditions': 'is_select_another_place'
        },
        {
            'trigger': 'advance',
            'source': [
                'satay',
                'rendang',
                'fried_rice'
                ],
            'dest': 'local_food',
            'conditions': 'is_select_another_place'
        }
    ],
    initial='init',
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True, reloader=True)
