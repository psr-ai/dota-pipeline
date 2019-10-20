import requests, time, logging
from constants.constants import GET_MATCH_HISTORY, KEY_1

logging.basicConfig(filename='serial_match_fetcher.log', level=logging.DEBUG, format='%(levelname)s:%(asctime)s %(message)s')
last_match_id = None

while True:
    logging.info(f'Getting match history')
    params = {'key': KEY_1, 'skill': 3, 'min_players': 10}
    try:
        response = requests.get(GET_MATCH_HISTORY, params=params)
        if response.status_code == 200:
            try:
                response_json = response.json()
                matches = response_json['result']['matches']
                match_ids = [match['match_id'] for match in matches]
                match_ids.sort()
                f = open('serial_matches.log', 'a+')
                f.write("\n")
                params['start_at_match_id'] = last_match_id
                last_match_id = match_ids[0]
                logging.info(f'Successfully written {len(matches)} records')
                f.write("\n".join(map(lambda t: str(t), match_ids)))
                f.close()
            except ValueError as v:
                logging.error(f'Decoding JSON has failed: {str(v)}')
        else:
            logging.error(f'Response status code: {response.status_code}')
    except Exception as e:
        logging.error(f'Error occurred {str(e)}, retrying')
    time.sleep(2)
