import bs4
from dataBase import *
from classes import *

#covert string to time
def convertTotTime(string):
    months={'januari':'01','februari':'02','mars':'03', 'april':'04','maj':'05','juni':'06','juli':'07','augusti':'08','september':'09','oktober':'10','november':'11','december':'12'}
    string=string.strip('den ')
    list=string.split(' ')
    day=list[0]
    month=months[list[1]]
    year=list[2]
    hour=list[4][:2]
    min=list[4][-2:]
    return TimeSent(year,month,day, hour, min)
#-------------------------------------------
#Read an html conversationFile
def readConversation(filename):
    print("\rInitializing conversation...")
    soup=bs4.BeautifulSoup(open(filename), 'html.parser')
    thread=soup.body
    title=str(thread.div.h3.text)
    conversation=None
    conversation=Thread(title)
    print("Adding users to conversation...")
    body=thread.div.contents
    participants=str(body[1]).replace('Participants: ', "")
    list=participants.split(", ")
    conversation.addUser('Gustaf Lidfeldt')

    for name in list:
        conversation.addUser(name)

    i=2
    print("\rAdding messages to conversation...")
    while i<len(body):
        try:
            message=body[i].div.contents
            testname = str(message[0].text)
            time = convertTotTime(str(message[1].text.encode('utf-8')))
            textmessage=str(body[i+1].text.encode('utf-8'))
            conversation.addMessages(testname, time.string, textmessage)
            i+=2
        except:
            pass
            i+=1
    return conversation
#-------------------------------------------

def main():
    db = Database('template1')
    db.clearTables()
    db.createTables()
    friends={}
    index=1
    messIndex=0
    amountOfConversations=3
    for i in range(1, amountOfConversations):
        print("File: "+str(i)+".html")
        filename=str(i)+".html"
        conversation=None
        conversation=readConversation(filename)
        id=i
        db.insert_entry('conversation',['id','name'], [id,conversation.name])
        for name in conversation.participants:
            if name not in friends:
                db.insert_entry('friends', ['id','name'],[str(index),name])
                friends[name]=str(index)
                index+=1
            db.insert_entry('participation', ['userid','conversationid',], [friends[name], str(i)])
        for name in conversation.participants:
            list=conversation.messages[name]
            for message in list:
                db.insert_entry('message', ['id','convID','userID','time','message'],[str(messIndex),str(i),friends[name], message.timeSent, message.body])
                messIndex+=1
main()