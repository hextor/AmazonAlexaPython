import boto3

# --------------- Helpers that build all of the responses ----------------------
# DO NOT change any of the code inside build_speechlet_response() or build_response()

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

# --------------- Functions that control the skill's behavior ------------------
# This is the section where we get creative. Add functions to handle your specific intents
# DO NOT change the names of get_welcome_response(), handle_session_end_request()
# DO NOT change what each function "returns"
# DO NOT change the names of the variables already initialized. ONLY change what values they hold
# ONLY change/add/remove the functions that start with "MyIntentFunction..."


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Hello, welcome to your roster list!"

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Roster roster roster!" 
    should_end_session =  False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

'''==================================================
STARTOF: ROSTER FUNCTIONS
====================================================='''

'''==================================================
FUNCTION: CreateRoster
DESCRIPTION: Creates a table in dynamodb that has a student and gold star field
    It will try to create a table, if it fails it will return and error 'ResourceInUse'
    Mean the table is already created.
PROMPTS:
    Success: Create the table. Tell the user the table was created
    Failure: Tell the user the table already exists
    
QUESTION:
    Should we ask for a name when creating the table or just hardcode it in.
    Like I do here.
    If we hardcode the table name then it can be easier for individuals to follow in my opinion.
====================================================='''
def CreateRoster(intent, session):
    dynamodb = boto3.resource('dynamodb')
    
    try:
        #try to create the table, if we fail we will fall into the `except` block
        table = dynamodb.create_table(
        TableName='HectorRoster',
        KeySchema=[
        #we are telling the database that student names will be unique (can't have two people of the same name)
            {
                'AttributeName': 'StudentName',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
        #creating a column for students as a string and gold stars as a number
            {
                'AttributeName': 'StudentName',
                'AttributeType': 'S'
            }
        ],
        #this is just saying how fast we should read and write the data
        # default is 5, no need to go more than that
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
        )
        speech_output = "Successfully created a table named Hector Roster"
    except:
        speech_output = "Table named Hector Roster already exists!"
    
    session_attributes = {}
    should_end_session =  False #change boolean when needed
    card_title = "Creating the roster!"
    reprompt_text = "Roster is available for use."
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

'''==================================================
FUNCTION: AddStudent
DESCRIPTION: Adds a student to the roster by creating a unique key after the students name,
    and creating a field for the student for gold stars
    
PROMPTS:
    Success: Adds the user successfully to the table
    Failure: No fail check, but it should be key error if the student name already exists.
        so two people with the same name will have issues

====================================================='''       
def AddStudent(intent, session):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('HectorRoster')
    
    student = intent['slots']['myStudent']['value']
    
    table.put_item(
    Item={
        'StudentName': student,
        'GoldStar': 0
    }
    )
    
    session_attributes = {}
    should_end_session =  False #change boolean when needed
    card_title = "Adding a student!"
    speech_output = "Added the student " + student + " to your roster."
    reprompt_text = "The student " + student + ", was added to your roster."
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
'''==================================================
FUNCTION: RemoveStudent
DESCRIPTION: Removes a student to the roster by looking for their name (which should be unique)
    
PROMPTS:
    Success: Removes the user successfully from the table
    Failure: No fail check, but it should be key error if the student doesn't exist

====================================================='''           
def RemoveStudent(intent, session):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('HectorRoster')
    
    student = intent['slots']['myStudent']['value']
    
    table.delete_item(
    Key={
        'StudentName': student
    }
    )
    
    session_attributes = {}
    should_end_session =  False #change boolean when needed
    card_title = "Removing a student!"
    speech_output = "Removed the student " + student + " from your roster."
    reprompt_text = "The student " + student + ", was removed from your roster."
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        

'''==================================================
FUNCTION: GetStudent
DESCRIPTION: Gets info on a student from the roster by looking for their name (which should be unique)
    When you get the name it is given as a dictionary with the root being 'Item'
    stucturally it looks this:
        'Item' : {
            'StudentName': 'Hector',
            'GoldStar': 0
        }
    
PROMPTS:
    Success: Gets info on user successfully
    Failure: No fail check, but it should be key error if the student doesn't exist

====================================================='''  
def GetStudent(intent, session):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('HectorRoster')
    
    student = intent['slots']['myStudent']['value']
    
    info = table.get_item(
    Key={
        'StudentName': student
    }
    )
    
    session_attributes = {}
    should_end_session =  False #change boolean when needed
    card_title = "Getting info on Student"
    speech_output = "Your student, " + student + " has " + info['Item']['GoldStar'] + " gold stars"
    reprompt_text = "The student " + student + " has " + info['Item']['GoldStar'] + " gold stars"
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        

'''==================================================
FUNCTION: GiveStar
DESCRIPTION: Gives stars to a student from the roster by looking for their name (which should be unique)
    First we need to get the number of stars the user currently has.
    Using the get_item() function.
    When we get the info on the student, we save the data from the gold star, because that's the only thing we are interested in
    Then we add the old star value with the given star value (parsed as an int because it comes in as a string originally)
    Then we can 'SET' the data to the new value
    
PROMPTS:
    Success: Gives stars to the user successfully
    Failure: No fail check, but it should be key error if the student doesn't exist

====================================================='''  
def GiveStar(intent, session):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('HectorRoster')
    
    student = intent['slots']['myStudent']['value']
    stars =  intent['slots']['myStar']['value']
    
    studentInfo = table.get_item(Key={'StudentName': student})
    oldStars = studentInfo['Item']['GoldStar']
    newStars = int(stars) + oldStars
    
    info = table.update_item(
    Key={
        'StudentName': student
    },
    UpdateExpression='SET GoldStar = :val1',
    ExpressionAttributeValues={
        ':val1': newStars
    }
    )
    
    session_attributes = {}
    should_end_session =  False #change boolean when needed
    card_title = "Giving Student Stars!"
    speech_output = "Your student, " + student + " has been given " + stars + " gold stars"
    reprompt_text = "The student " + student + " has " + stars + " more gold stars"
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
'''==================================================
FUNCTION: RemoveStar
DESCRIPTION: Removes stars from a student from the roster by looking for their name (which should be unique)
    Similar to GiveStar.
    First we need to get the number of stars the user currently has.
    Using the get_item() function.
    When we get the info on the student, we save the data from the gold star, because that's the only thing we are interested in
    Then we subtract the old star value with the given star value (parsed as an int because it comes in as a string originally)
    Then we can 'SET' the data to the new value
    
PROMPTS:
    Success: Removes stars from the user successfully
    Failure: No fail check, but it should be key error if the student doesn't exist

====================================================='''  
def RemoveStar(intent, session):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('HectorRoster')
    
    student = intent['slots']['myStudent']['value']
    stars =  intent['slots']['myStar']['value']
    
    studentInfo = table.get_item(Key={'StudentName': student})
    oldStars = studentInfo['Item']['GoldStar']
    newStars = oldStars - int(stars)
    
    info = table.update_item(
    Key={
        'StudentName': student
    },
    UpdateExpression='SET GoldStar = :val1',
    ExpressionAttributeValues={
        ':val1': newStars
    }
    )
    
    session_attributes = {}
    should_end_session =  False #change boolean when needed
    card_title = "Removing Student Stars!"
    speech_output = "Your student, " + student + " has lost " + stars + " gold stars"
    reprompt_text = "The student " + student + " has " + stars + " less gold stars"
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
        
'''==================================================
ENDOF: ROSTER FUNCTIONS
====================================================='''
  
  
'''==================================================
STARTOF: MY NAME AND REPEAT TESTINGS
====================================================='''
def MyNameIs(intent, session):
    username = intent['slots']['name']['value']
    session_attributes = {'username': username}
    
    should_end_session =  False #change boolean when needed
    card_title = "Is this your name? " + username
    speech_output = "Hello, " + username
    reprompt_text = "Roster was made for you."
    
    #I pass session to the build response
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def RepeatName(intent, session):
    session_attributes = {}
    #print session  - just to check how it was being called
    #I'm thinking after it is passed to the build response it creates the attribute tag like normal
    
    should_end_session =  False #change boolean when needed
    card_title = "Let me repeat!"
    speech_output = "Your name is, " + session['attributes']['username']
    reprompt_text = "Did i get your name right, " + session['attributes']['username']
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
'''==================================================
ENDOF: MY NAME AND REPEAT TESTINGS
====================================================='''


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Goodbye"

    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# --------------- Events ------------------
# All Alexa skills have events within their life, LaunchRequest (beginning), IntentRequest (middle), and
# SessionEnded (end). The following code just controls whether we are at the beginning, middle,
# or end of our skill. All we need to change here are the intent function names in on_intent().

def on_session_started(session_started_request, session):
     """ Called when the session starts """
    #not sure what needs to go here?

def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """
    # Dispatch to your skill's launch
    return get_welcome_response()

def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    #When adding new intent functions change the names in these 'if' statements
    # Dispatch to your skill's intent handlers
    '''================================================
        STARTOF: ROSTER INTENT CALLS    
    ================================================'''
    if intent_name == "CreateRosterIntent":
        return CreateRoster(intent, session)
    elif intent_name == "AddStudentIntent":
        return AddStudent(intent, session)
    elif intent_name == "RemoveStudentIntent":
        return RemoveStudent(intent, session)
    elif intent_name == "GetStudentIntent":
        return GetStudent(intent, session)
    elif intent_name == "GiveStarIntent":
        return GiveStar(intent, session)
    elif intent_name == "RemoveStarIntent":
        return RemoveStar(intent, session)
    # ENDOF: ROSTER INTENT CALLS    
    elif intent_name == "MyNameIsIntent":
        return MyNameIs(intent, session)
    elif intent_name == "RepeatNameIntent":
        return RepeatName(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    
    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
 

