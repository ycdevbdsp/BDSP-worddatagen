import sys
import json
import os
import uuid
import worddatagenerator as worddata
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox
from PyQt5.QtGui import QFont
from demoListWidget import *
class MyForm(QDialog):
    
    OpenFile = {}
    MessageList = {}
    FontSize = 54
    FontSizeAmp = 0.63
    path = "input"
    outputs = "output"
    NextLabelIndex = 0
    NextArrayIndex = 0
    SelectedMessageIndex = -1
    
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
        self.ui.btnSave.clicked.connect(self.saveChanges)
        
        list = self.ui.listMsgNames
        files = self.ui.listFileNames
        
        
        fileList = os.listdir(self.path)
        
        for f in fileList:
            files.addItem(f)
        
        files.setCurrentItem(files.item(0))
        self.show()
    
    def replaceMsg(self):
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
            self.OpenFile['labelDataArray'][self.SelectedMessageIndex]['wordDataArray'] = newMsg['wordDataArray']
            print(self.OpenFile['labelDataArray'][self.SelectedMessageIndex])
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
        #make sure an item is selected
        msgFile = self.ui.listFileNames.currentItem().text()
        list = self.ui.listMsgNames
        list.clear()
        self.MessageList = {}
        self.NextLabelIndex = 0
        self.NextArrayIndex = 0
        with open(self.path+"\\"+msgFile, encoding="utf-8") as msgs:
            self.OpenFile = json.load(msgs)
            FileName = self.OpenFile['m_Name']
            
            for Msg in self.OpenFile['labelDataArray']:
                labelIndex = Msg['labelIndex']
                arrayIndex = Msg['arrayIndex']
                labelName = Msg['labelName']
                
                if labelIndex >= self.NextLabelIndex:
                    self.NextLabelIndex = labelIndex + 1
                if arrayIndex >= self.NextArrayIndex:
                    self.NextArrayIndex = arrayIndex + 1
                    
                if labelName == "":
                    continue
                    
                self.MessageList[labelName] = Msg
                
                style = Msg['styleInfo']
                attribute = Msg['attributeValueArray']
                dialog = [{}]
                for WordData in Msg['wordDataArray']:
                    dialog.append(WordData)
                print(labelName)
                list.addItem(labelName)
        
    def dispNewMsgContents(self):
        self.ui.msgContents.setFont(QFont('Arial', 16))
        self.ui.msgContents.setText(self.ui.textEditNewMsg.toPlainText())
        
    def dispMsgContents(self):
        print(len(self.ui.listMsgNames.selectedItems()))
        if len(self.ui.listMsgNames.selectedItems()) == 0:
            return
        self.SelectedMessageIndex = self.ui.listMsgNames.currentIndex().row()
        print(self.SelectedMessageIndex)
        print("dispMsgContents")
        labelName = self.ui.listMsgNames.currentItem().text()
        msg = ""
        
        for words in self.MessageList[labelName]['wordDataArray']:
            if words['patternID'] == 5:
                msg += "<name>" + '\n'
            else:
                msg += words['str'] + '\n'
            
        self.ui.msgContents.setFont(QFont('Arial', 16))
        self.ui.msgContents.setText(msg)

if __name__=="__main__":
    app = QApplication(sys.argv)
    w = MyForm()
    w.show()
    sys.exit(app.exec_())