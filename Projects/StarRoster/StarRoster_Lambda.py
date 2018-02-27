from __future__ import print_function
#Boto is an AWS SDK for python used for amazon services
import boto3
# --------------- Main handler ------------------
def lambda_handler(event, context):

    #importing an existing table

    #first we need to get the service resource
    dynamodb = boto3.resource('dynamodb')
    #then we access the table that holds our information and store it into an object-variable
    #when I created the table I named the uniqueID to name for the student's name
    #at some point it will need to change but for sake of example it's fine
    studentTable = dynamodb.Table('STUDENTS')

    intent_name = event['request']['intent']['name']
    session = event['session']

    #Here I will pass the database table to each of my functions as a reference
    #The idea being that it will limit on calling the table
    #I will play around with it and see if it makes a difference
    if intent_name == 'SetStudentInfoIntent':
        return SetStudentInfo(event, session, studentTable)
    elif intent_name == 'GetStudentInfoIntent':
        return GetStudentInfo(event, session, studentTable)
    elif intent_name == 'GiveStudentStarIntent':
        return GiveStudentStar(event, session, studentTable)
    elif intent_name == 'DeleteStudentIntent':
        return DeleteStudent(event, session, studentTable)

# --------------- Functions that control the skill's behavior ------------------
def SetStudentInfo(event, session, studentTable):
    studentname = event['request']['intent']['slots']['setName']['value']

    #put_item is a function inside of boto3 that will create a new item
    #Item is the tutorial word that is used when creating a new object in our database
    #I'm sure another word can be used but we should stick to the standards
    #Item needs to be an kind of JSON list
    #name is our uniqueID for the table (at some point it will need to change since multiple people can have the same name)
    #the key ID that is creating in our dynamoDB page must be included in our Item or else you'll get an error
    #Here I created an item that holds a name and a star amount
    studentTable.put_item(Item={'name': studentname, 'stars': 0})
    sentence = "Ok, I have included a new student named " + studentname
    return response(sentence, session['attributes'], False)

def GetStudentInfo(event, session, studentTable):
    studentname = event['request']['intent']['slots']['getName']['value']

    #get_item is our next boto3 function that returns the data from our table in a json format
    #You can include as many identifiers as you want
    #I just looked for the Key where our unique ID name is equal to the student we want to know about
    data = studentTable.get_item(Key={'name': studentname})

    #data will look like
    #data: {Item: { "name" : somename, "stars": somenumber}}
    #big note, most of these items will be stored as unicode, so sometimes you will have to typecast to get the right effect
    sentence = studentname + " has only " + str(data['Item']['stars']) + " gold stars"
    return response(sentence, session['attributes'], False)

def GiveStudentStar(event, session, studentTable):
    studentname = event['request']['intent']['slots']['giveName']['value']
    added_stars = event['request']['intent']['slots']['giveStar']['value']

    #here I get the information on the student I want to reward
    data = studentTable.get_item(Key={'name': studentname})
    #then I add the stored amount with the new amount
    #because we got the amount from the spoken user, it was stored in unicode so we typecast
    starscore = data['Item']['stars'] + int(added_stars)

    #this is our third function from boto3 which will update our item
    #similar to get_item, you need to give Key some attributes to search for
    #in this case we just use the name is it's unique for now
    #We use NoSQL to update the item, but we shoudln't need to worry about teaching them much of that
    # :val1 is an expression so it will be substituted in and update the value when we call it at the same line
    #I did not try to do it another way yet.

    studentTable.update_item(
        Key={'name': studentname},
        UpdateExpression='SET stars = :val1',
        ExpressionAttributeValues={
            ':val1': starscore
        }
        )
    #typecasted starscore since you can only glue strings to a string
    sentence = "The stars have been updated. " + studentname + " now has " + str(starscore) + " stars!"
    return response(sentence, session['attributes'], False)

def DeleteStudent(event, session, studentTable):
     studentname = event['request']['intent']['slots']['deleteName']['value']
     #here we are deleting the students
     #We need to provide it a Key with the uniqueID (and any other attributes you want to include)
     studentTable.delete_item( Key= {"name": studentname} )
     sentence = "Successfully removed " + studentname + " from our class"
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
