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
        
def convert2BDSP(message, labelIndex, arrayIndex, printOutput = True, label = None):
    
    calculator.loadKey()

    ##Make it exit only on a specific command
    if message.lower() == ":q":
        exit()

    eventID = 1

    output = {"wordDataArray": []}

    message = message.replace('\\n', '\n')
    messageArray = re.split('( |\n)', message)
    #messageArray = message.split(" ") #message split by spaces
    subTotal = [] #length of line, not to drastically excede 800, to be inserted into text
    subTotal.append(0.0)
    subTotalCounter = 0 #used for accessing each line as the loop goes on
    newMessage = [] #each individual new line, to be inserted into txt
    newMessage.append("")
    newMessageCounter = 0 #counter used for accessing current line

    numWords = len(messageArray)
    wordCount = 1
    for word in messageArray:
        if printOutput:
            print(word)

        if word != '\n':
            wordLength = calculator.calculate(word)

            if subTotal[subTotalCounter] + wordLength > 660:
                newMessage[newMessageCounter] = newMessage[newMessageCounter].replace("'", "’")
                newMessageCounter += 1
                newMessage.append("")
                subTotalCounter += 1
                subTotal.append(0.0)

            newMessage[newMessageCounter] += word

            subTotal[subTotalCounter] += wordLength
        else:
            newMessage[newMessageCounter] = newMessage[newMessageCounter].replace("'", "’")
            newMessageCounter += 1
            newMessage.append("")
            subTotalCounter += 1
            subTotal.append(0.0)

        wordCount += 1

    subTotal.clear()
    newMessageIterator = copy.deepcopy(newMessage)
    newMessage.clear()

    index = 1
    patternID = 7
    eventID = 1
    count = len(newMessageIterator)

    for line in newMessageIterator:
        line.strip()

        if index == count:
            patternID = 0
            eventID = 7

        wordData = {
            "patternID": patternID,
            "eventID": eventID,
            "tagIndex": -1,
            "tagValue": 0.0,
            "str": line,
            "strWidth": calculator.calculate(line)
        }

        if eventID == 1:
            eventID = 3
        elif eventID == 3:
            eventID = 1

        output['wordDataArray'].append(wordData)
        index += 1

    if label == None:
        return output
        ##rapidjson is basically a drag and drop json class thats 2x faster

    else:
        return addHeader(output, labelIndex, arrayIndex, label)

if (__name__ == "__main__"):
    main()