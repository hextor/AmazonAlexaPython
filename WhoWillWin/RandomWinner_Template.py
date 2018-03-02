def Winner(event, session):
    yesOrNo = ["yes", "no"]
    randomNumber = random.randint(0,1)
    choice = yesOrNo[randomNumber]

    if choice == "yes":
        sentence = choice + " " + FIRST_ + " is better than " + SECOND_
    else:
        sentence = choice + " " + FIRST_ + " is not better than " + SECOND_

    return response(sentence, session['attributes'], False)
