# General things about Attributes
Alexa stores variables that can be used 'globally' under something called `event['session']['attributes']['variable']`
 `event`: is a built in word in Alexa that can be generalized to mean "the current running program"
 `session`: is one step into event that stores all the information that will be made by our running program
 `attributes`: is one step into session that will hold the variable names and its data
 `variable`: Unlike the others, you can the name of variable to anything you want. It will create an object that will store any data given into it.
 So, if we have `event['session']['attributes']['favoritefood']` then just created a variable called `favoritefood` inside of `attributes` which is inside of `session` which will be inside of `event`!
 Which will look something like this in Alexa:
```
event{
  "session":{
    "attributes":{
      "favoritefood": {}
    },
  },
}
```
Notice there is a pair of braces, `{}`, right next to `favoritefood`.
All it means is that we created the variable but it does not hold any data.
To fill it with data, we just need to include `=` to the right of `event['session']['attributes']['favoritefood']`.
          `event['session']['attributes']['favoritefood'] = taco`
Now our event list will look something like this:
```
event{
  "session":{
    "attributes":{
      "favoritefood": "taco"
    },
  },
}
```
Now this will only work until after we a new response a made.
