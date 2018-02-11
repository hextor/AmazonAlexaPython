#What saves more memory in the long run? accessing attributes directly or setting them to a local variable then calling that variable
# --------------- Main handler ------------------
def lambda_handler(event, context):
    session = event['session']
    session['attributes']['DETAILS_OF_STATES'] = {"california":["california got its name from a book called Las Sergas de Esplandian. In it was a mythical island named Califia","the golden state","sacramento"]}
    session['attributes']['HISTORY_OF_STATES'] = {"california":["not much was known about the first inhabitants of california", "Juan Rodrieguez Cabrillo was the first to explore california", "the country of spain settled into california", "colonial days were probably horrible!"]}
    #checking if this starts
    #Will users be allowed to choose different states?
    #Having kids work on the same code seems like a nightmare.
    #Gotta teach them version control!
    #Here we assume we only need to create california.
    #But I'll make it into a list in case we need to add stuff later.

    #this one will play a courtesy response if nothing was specified when opening the program
    if event['request']['type'] == "LaunchRequest":
        return LaunchRequest(event, session)
    elif event['request']['intent']['name'] == 'StateIntent':
        return StateIntent(event, session)
    elif event['request']['intent']['name'] == 'DetailsIntent':
        return DetailsIntent(event,session)
    elif event['request']['intent']['name'] == 'HistoricalFactsIntent':
        return HistoricalFactsIntent(event,session)
    elif event['request']['intent']['name'] == 'EverythingIntent':
        return EverythingIntent(event,session)

# --------------- Functions that control the skill's behavior ------------------
def StateIntent(event,session):
    session['attributes']['choice'] = event['request']['intent']['slots']['userChoice']['value']
    sentence = "Ok let's talk about " + session['attributes']['choice'] + ". "
    sentence += "What would you like to know?"
    return response(sentence, session['attributes'], False)

def DetailsIntent(event,session):
    sentence = session['attributes']['DETAILS_OF_STATES'][session['attributes']['choice']][0] + ". "
    sentence += "Its nicknamed " + session['attributes']['DETAILS_OF_STATES'][session['attributes']['choice']][1] + ". "
    sentence += "And its state capital is " + session['attributes']['DETAILS_OF_STATES'][session['attributes']['choice']][2] + ". "
    return response(sentence, session['attributes'], False)

def HistoricalFactsIntent(event,session):
    sentence = session['attributes']['HISTORY_OF_STATES'][session['attributes']['choice']][0] + ". "
    sentence += session['attributes']['HISTORY_OF_STATES'][session['attributes']['choice']][1] + ". "
    sentence += session['attributes']['HISTORY_OF_STATES'][session['attributes']['choice']][2] + ". "
    sentence += session['attributes']['HISTORY_OF_STATES'][session['attributes']['choice']][3] + ". "
    return response(sentence, session['attributes'], False)

def EverythingIntent(event, session):
    someValue = event['request']['intent']['slots']['userChoice_']['value']
    if someValue:
        session['attributes']['choice'] = someValue
        #pull the response strings out of these guys.
    return response(DetailsIntent(event, session) and HistoricalFactsIntent(event, session), session['attributes'], False)

#---------------- Courtesy responses ------------------------------------------
def LaunchRequest(event, session):
    sentence ="Welcome to the state information booth. Would you like to talk about a state's historical information or a state's features?"
    sentence += " We can also talk about everything!"
    response(sentence, session['attributes'], False)

# --------------- Helper that build all of the responses ----------------------

def response(text, session_attributes, should_end_session):
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
    "sessionAttributes": session_attributes
    }
