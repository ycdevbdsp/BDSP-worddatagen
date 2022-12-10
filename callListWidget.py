import sys
import re
import json
import os
import uuid
import worddatagenerator as worddata
import stringLengthCalculator as calculator
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QTableWidgetItem, QColorDialog
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import QModelIndex
from dialogEditor import *
class MyForm(QDialog):    
    OpenFile = {}
    MessageList = {}
    MessageListIndices = {}
    Speakers = {}
    Names = {}
    FontSize = 54
    FontSizeAmp = 0.63
    path = "input"
    nameplatesPath = "input\MsgWindowData.json"
    speakerNamesPath = "input\english_dlp_speakers_name.json"
    outputs = "output"
    NextLabelIndex = 0
    NextArrayIndex = 0
    SelectedMessageIndex = -1
    SelectedTextFile = ""
    useKakugo = False


    OpenColorTag = {
        "patternID": 2,
        "eventID": 0,
        "tagIndex": -1,
        "tagValue": 0.0,
        "str": "<color=#FFFFFFFF>",
        "strWidth": -1.0
    }

    CloseColorTag = {
        "patternID": 2,
        "eventID": 0,
        "tagIndex": -1,
        "tagValue": 0.0,
        "str": "</color>",
        "strWidth": -1.0
    }

    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.textEditNewMsg.textChanged.connect(self.dispNewMsgContents)
        self.ui.listFileNames.currentItemChanged.connect(self.popMessages)
        #self.ui.listMsgNames.currentItemChanged.connect(self.dispMsgContents)
        self.ui.listMsgNames.itemSelectionChanged.connect(self.dispMsgContents)
        self.ui.btnAddMsg.clicked.connect(self.addMsg)
        self.ui.btnReplaceMsg.clicked.connect(self.replaceMsg)
        self.ui.btnSanitize.clicked.connect(self.sanitize)
        self.ui.btnSave.clicked.connect(self.saveChanges)
        self.ui.btnSetAllTextColor.clicked.connect(self.setAllTextColor)
        self.ui.textEditNewMsg.setFont(QFont('FOT-UDKakugoC80 Pro DB', 16))
        self.ui.speakerCombo.currentTextChanged.connect(self.filterMsgsBySpeaker)
        self.ui.msgTableFilter.textChanged.connect(self.filterMsgTable)
        self.ui.msgTable.cellClicked.connect(self.selectMsgFromMessageList)

        # if self.ui.textEditNewMsg.font().family() == 'FOT-UDKakugoC80 Pro DB':
        #     self.ui.textEditNewMsg.setFontPointSize(17)
        list = self.ui.listMsgNames
        files = self.ui.listFileNames
        
        
        fileList = os.listdir(self.path)
        
        for f in fileList:
            if f != "MsgWindowData.json" and f != "english_dlp_speakers_name.json":
                files.addItem(f)
        
        if os.path.exists(self.nameplatesPath):

            npFile = open(self.nameplatesPath, 'r', encoding="utf-8")
            speakerNameFile = open(self.speakerNamesPath, 'r', encoding="utf-8")
            np = json.load(npFile)
            spk = json.load(speakerNameFile)
            
            self.Speakers = {}  #english_dlp_speakers_name.json
            for s in spk["labelDataArray"]:
                if s["wordDataArray"][0]["str"] != "":
                    self.Speakers[s["labelName"]] = s["wordDataArray"][0]["str"]
                    print(self.Speakers[s["labelName"]])

            self.Names = {}     #MsgWindowData.json
            for n in np["SpeakerNameData"]:
                if "SPEAKERS_NAME" not in n["talk_label"]:
                    self.Names[n["label"]] = n["talk_label"]
                    #This is a name that is referenced by variables, like the rival's name so add it to the Speakers list if it doesn't already exist.
                    if n["talk_label"] not in self.Speakers:
                        self.Speakers[n["talk_label"]] = n["talk_label"]
                else:
                    self.Names[n["label"]] = self.Speakers[n["talk_label"]]

            #Fill the combobox with the different speakers, but first add the "all" option.
            self.ui.speakerCombo.addItem("All")
            for s in self.Speakers:
                self.ui.speakerCombo.addItem(self.Speakers[s])
            
        files.setCurrentItem(files.item(0))
        self.show()
    
    def filterMsgTable(self):
        filterText = self.ui.msgTableFilter.text().lower()

        if len(filterText) < 2 and filterText != "":
            return

        for row in range(self.ui.msgTable.rowCount()):
            _row = self.ui.msgTable.item(row, 1)
            if _row is not None and filterText in _row.text().lower():
                self.ui.msgTable.showRow(row)
            else:
                self.ui.msgTable.hideRow(row)


    def filterMsgsBySpeaker(self):
        speaker = self.ui.speakerCombo.currentText()

        i = 0
        while i < self.ui.listMsgNames.count():
            msg = self.ui.listMsgNames.item(i).text()

            if speaker != "All" and (msg not in self.Names or self.Names[msg] != speaker):
                self.ui.listMsgNames.item(i).setHidden(True)
            else:
                self.ui.listMsgNames.item(i).setHidden(False)
            i += 1

    def sanitize(self):
        index = 0
        calculator.loadKey()
        for m in self.MessageList:
            wd = self.OpenFile['labelDataArray'][index]['wordDataArray']
            td = self.OpenFile['labelDataArray'][index]['tagDataArray']
            newText = ""
            skip = False

            #worddata empty? skip it

            if len(wd) == 0:
                index += 1
                continue

            #tagdata of len > 0 means we have variables. just skip this one and move on to the next.
            if len(td) > 0:
                index += 1
                continue
            
            #preliminarily search for any pattern IDs that aren't 0 or 7. If there is one, then don't
            #try to sanitize it.

            for preW in wd:
                if preW['patternID'] not in [0, 7]:
                    skip = True
                    break
            
            if skip == True:
                index += 1
                continue

            # get each string of text in this worddata
            wdIndex = 0
            for w in wd: 
                str = w['str']
                eventID = w['eventID']
                newText += str.strip()

                # don't append any formatters to single entry worddatas or to the final entry,
                # unless the first entry has eventID 3.
                
                if eventID != 3 and (len(wd) == 1 or wdIndex == len(wd) - 1):
                    continue

                #if the strwidth of str plus the width of the first word of the next str is greater than 660,
                #and the eventID of this wd is 1 or 4, then we do not need to append an explicit \f. Otherwise
                #we do. If the eventID in this case is 3, then we still need to preserve that with the \r formatter.

                if wdIndex + 1 < len(wd):
                    strWidth = w['strWidth']
                    nextWord = re.split('( |\n)', wd[wdIndex+1]['str'].strip())[0]
                    nextWordWidth = calculator.calculate(nextWord)

                    if strWidth + nextWordWidth > 660:
                        if eventID == 3:
                            newText += '\\r'

                        elif newText.endswith(' ') == False:
                            newText += ' '
                        wdIndex += 1
                        continue                       
                
                if eventID == 3:
                    newText += '\\r'

                else:
                    newText += '\\f'

                wdIndex += 1

            # before we sanitize, fix cases like 'strong...\f...\ranyway' where more than one formatter
            # is in a "word"

            message = newText.rstrip()
            messageArray = re.split('( |\n)', message)
            finalText = ""
            for m in messageArray:
                if m.count('\\r') + m.count('\\f') > 1:
                    m = m.replace('\\r', '\\r ')
                    m = m.replace('\\f', '\\f ')

                finalText += m

            # Run the newText through the tool, then replace the existing worddata
            # with the resulting worddad

            newMsg = worddata.convert2BDSP(finalText, 0, 0, False, "")
            self.OpenFile['labelDataArray'][index]['wordDataArray'] = newMsg['wordDataArray']
            index += 1

        print('Sanitized! Please Save immediately.')

    def setAllTextColor(self):
        color = QColorDialog.getColor()

        if color.isValid():
            print(color.name())

            msg = QMessageBox()
            ret = msg.question(self, '',
               f"You are about to overwrite the text color of all spoken dialog in {self.SelectedTextFile}. Do you wish to continue?",
               msg.Yes | msg.No)

            if (ret == msg.No):
                return

            self.OpenColorTag['str'] = f"<color={color.name()}>"
            for w in self.OpenFile['labelDataArray']:
                if w['styleInfo']['colorIndex'] == 10:
                    continue
                
                newWordData = []
                preserveCount = 0
                for wd in w['wordDataArray']:                    
                    
                    if preserveCount > 0:
                        newWordData.append(wd)
                        preserveCount -= 1
                        continue

                    if "<color=" in wd['str']:
                        #this is a preexisting color tag that we should preserve completely.
                        #We assume that color tags only contain one entry between open and close.

                        newWordData.append(wd)
                        preserveCount = 2
                        continue

                    newWordData.append(self.OpenColorTag)
                    newWordData.append(wd)
                    newWordData.append(self.CloseColorTag)

                w['wordDataArray'] = newWordData
            return
        return

    def replaceMsg(self):
        label = self.ui.listMsgNames.currentItem().text()
        print(self.SelectedMessageIndex)
        if self.SelectedMessageIndex == -1:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Select a message to replace.")
            msg.exec_()
            return

        try:
            newMsg = worddata.convert2BDSP(self.ui.textEditNewMsg.toPlainText(), 0, 0, False, "")
            print("Selected Message Index: " + str(self.SelectedMessageIndex))
            self.OpenFile['labelDataArray'][self.MessageListIndices[label]]['wordDataArray'] = newMsg['wordDataArray']
            print(self.OpenFile['labelDataArray'][self.MessageListIndices[label]])
            self.dispNewMsgContents()
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(str(e))
            msg.exec_()
        return
    
    def addMsg(self):
        msgLabel = "1-msg_" + self.ui.msgLabel.text()
        
        newMsg = worddata.convert2BDSP(self.ui.textEditNewMsg.toPlainText(), self.NextLabelIndex, self.NextArrayIndex, False, msgLabel)
        
        self.NextLabelIndex += 1
        self.NextArrayIndex += 1
        
        print (newMsg)
        self.OpenFile['labelDataArray'].append(newMsg)
        return
        
    def saveChanges(self):
        try:
            msgFile = self.ui.listFileNames.currentItem().text()

            if os.path.exists(self.outputs) == False:
                os.makedirs(self.outputs)

            with open(self.outputs+"\\new_" + msgFile, 'w+', encoding="utf-8") as outfile:
                json.dump(self.OpenFile, outfile)
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("An error occurred trying to save your changes:\n" + str(e) + "\nMake sure the 'output' folder exists in the same " +
               "directory as this executable, and then try again.")
            msg.exec_()
    
    
    def popMessages(self):
        _translate = QtCore.QCoreApplication.translate

        #make sure an item is selected
        msgFile = self.ui.listFileNames.currentItem().text()
        self.SelectedTextFile = msgFile
        list = self.ui.listMsgNames
        msgTable = self.ui.msgTable
        list.clear()
        self.MessageList = {}
        self.NextLabelIndex = 0
        self.NextArrayIndex = 0
        self.ui.msgTable.setRowCount(0)
        self.ui.msgTableFilter.setText("")

        with open(self.path+"\\"+msgFile, encoding="utf-8") as msgs:
            self.OpenFile = json.load(msgs)
            FileName = self.OpenFile['m_Name']
            trueIndex = 0

            for Msg in self.OpenFile['labelDataArray']:
                labelIndex = Msg['labelIndex']
                arrayIndex = Msg['arrayIndex']
                labelName = Msg['labelName']
                
                if labelIndex >= self.NextLabelIndex:
                    self.NextLabelIndex = labelIndex + 1
                if arrayIndex >= self.NextArrayIndex:
                    self.NextArrayIndex = arrayIndex + 1
                    
                if labelName == "":
                    labelName = str(trueIndex) + "-unused"
                    
                self.MessageList[labelName] = Msg
                self.MessageListIndices[labelName] = trueIndex

                dialog = [{}]
                messageRow = ""
                delimiter = ''
                for WordData in Msg['wordDataArray']:
                    dialog.append(WordData)
                    messageRow += (delimiter + str(WordData['str']))

                    if len(messageRow) > 0 and messageRow[len(messageRow)-1] != ' ':
                        delimiter = ' '
                    else:
                        delimiter = ''

                #sprint(labelName)
                    self.ui.msgTable.setRowCount(trueIndex+1)
                    item = QTableWidgetItem(labelName)
                    self.ui.msgTable.setItem(trueIndex, 0, item)
                    item = QTableWidgetItem(messageRow)
                    self.ui.msgTable.setItem(trueIndex, 1, item)
                list.addItem(labelName)
                trueIndex += 1
            
        
    def dispNewMsgContents(self):
        self.ui.msgContents.setFont(QFont('FOT-UDKakugoC80 Pro DB', 16))

        # if self.ui.msgContents.font().family() == 'FOT-UDKakugoC80 Pro DB':
        #     self.ui.msgContents.setFontPointSize(17)
        newMsg = worddata.convert2BDSP(self.ui.textEditNewMsg.toPlainText(), 0, 0, False, "")
        msg = ""
        for words in newMsg['wordDataArray']:
            if words['patternID'] == 5:
                msg += "<name>" + '\n'
            else:
                msg += words['str'] + '\n'
        self.ui.msgContents.setText(msg)
        
    def selectMsgFromMessageList(self):
        index = self.ui.msgTable.currentRow()
        print(f"table index: {index}")
        self.ui.listMsgNames.setCurrentRow(index)

    def dispMsgContents(self):
        if len(self.ui.listMsgNames.selectedItems()) == 0:
            return
        self.SelectedMessageIndex = self.ui.listMsgNames.currentIndex().row()
        tLabel = self.ui.listMsgNames.currentItem().text()
        print(self.SelectedMessageIndex)
        print("dispMsgContents")
        msg = ""
        
        for words in self.MessageList[tLabel]['wordDataArray']:
            if words['patternID'] == 5:
                msg += "<name>" + '\n'
            else:
                msg += words['str'] + '\n'
            
        self.ui.msgContents.setFont(QFont('FOT-UDKakugoC80 Pro DB', 16))
        # if self.ui.msgContents.font().family() == 'FOT-UDKakugoC80 Pro DB':
        #     self.ui.msgContents.setFontPointSize(17)
        self.ui.msgContents.setText(msg)

if __name__=="__main__":
    app = QApplication(sys.argv)
    w = MyForm()
    w.show()
    sys.exit(app.exec_())