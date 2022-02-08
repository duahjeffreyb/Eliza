##############################################################################################################
#Jeffrey Duah 
#February 8th,  2022
#CMSC 416
#This program is meant to simulate the Rogerian psychotherapist, ELIZA, originially created by Joseph Wizenbaum
#ELIZA takes input from the user and poses questions in a similar fashion as a psychotherapist. This is mainly
#to be done uses word spotting using keywords to form questions to ask back to the user.
#Usage instructions:
    #Open terminal
    #type "python eliza.py" into terminal to being program execution
    #Answer questions that ELIZA prompts you with 
    #type "bye" to end program execution
#Example program execution:
    #[ELIZA] Hi! This is ELIZA, your Rogerian psychotherapist. What is your name?
    #[User] Jeffrey
    #[ELIZA] Hi Jeffrey, what can I help you with today?
    #[Jeffrey] I am feeling happy today
    #[ELIZA] Tell me more about how you are feeling happy today
    #[Jeffrey] I had a great breakfast
    #[ELIZA] you had a great breakfast?
    #[Jeffrey] Yes, pancakes, eggs, all of that
    #[ELIZA] Interesting, tell me more
    #[Jeffrey] ...
# This program was created using regular expressions to spot keywords in users input in order to pose questions
# based on those keywords. Once a keyword is spotted, the program randomly selects from a couple of sentences
# in order to ask a question and keep the conversation going. Most of the decision making is done by using
# conditional statements to check whether the keyword has been spotted or not. If no keyword is spotted, the 
# program will randomly choose from a couple of generic replies. The program also replaces certain pronouns 
# so that ELIZA's grammar sounds more human.  Program execution ends when user types in bye
# which will them display a message for billing after talking to ELIZA. The keywords a checked for in a descending
# order where the earlier the keyword is in the code, the more important it is to catch that keyword. Examples
# of this include snetences where you address ELIZA directly, as well as sentences where you say you are something
# Some special/unique cases include a special response to when you say you are happy, prompting for a specific time
# an event occured when saying someone, everyone, or always and special responses connected to keywords dealing with family. 
# ELIZA also keeps track of how many times she responds with a generic response in order to keep the conversation fresh. 
# After 5 generic responses, ELIZA will prompt user to change the subject. This counter is refreshed everytime
# the program encounters a keyword.
##############################################################################################################
import re
import random

