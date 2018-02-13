# --------------- Main handler ------------------
def lambda_handler(event, context):
    #Here are key values that hold a list and within it is an array
    #My thought process here was to make seperate listings/dictionaries for each detail piece and just add states as I go along.
    #session['attributes']['DETAILS_OF_STATES'] = {"california":["california got its name from a book called Las Sergas de Esplandian. In it was a mythical island named Califia","the golden state","sacramento"]}
    #session['attributes']['HISTORY_OF_STATES'] = {"california":["not much was known about the first inhabitants of california", "Juan Rodrieguez Cabrillo was the first to explore california", "the country of spain settled into california", "colonial days were probably horrible!"]}
    #session['attributes']['STATEHOOD_OF_STATES'] = {"california":["california was ceded to the US after the Mexican American war, then became part of the union as a slave free state in 1850","california was the 31st state to enter the union"]}


    #What I'll do next is create a variable for each state (just california) then make an array for each detail, then make the array for the answers inside
    #instead of doing what I did up there with using the name california, i'll just make a 2d array then pass in hard values
    #since we don't have to repeat the section we are looking at (not in the specs)
    #from 0 -> Pysical Features, last-> Famous People, so we going to list info in order
    #I'll add all the info later today, but it should work.
    #session['attributes'][myState][section#][answer#]
   # session['attributes']['california'] = [[]]


    #This variable was only created so that we don't have to type event everytime
    #Just a style choice, if you want to remove it just remember to remove argument parameters from our functions
    session = event['session']

    #OK trying out the way martin set up which should be more streamlined
    #that means: readable, easy to execute and debug

    session['attributes']['stateDiction'] = {
        "california" : {
            "historical" : {
                "details" : {
                    "nameOrigin" : "california got its name from a book called Las Sergas de Esplandian. In it was a mythical island named Califia",
                    "nickname" : "the golden state",
                    "capital" : "sacramento"
                },
                "facts" : {
                    "inhabitants" : "not much was known about the first inhabitants of california",
                    "explorer" : "Juan Rodrieguez Cabrillo was the first to explore california",
                    "settlers" : "the country of spain settled into california",
                    "colonialDays" : "colonial days were probably horrible!"

                },
                "statehood" : {
                    "stateOrigin" : "california was ceded to the US after the Mexican American war, then became part of the union as a slave free state in 1850",
                    "stateNumber" : "california was the 31st state to enter the union"
                }
            },
            "features" : {
                "physical" : {
                    "regions" : "California has 4 major regions. Coastal, central valley, desert, and mountains.",
                    "lohi" : "Mount Whitney is the highest point of evelavation in California, at only a mere fourty four hundred meters above sea level. Badwater Basin in death valley is the lowest point in california at 85 meters below sea level.",
                    "stateSize" : "California is the 3rd biggest state in the US, right behind Texas."
                },
                "political" : {
                    "populationCount" : "as of 2016, the population count is 36 million",
                    "countyCount" : "there are 58 counties in california, orange county got its name because they mostly grew oranges when they divided up the counties.",
                    "majorCities": "in california we have Los Angeles, san francisco, san diego, and a whole other number of cities. Probably the nicest major city is Santa Barbara."
                },
                "economy" : {
                    "economyType" : "California is the leading tech giant of the nation and is the major contributor of agriculture goods and aeorspace engineering.",
                    "agriculture" : "California supplies the nation with most of its almonds, pistachios, avocados, and strawberries. It comes second in producing oranges.",
                    "manufacture" : "California leads in supplying electrical equipment, components, and military communication equipment. It comes second in manurfacturing computer machinery."
                },
                "weather" : {
                    "description": "it is super hot and only rains when my car windows are down"
                },
                "visitorsGuide" : {
                    "description" : "When coming to california. People should visit the Queen Mary, especially during halloween when the bloody mary roams the boat. Napa Valley is also a great place for adults who would like to do a little wine tasting."
                    +"For the kids, we have disney land! most nights they run a mini parade and light fireworks above the disney castle. If you have no clue what to do but just want to enjoy the weather, you can take a drive the pacific coast highway."
                    +"It offers a beautiful scenic drive for the lucky person in your passegener seat. Since you as the driver needs to keep both eyes on the road since it can get a little scary."
                },
                "famousPeople" : {
                    "description" : "There are way to many famouse people in california. They help turn the gears of the economy whether they be an actor or inventor."
                }
            }
        }
    }



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
        return HistoricalInformationIntent(event, session)
    elif event['request']['intent']['name'] == 'DetailsIntent':
        return DetailsIntent(event,session)
    elif event['request']['intent']['name'] == 'HistoricalFactsIntent':
        return HistoricalFactsIntent(event,session)
    elif event['request']['intent']['name'] == 'StatehoodHistoryIntent':
        return StatehoodHistoryIntent(event,session)
    elif event['request']['intent']['name'] == 'StateFeaturesIntent':
        return StateFeaturesIntent(event,session)
    elif event['request']['intent']['name'] == 'PhysicalFeaturesIntent':
        return PhysicalFeaturesIntent(event,session)
    elif event['request']['intent']['name'] == 'PoliticalFeaturesIntent':
        return PoliticalFeaturesIntent(event,session)
    elif event['request']['intent']['name'] == 'EconomyIntent':
        return EconomyIntent(event,session)
    elif event['request']['intent']['name'] == 'WeatherIntent':
        return WeatherIntent(event,session)
    elif event['request']['intent']['name'] == 'VisitorsGuideIntent':
        return VisitorsGuideIntent(event,session)
    elif event['request']['intent']['name'] == 'FamousPeopleIntent':
        return FamousPeopleIntent(event,session)

