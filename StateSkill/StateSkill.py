#What saves more memory in the long run? accessing attributes directly or setting them to a local variable then calling that variable
# --------------- Main handler ------------------
def lambda_handler(event, context):
    #This variable was only created so that we don't have to type event everytime
    #Just a style choice, if you want to remove it just remember to remove argument parameters from our functions
    session = event['session']

    #Here are key values that hold a list and within it is an array
    #My thought process here was to make seperate listings/dictionaries for each detail piece and just add states as I go along.
    session['attributes']['DETAILS_OF_STATES'] = {"california":["california got its name from a book called Las Sergas de Esplandian. In it was a mythical island named Califia","the golden state","sacramento"]}
    session['attributes']['HISTORY_OF_STATES'] = {"california":["not much was known about the first inhabitants of california", "Juan Rodrieguez Cabrillo was the first to explore california", "the country of spain settled into california", "colonial days were probably horrible!"]}
    session['attributes']['STATEHOOD_OF_STATES'] = {"california":["california was ceded to the US after the Mexican American war, then became part of the union as a slave free state in 1850","california was the 31st state to enter the union"]}


    #What I'll do next is create a variable for each state (just california) then make an array for each detail, then make the array for the answers inside
    #instead of doing what I did up there with using the name california, i'll just make a 2d array then pass in hard values
    #since we don't have to repeat the section we are looking at (not in the specs)
    #from 0 -> Pysical Features, last-> Famous People, so we going to list info in order
    #I'll add all the info later today, but it should work.
    #session['attributes'][myState][section#][answer#]
    session['attributes']['california'] = [[]]



    #checking if this starts
    #Will users be allowed to choose different states?
    #Having kids work on the same code seems like a nightmare.
    #Gotta teach them version control!
    #Here we assume we only need to create california.
    #But I'll make it into a list in case we need to add stuff later.

    #this one will play a courtesy response if nothing was specified when opening the program
    if event['request']['type'] == "LaunchRequest":
        return LaunchRequest(event, session)
    elif event['request']['intent']['name'] == 'HistoricalInformationIntent':
        return StateIntent(event, session)
    elif event['request']['intent']['name'] == 'DetailsIntent':
        return DetailsIntent(event,session)
    elif event['request']['intent']['name'] == 'HistoricalFactsIntent':
        return HistoricalFactsIntent(event,session)
    elif event['request']['intent']['name'] == 'StatehoodHistoryIntent':
        return StatehoodHistoryIntent(event,session)
    elif event['request']['intent']['name'] == 'StateFeaturesIntent':
        return StateFeaturesIntent(event,session):
    elif event['request']['intent']['name'] == 'PhysicalFeaturesIntent':
        return StateFeaturesIntent(event,session):
    elif event['request']['intent']['name'] == 'PoliticalFeaturesIntent':
        return StateFeaturesIntent(event,session):
    elif event['request']['intent']['name'] == 'EconomyIntent':
        return StateFeaturesIntent(event,session):
    elif event['request']['intent']['name'] == 'WeatherIntent':
        return StateFeaturesIntent(event,session):
    elif event['request']['intent']['name'] == 'VisitorsGuideIntent':
        return StateFeaturesIntent(event,session):
    elif event['request']['intent']['name'] == 'FamousPeopleIntent':
        return StateFeaturesIntent(event,session):

# --------------- Functions that control the skill's behavior ------------------
def HistoricalInformationIntent(event,session):
    session['attributes']['choice'] = event['request']['intent']['slots']['stateChoice']['value']
    sentence = "Ok let's talk about " + session['attributes']['choice'] + ". "
    sentence += "What would you like to know? All of it? Basic details? Historical Facts? Statehood?"
    return response(sentence, session['attributes'], False)

def DetailsIntent(event,session):
    myState = session['attributes']['choice']
    sentence = session['attributes']['DETAILS_OF_STATES'][myState][0] + ". "
    sentence += "Its nicknamed " + session['attributes']['DETAILS_OF_STATES'][myState][1] + ". "
    sentence += "And its state capital is " + session['attributes']['DETAILS_OF_STATES'][myState][2] + ". "
    return response(sentence, session['attributes'], False)

def HistoricalFactsIntent(event,session):
    myState = session['attributes']['choice']
    sentence = session['attributes']['HISTORY_OF_STATES'][myState][0] + ". "
    sentence += session['attributes']['HISTORY_OF_STATES'][myState][1] + ". "
    sentence += session['attributes']['HISTORY_OF_STATES'][myState][2] + ". "
    sentence += session['attributes']['HISTORY_OF_STATES'][myState][3] + ". "
    return response(sentence, session['attributes'], False)

def StatehoodHistoryIntent(event, session):
    myState = session['attributes']['choice']
    sentence = session['attributes']['STATEHOOD_OF_STATES'][myState][0]+". "
    sentence = session['attributes']['STATEHOOD_OF_STATES'][myState][1]+". "
    return response(sentence, session['attributes'], False)

def StateFeaturesIntent(event,session):
    session['attributes']['choice'] = event['request']['intent']['slots']['stateChoice']['value']
    sentence = "Ok let's talk about " + session['attributes']['choice'] + ". "
    sentence += "What would you like to know? Physical Features? Politcal Features? Economy? Weather? Want a Visitors Guide? or maybe the kind of Famous People that live here."
    return response(sentence, session['attributes'], False)

#PhysicalFeatures is the first thing in the array.
#session['attributes'][myState][section#][answer#]
def PhysicalFeaturesIntent(event,session):
    myState = session['attributes']['choice']
    sentence = session['attributes'][myState][0][0] +". "
    sentence = session['attributes'][myState][0][1] +". "
    sentence = session['attributes'][myState][0][2] +". "
    return response(sentence, session['attributes'], False)

def PoliticalFeaturesIntent(event,session):
    myState = session['attributes']['choice']
    sentence = session['attributes'][myState][0][0] +". "
    sentence = session['attributes'][myState][0][1] +". "
    sentence = session['attributes'][myState][0][2] +". "
    return response(sentence, session['attributes'], False)

def EconomyIntent(event,session):
    myState = session['attributes']['choice']
    sentence = session['attributes'][myState][0][0] +". "
    sentence = session['attributes'][myState][0][1] +". "
    sentence = session['attributes'][myState][0][2] +". "
    return response(sentence, session['attributes'], False)

def WeatherIntent(event,session):
    myState = session['attributes']['choice']
    sentence = session['attributes'][myState][0][0] +". "
    return response(sentence, session['attributes'], False)

def VisitorsGuideIntent(event,session):
    myState = session['attributes']['choice']
    sentence = session['attributes'][myState][0][0] +". "
    return response(sentence, session['attributes'], False)
def FamousPeopleIntent(event,session):
    myState = session['attributes']['choice']
    sentence = session['attributes'][myState][0][0] +". "
    return response(sentence, session['attributes'], False)


#Ok we do have to say everything at some point.
#def EverythingIntent(event, session):
#    someValue = event['request']['intent']['slots']['userChoice_']['value']
#    if someValue:
#        session['attributes']['choice'] = someValue
#        #pull the response strings out of these guys.
#    return response(DetailsIntent(event, session) and HistoricalFactsIntent(event, session), session['attributes'], False)

#---------------- Courtesy responses ------------------------------------------
def LaunchRequest(event, session):
    sentence ="Welcome to the state information booth. Would you like to talk about a state's historical information or a state's features?"
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