famChoices = ["[ELIZA] How is your marriage going?\n", "[ELIZA] Tell me more about your family\n"]
noKeyword = 0
def response(line, name):
    global noKeyword, famChoices
    # Flip common pronouns
    line = re.sub(r'\s\bmy\b\s+', ' your ', line)
    line = re.sub(r'\bme\b', ' you ', line)


    # Searches for sentences where you address ELIZA
    # substitution to change any "you"'s to "I"'s in the case of "You have"
    check1 = re.search(r'((\w*\s)*)(eliza is)((\s\w*)+)', re.sub(r'\s*(Y|y)ou are\s', "eliza is ", line))
    if check1:
        noKeyword = 0
        num = random.randint(0,2)
        #Randomly choose output based on number
        if num == 0:
            return "[ELIZA] I am" + check1.group(5) + "?\n"
        elif num == 1:
            return "[ELIZA] Do you think you are" + check1.group(4) + "?\n"
        else:
            return "[ELIZA] Enough about me, tell me more about you.\n"


    # Searches for words describing oneself
    # Substitution to change phrase "I am" to "you are"
    check2 = re.search(r'\w*\b((y|Y)ou are)\b((\s\w+)*)', re.sub(r'\s*I am\s*', ' you are ', line))
    if check2:
        noKeyword = 0
        num = random.randint(0,2)
        # special case for happy
        if "you are happy" in check2.group() and num == 1:
            return "[ELIZA] A rare occurance among my patients. Any particular reason you're feeling happy?\n"
        #Randomly choose output based on number
        elif num == 0:
            return "[ELIZA] You are" + check2.group(3) + "?\n"
        elif num == 2:
            return "[ELIZA] Why do you think you are" + check2.group(3) + "?\n"
        else:
            return "[ELIZA] Tell me more about how you are" + check2.group(3) + "\n"


    # Searches for sentence where someone says something
    check3 = re.search(r'((\w*\s)*)(([a-zA-Z]+) said)(\s\w+)((\s\w+)*)', line)
    if check3:
        noKeyword = 0
        # If you say something
        if check3.group(4) == "I":
            # Prompt you user for what they said if they specifically say "I said something"
            if check3.group(5) == " something":
                return "What did you say?\n"
            else:
                return "[ELIZA] Why would you say" + check3.group(5) + check3.group(6) + "?\n"
        # Prompt you user for what person said if they specifically say "[name] said something"
        num = random.randint(0,1)
        if check3.group(5) == " something":
                return "What did " +  check3.group(4) + " say?\n"
        #Randomly choose output based on number 
        if num == 0:
            return "[ELIZA] Why do you think that " + check3.group(4) + " would say that" + check3.group(5) + check3.group(6) + "?\n"
        if num == 1:
            return "[ELIZA] How did what " + check3.group(3) + " make you feel?\n"

    # Searches for sentences where user says it is
    check4 = re.search(r'((\w*\s)*)((I|i)t is)((\s\w*)*)', line)
    if check4:
        noKeyword = 0
        num = random.randint(0,1)
        # if the phrase "it is" has more text after it, randomly choose an output
        if check4.group(5):
            if num == 0:
                return "[ELIZA] Why is it" + check4.group(5) + "?\n"
            if num == 1:
                return "[ELIZA] How does it being" + check4.group(5) + " make you feel?\n"
        else:
            # generic response if there is no text after "it is"
            return "[ELIZA] Is it?\n"

    #Searches for sentences that start with I have/I had
    check8 = re.search(r'((\w*\s)*)(I (have|had)((\s\w+)*))', line)
    if check8:
        noKeyword = 0
        num = random.randint(0,1)
        # select random case if verb is "had"
        if check8.group(4) == "had":
            if num == 0:
                return "[ELIZA] You had" + check8.group(5) + "?\n"
            elif num == 1:
                return "[ELIZA] Why did you have" + check8.group(5) + "?\n"

        # select random case if verb is "have"
        if check8.group(4) == "have":
            if "think" in check8.group(2):
                return "[ELIZA] Why do you think you have" + check8.group(5) + "?\n"
            if num == 0:
                return "[ELIZA] You have" + check8.group(5) + "?\n"
            elif num == 1:
                return "[ELIZA] Why do you have" + check8.group(5) + "?\n"
    
    # searches for sentences that has "I [verb]"
    # subsitution which replace I with you
    check5 = re.search(r'((\w*\s)*)(you)((\s\w+)+)', re.sub(r'\bI\b', 'you' ,line))
    if check5:
        noKeyword = 0
        # random input based on number
        num = random.randint(0,1)
        if num == 0:
            return "[ELIZA] " + check5.group(3) + check5.group(4) + "?\n"
        if num == 1:
            return "[ELIZA] " + check5.group(3) + check5.group(4) + "? How does that make you feel?\n"

    #Searches for family keywords in a sentence
    check6 = re.search(r'((\w*\s)*)(father|mom|dad|mother|sister|brother|wife|husband|kids|family|children)((\s\w+)*)', line)
    if check6:
        noKeyword = 0
        # Get family member being taked about
        familyMember = check6.group(3)
        num = random.randint(0,3)
        # Special one time questions for married folks
        if familyMember == 'wife' or familyMember == 'husband' and num == 2 and famChoices[0] != None:
            string = famChoices[0]
            famChoices[0] = None
            return string
        # Special one time broad question about family
        elif num == 1 and famChoices[1] != None:
            string = famChoices[1]
            famChoices[1] = None
            return string
        else:
            return "[ELIZA] How's your relationship with your " + check6.group(3) + "?\n" 
    
    # Searches for sentences where you describes something you love or hate
    check7 = re.search(r'((\w*\s)*)(\b(lov|hat|lik)(ed|e)\b)((\s\w+)*)', line)
    if check7:
        noKeyword = 0
        # special cases for past tense forms
        if check7.group(3) == "loved":
            return "[ELIZA] What changed with your love for" + check7.group(6) + "?\n"
        if check7.group(3) == "hated":
            return "[ELIZA] What changed with your hate for" +  check7.group(6) + "?\n"
        if check7.group(3) == "liked":
            return "[ELIZA] What changed with you like for" +  check7.group(6) + "?\n"
        # generic case of present tense forms
        return "[ELIZA] Why do you " + check7.group(3) + check7.group(6) + "?\n"


    
    # Searches for keywords "everybody", "never", or "always"
    check9 = re.search(r'((\w*\s)*)((E|e)verybody|(E|e)veryone|always)((\s\w*)+)', line)
    if check9:
        noKeyword = 0
        # special case for when sentence contains "everyone" or "everybody"
        if(check9.group(3).lower() == "everybody" or check9.group(3).lower() == "everyone"):
            return "[ELIZA] Can you think of a specific time where " + check9.group(3) + check9.group(6) + "?" + "\n"
        else:
            # When sentence contains "always"
            return "[ELIZA] Can you think of a specific time where you always" + check9.group(6) + "?" + "\n"

    
    # Phases randomly selected if no keyword is found
    num = random.randint(0,8)
    #Change topic if keywords are not being caught
    if noKeyword == 5:
        noKeyword = 0
        num = random.randint(0,1)
        if num == 0:
            return "[ELIZA] Ok, " + name + ", let's switch gears a bit. Anything else you want to talk about?\n"
        if num == 1:
            return "[ELIZA] Come on " + name + ", you gotta work with me here....Let's try talking about something else.\n"
    else:
        if num == 0:
            noKeyword += 1
            return "[ELIZA] Please elaborate...\n"
        elif num == 1:
            noKeyword += 1
            return "[ELIZA] Interesting, tell me more\n"
        elif num == 2:
            noKeyword += 1
            return "[ELIZA] Writing that down....please, can you explain further?\n"
        elif num == 3:
            noKeyword += 1
            return "[ELIZA] Let's expand on that\n"
        elif num==4:
            noKeyword += 1
            return "[ELIZA] Let's go into further details on that\n"
        elif num == 5:
            return "[ELIZA] I didn't quite get that, could you reiterate it?\n"
        else:
            noKeyword += 1
            return "[ELIZA] " + line + "?\n"

# beginning prompts
name = input('[ELIZA] Hi! This is ELIZA, your Rogerian psychotherapist. What is your name?\n[user] ')
line = input('[ELIZA] Hi ' + name + ', what can I help you with today?\n' + "[" + name + "] ")
# while loop for asking and responding
while(line != "bye"):
    line = input(response(line, name) + "[" + name + "] ")
# exit statement when goodbye is typed
print("Goodbye " + name + "! you will receive your $" + str(round(random.uniform(10000,1000000), 2)) + " bill in the mail.\n It's due in 2 weeks! Please pay or I, ELIZA, will find you....Have a good day! :)")
