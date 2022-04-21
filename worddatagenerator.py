import re
from tkinter import N
import rapidjson
from generateHeader import addHeader
import stringLengthCalculator as calculator
import copy
from PyQt5.QtWidgets import QMessageBox

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
    message = message.rstrip()
    messageArray = re.split('( |\n)', message)
    #messageArray = message.split(" ") #message split by spaces
    subTotal = [] #length of line, not to drastically excede 800, to be inserted into text
    subTotal.append(0.0)
    subTotalCounter = 0 #used for accessing each line as the loop goes on
    newMessage = [] #each individual new line, to be inserted into txt
    newMessage.append("")
    newMessageCounter = 0 #counter used for accessing current line
    eventIDList = []
    eventIDList.append(0)

    numWords = len(messageArray)
    wordCount = 1
    for word in messageArray:
        if printOutput:
            print(word)

        words = []

        if word != '\n' and '\n' not in word and '\\r' not in word and '\\f' not in word and '\\w' not in word and "<name>" not in word:
            wordLength = calculator.calculate(word)

            if subTotal[subTotalCounter] + wordLength > 660:
                newMessage[newMessageCounter] = newMessage[newMessageCounter].replace("'", "’")
                
                #eventID 4 cannot follow 3, so if the previous eventID was 3, force this one to be 1 instead.

                if newMessageCounter > 0 and eventIDList[newMessageCounter-1] == 3:
                    eventIDList[newMessageCounter] = 1
                else:
                    eventIDList[newMessageCounter] = 4
                newMessageCounter += 1
                eventIDList.append(0)
                newMessage.append("")
                subTotalCounter += 1
                subTotal.append(0.0)

                # #we might have a format specifier between two words all lumped together, throwing off the calculated
                # #total, so check for that here. But even if it does go over the limit, each specifier results in the
                # #end of a line regardless.

                # if '\\r' in word:
                #     words = re.split('\\\\r', word)
                #     eventIDList[newMessageCounter] = 3
                #     eventIDList.append(0)

                # elif '\\f' in word:
                #     words = re.split('\\\\f', word)
                #     eventIDList[newMessageCounter] = 4
                #     eventIDList.append(0)

                # elif '\\w' in word:
                #     words = re.split('\\\\w', word)
                #     eventIDList[newMessageCounter] = 2
                #     eventIDList.append(0)

                # if len(words) > 0:
                #     word = words[0]
                #     wordLength = calculator.calculate(words)

                #     if subTotal[subTotalCounter] + wordLength > 660:
                #         newMessage[newMessageCounter] = newMessage[newMessageCounter].replace("'", "’")
                #         newMessageCounter += 1
                #         newMessage.append("")
                #         subTotalCounter += 1
                #         subTotal.append(0.0)

                #     messageArray.insert(wordCount, words[1])

            newMessage[newMessageCounter] += word

            subTotal[subTotalCounter] += wordLength
        else:
            event = []
            if word == '\n':
                eventIDList[newMessageCounter] = 3

            elif '\n' in word:
                event = re.split('\n', word)
                eventIDList[newMessageCounter] = 3

            if '\\r' in word:
                event = re.split('\\\\r', word)
                print(event)
                eventIDList[newMessageCounter] = 3
            
            if '\\w' in word:
                event = re.split('\\\\w', word)
                eventIDList[newMessageCounter] = 2

            if '\\f' in word:
                event = re.split('\\\\f', word)
                #eventID 4 cannot follow 3, so if the previous eventID was 3, force this one to be 1 instead.

                if newMessageCounter > 0 and eventIDList[newMessageCounter-1] == 3:
                    eventIDList[newMessageCounter] = 1
                else:
                    eventIDList[newMessageCounter] = 4

            if len(event) > 0:
                #the first side of the split gets added to the current newMessageCounter just as if it were read off
                #the line. If it wraps to a new line, that's fine.

                wordLength = calculator.calculate(event[0])

                if subTotal[subTotalCounter] + wordLength > 660:
                    newMessage[newMessageCounter] = newMessage[newMessageCounter].replace("'", "’")
                    newMessageCounter += 1
                    newMessage.append("")

                    #did this happen on a \r boundary? Need to make sure the 3 we just assigned is actually a 4,
                    #and move the 3 to the next eventID.

                    if '\\r' in word:
                        eventIDList[newMessageCounter-1] = 4
                        eventIDList.append(3)
                    #else just append 4 as usual.
                    else:
                        eventIDList.append(4) #\f formatter needed here.
                    subTotalCounter += 1
                    subTotal.append(0.0)

                newMessage[newMessageCounter] += event[0]
                subTotal[subTotalCounter] += wordLength

                #The second side of the split always starts on an incremented newMessageCounter, so we need to increment
                #both the newMessageCounter and subTotalCounter here.

                newMessage[newMessageCounter] = newMessage[newMessageCounter].replace("'", "’")
                newMessageCounter += 1
                newMessage.append("")
                eventIDList.append(0)
                subTotalCounter += 1
                subTotal.append(0.0)

                newMessage[newMessageCounter] += event[1]
                subTotal[subTotalCounter] += wordLength

            # newMessage[newMessageCounter] = newMessage[newMessageCounter].replace("'", "’")
            # newMessageCounter += 1

            if len(event) == 0:
                newMessage.append("")
                newMessageCounter += 1
                eventIDList.append(0)

            subTotalCounter += 1
            subTotal.append(0.0)

            if "<name>" in word:
                #separate what's on either side of "<name>"
                insertString = re.split('(<name>)', word)

                #insertString will have at most 3 entries, and seems to always have an empty string "" at index 0
                #if <name> isn't preceded by anything in the entered message. It's trickier than I care to deal with
                #if the user does something like hello<name>!, so I'm just going to reject the message and force that
                #space before <name>.

                if insertString[0] != "":
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Nothing can precede <name> unless it's at the start of a message.")
                    msg.exec_()
                    raise Exception ("Nothing can precede <name> unless it is the beginning of a message.")

                print(insertString)
                eventIDList[newMessageCounter] = 5
                newMessage[newMessageCounter] += insertString[1]
                newMessageCounter += 1
                newMessage.append("")
                if insertString[2] != "":
                    newMessage[newMessageCounter] += insertString[2]
                    newMessageCounter += 1
                    newMessage.append("")

        wordCount += 1

    newMessageIterator = copy.deepcopy(newMessage)
    newMessage.clear()

    index = 1
    patternID = 7
    eventID = 1
    eventIDListIndex = 0
    count = len(newMessageIterator)
    print(len(eventIDList))

    #The first entry in worddata always has eventID of 1, so force that here.
    #It's easier to do it this way than to provide logic above to only use 1 in the first index.

    eventIDList[0] = 1
    for line in newMessageIterator:
        line.strip()

        eventID = eventIDList[eventIDListIndex]
        tagValue = 0.0

        if index + 1 == count:
            precedingFinal = True

        if index == count:
            patternID = 0
            eventID = 7

        if eventID == 2:
            tagValue = 0.19999999999

        # eventID 1 should not follow each other, so treat the preceding eventID 1 as the "end" of the previous
        # textbox and force it to be eventID 3.

        if eventID == 1 and eventIDListIndex < len(eventIDList) and eventIDList[eventIDListIndex+1] == 1:
            eventID = 3

        if eventID == 4 and eventIDListIndex > 0 and eventIDList[eventIDListIndex-1] == 3:
            eventID = 1

        wordData = {
            "patternID": patternID,
            "eventID": eventID,
            "tagIndex": -1,
            "tagValue": tagValue,
            "str": line,
            "strWidth": calculator.calculate(line)
        }

        if line == "<name>":
            wordData["patternID"] = 5
            wordData["eventID"] = 0
            wordData["tagIndex"] = 0
            wordData["str"] = ""
            wordData["strWidth"] = -1.0

        eventIDListIndex += 1
        output['wordDataArray'].append(wordData)
        index += 1

    if label == None:
        return output
        ##rapidjson is basically a drag and drop json class thats 2x faster

    else:
        return addHeader(output, labelIndex, arrayIndex, label)

if (__name__ == "__main__"):
    main()