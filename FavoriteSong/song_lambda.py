# --------------- Main handler ------------------
def lambda_handler(event, context):
    intent_name = event['request']['intent']['name']
    session = event['session']

    if intent_name == 'SongIntent':
        return SongIntent(event, session)

# --------------- Functions that control the skill's behavior ------------------
def SongIntent(event, session):
    sentence = "Your favorite song is My Guitar Gently Weeps by the Beatles and also Black Bird which is also by the Beatles"
    return response(sentence, session['attributes'], False)

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
