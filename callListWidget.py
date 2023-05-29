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
from adventureNoteEditor import *

class AdventureNotesEditorForm(QDialog):

    AdvNotesPath = "input\AdventureNoteData.json"
    AdvNotesLabelsPath = "input\english_dlp_adventure_note.json"
    AdvNotesContents = {}
    AdvNotesLabelsContents = {}
    AdvNoteDataIndices = {}
    AdvNotesLabelsIndices = {}
    AdvNotesTitlePageCounts = {}
    AdventureNoteDataOpenFile = {}
    DLPAdventureNoteOpenFile = {}
    NextLabelIndex = 0
    NextArrayIndex = 0
    SelectedPageIndex = -1
    outputs = "output"

    def __init__(self):
        super().__init__()
        self.ui = Ui_AdventureNotesEditor()
        self.ui.setupUi(self)
        self.ui.listAdventureNotePages.itemSelectionChanged.connect (self.adventureNotesPageChanged)
        self.ui.textEditPageTitle.setFont(QFont('FOT-UDKakugoC80 Pro DB', 16))
        self.ui.textEditTextLabel.setFont(QFont('FOT-UDKakugoC80 Pro DB', 16))
        self.ui.textEditTextLabelPatch.setFont(QFont('FOT-UDKakugoC80 Pro DB', 16))
        self.ui.btnAddPage.clicked.connect(self.btnAddPageClicked)
        self.ui.btnReplacePage.clicked.connect(self.btnReplacePageClicked)
        self.ui.btnSavePage.clicked.connect(self.btnSavePageClicked)

        pages = self.ui.listAdventureNotePages
        
        with open(self.AdvNotesPath, 'r', encoding='utf-8') as file:
            advNotesPathFile = file.read()
            self.AdventureNoteDataOpenFile = json.loads(advNotesPathFile)

        with open(self.AdvNotesLabelsPath, 'r', encoding='utf-8') as file:
            advNotesLabelsPathFile = file.read ()
            self.DLPAdventureNoteOpenFile = json.loads(advNotesLabelsPathFile)

        trueIndex = 0
        for label in  self.DLPAdventureNoteOpenFile['labelDataArray']:
            self.AdvNotesLabelsContents[label['labelName']] = label['wordDataArray']
            self.AdvNotesLabelsIndices[label['labelName']] = trueIndex
            trueIndex += 1

            if label['labelIndex'] > self.NextLabelIndex:
                self.NextLabelIndex = label['labelIndex'] + 1

            if label['arrayIndex'] > self.NextArrayIndex:
                self.NextArrayIndex = label['arrayIndex'] + 1
            
        trueIndex = 0
        for note in self.AdventureNoteDataOpenFile['Data']:
            if (note['TitleLabel'] in self.AdvNotesTitlePageCounts):
                self.AdvNotesTitlePageCounts[note['TitleLabel']] += 1
            else:
                self.AdvNotesTitlePageCounts[note['TitleLabel']] = 1
            self.AdvNoteDataIndices[note['Index']] = trueIndex
            trueIndex += 1

            pages.addItem(f"{self.AdvNotesLabelsContents[note['TitleLabel']][0]['str']} {self.AdvNotesTitlePageCounts[note['TitleLabel']]}")
            self.AdvNotesContents[note['Index']] = note


        self.NextPageIndex = pages.count() + 1
        

    def adventureNotesPageChanged(self):

        if len(self.ui.listAdventureNotePages.selectedItems()) == 0:
            return
        
        self.SelectedPageIndex = self.ui.listAdventureNotePages.currentIndex().row()
        print(f"Length of list = {self.ui.listAdventureNotePages.count()}")
        print(f"SelectedPageIndex = {self.SelectedPageIndex}")
        selectedPage = self.SelectedPageIndex + 1 #add 1 because the indexes in the file are 1-indexed.
        pageData = self.AdvNotesContents[selectedPage]
        print(pageData)
        pageTitle = pageData['TitleLabel']
        pageText = pageData['TextLabel']
        pagePatchText = pageData['TextLabelPatch']
        pageNoteShowFlag = pageData['NoteShowFlag']
        pageImage = pageData['Image']
        pageOpenFlag = pageData['OpenFlag']

        self.ui.titleLabelLineEdit.setText(pageTitle)
        self.ui.textLabelLineEdit.setText(pageText)
        self.ui.textLabelPatchLineEdit.setText(pagePatchText)
        self.ui.noteShowFlagLineEdit.setText(str(pageNoteShowFlag))
        self.ui.imageLineEdit.setText(pageImage)
        self.ui.openFlagLineEdit.setText(str(pageOpenFlag))

        # Populate the title and text fields with the actual contents.

        # The titles just have one wordDataArray entry, so they can always just be indexed at 0.

        title = self.AdvNotesLabelsContents[pageTitle][0]['str']
        self.ui.textEditPageTitle.setText (title)

        # Page contents can be variable length, so we need to concat it all together.

        #TextLabel first
        msg = ""
        for words in self.AdvNotesLabelsContents[pageText]:
            if words['patternID'] == 5:
                    msg += "<name>" + '\n'
            else:
                msg += words['str'] + '\n'

        self.ui.textEditTextLabel.setText(msg)

        #TextLabelPatch next
        msg = ""
        for words in self.AdvNotesLabelsContents[pagePatchText]:
            if words['patternID'] == 5:
                    msg += "<name>" + '\n'
            else:
                msg += words['str'] + '\n'

        self.ui.textEditTextLabelPatch.setText(msg)

        return
    
    def btnAddPageClicked(self):
        
        if self.ui.titleLabelLineEdit.text() not in self.AdvNotesLabelsContents:
            newTitle = worddata.convert2BDSPNoteTitle(self.ui.textEditPageTitle.toPlainText(), self.NextLabelIndex, self.NextArrayIndex, False, self.ui.titleLabelLineEdit.text())
            self.NextLabelIndex += 1
            self.NextArrayIndex += 1
            self.DLPAdventureNoteOpenFile['labelDataArray'].append(newTitle)
            self.AdvNotesLabelsContents[self.ui.titleLabelLineEdit.text()] = newTitle['wordDataArray']
            self.AdvNotesTitlePageCounts[self.ui.titleLabelLineEdit.text()] = 1
            self.AdvNotesLabelsIndices[self.ui.titleLabelLineEdit.text()] = len(self.AdvNotesLabelsIndices) #this will be the len before we've added the new entry, which is ultimately what we want
        else:
            self.AdvNotesTitlePageCounts[self.ui.titleLabelLineEdit.text()] += 1
        
        if self.ui.textLabelLineEdit.text() not in self.AdvNotesLabelsContents:
            print(self.ui.textEditTextLabel.toPlainText())
            newText = worddata.convert2BDSPNoteText(self.ui.textEditTextLabel.toPlainText(), self.NextLabelIndex, self.NextArrayIndex, False, self.ui.textLabelLineEdit.text())
            self.NextLabelIndex += 1
            self.NextArrayIndex += 1
            self.DLPAdventureNoteOpenFile['labelDataArray'].append(newText)
            self.AdvNotesLabelsContents[self.ui.textLabelLineEdit.text()] = newText['wordDataArray']
            self.AdvNotesLabelsIndices[self.ui.textLabelLineEdit.text()] = len(self.AdvNotesLabelsIndices) #this will be the len before we've added the new entry, which is ultimately what we want

        if self.ui.textLabelPatchLineEdit.text() not in self.AdvNotesLabelsContents:
            newTextPatch = worddata.convert2BDSPNoteText(self.ui.textEditTextLabelPatch.toPlainText(), self.NextLabelIndex, self.NextArrayIndex, False, self.ui.textLabelPatchLineEdit.text())
            self.NextLabelIndex += 1
            self.NextArrayIndex += 1
            self.DLPAdventureNoteOpenFile['labelDataArray'].append(newTextPatch)
            self.AdvNotesLabelsContents[self.ui.textLabelPatchLineEdit.text()] = newTextPatch['wordDataArray']
            self.AdvNotesLabelsIndices[self.ui.textLabelPatchLineEdit.text()] = len(self.AdvNotesLabelsIndices) #this will be the len before we've added the new entry, which is ultimately what we want

        data = {
            "Index": len(self.AdvNoteDataIndices) + 1,
            "Version": 0,
            "Category": 1,
            "TitleLabel": self.ui.titleLabelLineEdit.text(),
            "TextLabel": self.ui.textLabelLineEdit.text(),
            "TextLabelPatch": self.ui.textLabelPatchLineEdit.text(),
            "NoteShowFlag": int(self.ui.noteShowFlagLineEdit.text()),
            "Image": self.ui.imageLineEdit.text(),
            "OpenFlag": int(self.ui.openFlagLineEdit.text())
        }

        self.AdvNoteDataIndices[data['Index']] = data['Index'] - 1
        self.AdventureNoteDataOpenFile['Data'].append(data)
        self.AdvNotesContents[data['Index']] = data
        self.ui.listAdventureNotePages.addItem(f"{self.ui.textEditPageTitle.toPlainText()} {self.AdvNotesTitlePageCounts[data['TitleLabel']]}")
        return
    
    def btnReplacePageClicked(self):

        if self.SelectedPageIndex == -1:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Select a page to replace.")
            msg.exec_()
            return

        try:
            #Update the entries in dlp_adventure_note.json
            titleLabel = self.ui.titleLabelLineEdit.text ()
            newTitle = worddata.convert2BDSP(self.ui.textEditPageTitle.toPlainText(), 0, 0, False, "")
            self.DLPAdventureNoteOpenFile['labelDataArray'][self.AdvNotesLabelsIndices[titleLabel]]['wordDataArray'] = newTitle['wordDataArray']
            
            textLabel = self.ui.textLabelLineEdit.text()
            newText = worddata.convert2BDSP(self.ui.textEditTextLabel.toPlainText(), 0, 0, False, "")
            self.DLPAdventureNoteOpenFile['labelDataArray'][self.AdvNotesLabelsIndices[textLabel]]['wordDataArray'] = newText['wordDataArray']

            textPatchLabel = self.ui.textLabelPatchLineEdit.text()
            newTextPatch = worddata.convert2BDSP(self.ui.textEditTextLabelPatch.toPlainText(), 0, 0, False, "")
            self.DLPAdventureNoteOpenFile['labelDataArray'][self.AdvNotesLabelsIndices[textPatchLabel]]['wordDataArray'] = newTextPatch['wordDataArray']

            #Update the entries in AdventureNoteData.json
            
            self.AdventureNoteDataOpenFile['Data'][self.SelectedPageIndex]['TitleLabel'] = self.ui.titleLabelLineEdit.text()
            self.AdventureNoteDataOpenFile['Data'][self.SelectedPageIndex]['TextLabel'] = self.ui.textLabelLineEdit.text()
            self.AdventureNoteDataOpenFile['Data'][self.SelectedPageIndex]['TextLabelPatch'] = self.ui.textLabelPatchLineEdit.text()
            self.AdventureNoteDataOpenFile['Data'][self.SelectedPageIndex]['NoteShowFlag'] = int(self.ui.noteShowFlagLineEdit.text())
            self.AdventureNoteDataOpenFile['Data'][self.SelectedPageIndex]['Image'] = self.ui.imageLineEdit.text()
            self.AdventureNoteDataOpenFile['Data'][self.SelectedPageIndex]['OpenFlag'] = int(self.ui.openFlagLineEdit.text())

            self.AdvNotesContents[self.SelectedPageIndex+1] = self.AdventureNoteDataOpenFile['Data'][self.SelectedPageIndex]

            self.AdvNotesLabelsContents[titleLabel] = newTitle['wordDataArray']
            self.AdvNotesLabelsContents[textLabel] = newText['wordDataArray']
            self.AdvNotesLabelsContents[textPatchLabel] = newTextPatch['wordDataArray']
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(str(e))
            msg.exec_()
        return
    
    def btnSavePageClicked(self):
        try:
            dlpFile = "english_dlp_adventure_note.json"
            advNoteDataFile = "AdventureNoteData.json"

            if os.path.exists(self.outputs) == False:
                os.makedirs(self.outputs)

            with open(self.outputs+"\\new_" + dlpFile, 'w+', encoding="utf-8") as outfile:
                json.dump(self.DLPAdventureNoteOpenFile, outfile)

            with open(self.outputs+"\\new_" + advNoteDataFile, 'w+', encoding="utf-8") as outfile:
                json.dump(self.AdventureNoteDataOpenFile, outfile)

        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("An error occurred trying to save your changes:\n" + str(e) + "\nMake sure the 'output' folder exists in the same " +
               "directory as this executable, and then try again.")
            msg.exec_()
        return
    
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
        self.ui.btnAdventureNotes.clicked.connect(self.openAdventureNotesEditor)

        self.adventureNotesEditor = AdventureNotesEditorForm()

        # if self.ui.textEditNewMsg.font().family() == 'FOT-UDKakugoC80 Pro DB':
        #     self.ui.textEditNewMsg.setFontPointSize(17)
        list = self.ui.listMsgNames
        files = self.ui.listFileNames
        
        
        fileList = os.listdir(self.path)
        
        for f in fileList:
            if f != "MsgWindowData.json" and f != "english_dlp_speakers_name.json" and f != "AdventureNoteData.json" and f != "english_dlp_adventure_note.json":
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
    
    def openAdventureNotesEditor(self):
        self.adventureNotesEditor.show()


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