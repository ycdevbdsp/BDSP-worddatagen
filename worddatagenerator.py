import re
import rapidjson
from generateHeader import addHeader
import stringLengthCalculator as calculator
import copy

def main():
    
    building = True
    
    outfile = 'wordData.json'
    file = open(outfile, "w+", encoding="utf8")
    
    while building:
        message = input("Input your message: ")

        file.write(convert2BDSP(message))
        print("Message Saved to wordData.json")
        
def convert2BDSP(message, printOutput = True, label = None):
    
    calculator.loadKey()

    ##Make it exit only on a specific command
    if message.lower() == ":q":
        exit()

    eventID = 1

    output = {"wordDataArray": []}

    if message[0] == '#':
        message = message.replace("#", "", 1)
        eventID = 7
    
    message = message.replace('\\n', '\n')
    messageArray = re.split('( |\n)', message)
    #messageArray = message.split(" ") #message split by spaces
    subTotal = [] #length of line, not to drastically excede 800, to be inserted into text
    subTotal.append(0.0)
    subTotalCounter = 0 #used for accessing each line as the loop goes on
    newMessage = [] #each individual new line, to be inserted into txt
    newMessage.append("")
    newMessageCounter = 0 #counter used for accessing current line
    
    words = len(messageArray)
    index = 0
    
    if printOutput:
        print("Counted", words, "Words in your message")
        
    for word in messageArray:

        if printOutput:
            print(word)
            
        if word == ' ':
            index += 1
            continue
        elif word != '\n':
            wordLength = calculator.calculate(word)

        if subTotal[subTotalCounter] + wordLength > 600 or index == words or word == '\n':
            newMessage[0] = newMessage[0].replace("'", "’")

            wordData = {
                "patternID": 7,
                "eventID": eventID,
                "tagIndex": -1,
                "tagValue": 0.0,
                "str": newMessage[0],
                "strWidth": subTotal[0]
            }
            
            if eventID == 1:
                eventID = 4
                
            output['wordDataArray'].append(wordData)

            subTotal.clear()
            subTotal.append(0.0)
            newMessage.clear()
            newMessage.append("")

        if word == '\n':
            eventID = 1
            index += 1
            continue

        newMessage[newMessageCounter] += word + " "
        subTotal[subTotalCounter] += wordLength
        index += 1

    if index == words:
        if len(newMessage[0]) > 0:
            newMessage[0] = newMessage[0].replace("'", "’")
            wordData = {
                "patternID": 7,
                "eventID": 7,
                "tagIndex": -1,
                "tagValue": 0.0,
                "str": newMessage[0],
                "strWidth": subTotal[0]
            }
            output['wordDataArray'].append(wordData)

        output['wordDataArray'][len(output['wordDataArray']) - 1]['eventID'] = 7
        
        if label == None:
            return rapidjson.dumps(output, indent=4)
            ##rapidjson is basically a drag and drop json class thats 2x faster
            
        else:
            return addHeader(output, label)

if (__name__ == "__main__"):
    main()