# --------------- Functions that control the skill's behavior ------------------
def HistoricalInformationIntent(event,session):
    session['attributes']['choice'] = event['request']['intent']['slots']['stateChoice']['value']
    sentence = "Ok let's talk about " + session['attributes']['choice'] + ". "
    sentence += "What would you like to know? All of it? Basic details? Historical Facts? Statehood?"
    return response(sentence, session['attributes'], False)

def DetailsIntent(event,session):
    myState = session['attributes']['choice']
    sentence = session['attributes']['stateDiction'][myState]['historical']['details']['nameOrigin'] + " "
    sentence += "Its nicknamed " + session['attributes']['stateDiction'][myState]['historical']['details']['nickname'] + ". "
    sentence += "And its state capital is " + session['attributes']['stateDiction'][myState]['historical']['details']['capital'] + ". "
    return response(sentence, session['attributes'], False)

def HistoricalFactsIntent(event,session):
    myState = session['attributes']['choice']
    sentence = session['attributes']['stateDiction'][myState]['historical']['facts']['inhabitants'] + ". "
    sentence += session['attributes']['stateDiction'][myState]['historical']['facts']['explorer'] + ". "
    sentence += session['attributes']['stateDiction'][myState]['historical']['facts']['settlers'] + ". "
    sentence += session['attributes']['stateDiction'][myState]['historical']['facts']['colonialDays'] + ". "
    return response(sentence, session['attributes'], False)

def StatehoodHistoryIntent(event, session):
    myState = session['attributes']['choice']
    sentence = session['attributes']['stateDiction'][myState]['historical']['statehood']['stateOrigin']+". "
    sentence = session['attributes']['stateDiction'][myState]['historical']['statehood']['stateNumber']+". "
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
    sentence = session['attributes']['stateDiction'][myState]['features']['physical']['regions']+". "
    sentence += session['attributes']['stateDiction'][myState]['features']['physical']['lohi'] +". "
    sentence += session['attributes']['stateDiction'][myState]['features']['physical']['stateSize']+". "
    return response(sentence, session['attributes'], False)

def PoliticalFeaturesIntent(event,session):
    myState = session['attributes']['choice']
    sentence = session['attributes']['stateDiction'][myState]['features']['political']['populationCount'] +". "
    sentence += session['attributes']['stateDiction'][myState]['features']['political']['countyCount'] +". "
    sentence += session['attributes']['stateDiction'][myState]['features']['political']['majorCities'] +". "
    return response(sentence, session['attributes'], False)

def EconomyIntent(event,session):
    myState = session['attributes']['choice']
    sentence = session['attributes']['stateDiction'][myState]['features']['economy']['economyType'] +". "
    sentence += session['attributes']['stateDiction'][myState]['features']['economy']['agriculture'] +". "
    sentence += session['attributes']['stateDiction'][myState]['features']['economy']['manufacture'] +". "
    return response(sentence, session['attributes'], False)

def WeatherIntent(event,session):
    myState = session['attributes']['choice']
    sentence = session['attributes']['stateDiction'][myState]['features']['weather']['description'] +". "
    return response(sentence, session['attributes'], False)

def VisitorsGuideIntent(event,session):
    myState = session['attributes']['choice']
    sentence = session['attributes']['stateDiction'][myState]['features']['visitorsGuide']['description'] +". "
    return response(sentence, session['attributes'], False)

def FamousPeopleIntent(event,session):
    myState = session['attributes']['choice']
    sentence = session['attributes']['stateDiction'][myState]['features']['famousPeople']['description'] +". "
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
