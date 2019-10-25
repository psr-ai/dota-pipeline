import logging, requests, datetime

from library.constants import GET_MATCH_DETAILS, DATABASE_URL, LOG_ROOT, DATA_ROOT

from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient

logging.basicConfig(filename=LOG_ROOT+'match_details_fetcher.log', level=logging.DEBUG, format='%(levelname)s:%(asctime)s %(message)s')

client = FaunaClient(secret="secret", domain=DATABASE_URL, scheme="http", port="8443")


def getMatchDetails(matchID, processName, key):
    try:
        startTime = datetime.datetime.now()
        response = requests.get(GET_MATCH_DETAILS, params={'match_id': matchID, 'key': key})
        endTime = datetime.datetime.now()

        if response.status_code == 200:
            try:
                responseJson = response.json()

                writeDataToFile(responseJson)
                addProvenance(responseJson, startTime, endTime, processName)
                writeDataToDatabase(responseJson, matchID)

                logging.info(f'Successfully written match details for match {matchID}')

            except ValueError as v:
                logging.error(f'Decoding JSON has failed: {str(v)}')
        else:
            logging.error(f'Response status code: {response.status_code}')
        return response.status_code
    except Exception as e:
        logging.error(f'Error occurred {str(e)}')
    return


def writeDataToDatabase(responseJson, matchID):
    logging.debug(f'Persisting {responseJson} to database')

    client.query(
        q.create(
            q.ref(q.collection("matches"), matchID),
            { "data" : responseJson }
        )
    )
    logging.debug(f'Added matchID {matchID} to database')

def addProvenance(responseJson, startTime, endTime, processName):
    responseJson['provenance'] = {}
    responseJson['provenance']['dataFetchStage'] = {}

    responseJson['provenance']['dataFetchStage']['startTime'] = str(startTime)
    responseJson['provenance']['dataFetchStage']['apiCallDuration'] = str(endTime - startTime)
    responseJson['provenance']['dataFetchStage']['processedBy'] = processName

def writeDataToFile(responseJson):
    f = open(DATA_ROOT+'match_details.log', 'a+')
    f.write("\n")
    f.write(str(responseJson))
    f.close()