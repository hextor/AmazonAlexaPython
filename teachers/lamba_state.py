#template for lambda functions in python


#==================== Main Handler ==================================
def lambda_handler(event, context):

    intent_name = event['request']['intent']['name']
    session = event['session']
    session['attributes']['california'] = { "EarlyHistoricalFacts": "California was founded in 1850.","StateHood" : "California was the 31st state to enter the union."}

    if intent_name == 'GiveStateCapitalIntent':
        #handle intent here
        return GiveStateCapitalIntent(event,session)
    elif intent_name == 'GiveStateBirdIntent':
        #handle intent here
        return GiveStateBirdIntent(event,session)
    elif intent_name == 'GiveStateHistoryIntent':
        #handle intent here
        return GiveStateHistoryIntent(event,session)



#================= Intent Handlers ==================================

def GiveStateCapitalIntent(event,session):
    sentence = "The state capital of california is Sacramento"
    return response(sentence, False)
def GiveStateBirdIntent(event,session):
    sentence = "The state bird is a Quail"
    return response(sentence, False)
def GiveStateHistoryIntent(event,session):
    sentence = session['attributes']['california']['EarlyHistoricalFacts']
    sentence += session['attributes']['california']['StateHood']
    return response(sentence, False)


#=====================Speech Function =============================

#call on this function to make alexa return speech
def response(text,should_end_session):
      return {
      "version": "1.0",
      "response": {
        "outputSpeech": {
          "text": text,
          "type": "PlainText"
        },
        "speechletResponse": {
          "outputSpeech": {
            "text": text
          },
          "shouldEndSession": should_end_session
        }
      },
      "sessionAttributes": {}
      }
