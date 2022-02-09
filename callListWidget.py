import sys
import json
import tkinter as tk
import os
import rapidjson
import uuid
import worddatagenerator as worddata
from tkinter import filedialog
from PyQt5.QtWidgets import QDialog, QApplication
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
    SelectedMessageIndex = 0
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.textEditNewMsg.textChanged.connect(self.dispNewMsgContents)
        self.ui.listFileNames.currentItemChanged.connect(self.popMessages)
        self.ui.listMsgNames.currentItemChanged.connect(self.dispMsgContents)
        self.ui.btnAddMsg.clicked.connect(self.addMsg)
        self.ui.btnReplaceMsg.clicked.connect(self.replaceMsg)
        self.ui.btnSave.clicked.connect(self.saveChanges)
        
        list = self.ui.listMsgNames
        files = self.ui.listFileNames
        
        
        fileList = os.listdir(self.path)
        
        for f in fileList:
            files.addItem(f)
        
        files.setCurrentItem(files.item(0))
        # with open(file, encoding="utf-8") as msgs:
            # Messages = json.load(msgs)
            # FileName = Messages['m_Name']
            # print(FileName)
            # RealIndex = 0
            
            # for Msg in Messages['labelDataArray']:
                # labelIndex = Msg['labelIndex']
                # arrayIndex = Msg['arrayIndex']
                # labelName = Msg['labelName']
                
                # if labelName == "":
                    # continue
                # self.MessageList[labelName] = Msg
                
                # style = Msg['styleInfo']
                # attribute = Msg['attributeValueArray']
                # dialog = [{}]
                # for WordData in Msg['wordDataArray']:
                    # dialog.append(WordData)
                # print(labelName)
                # list.addItem(labelName)
                
        self.show()
    
    def replaceMsg(self):
        newMsg = worddata.convert2BDSP(self.ui.textEditNewMsg.toPlainText(), 0, 0, False, "")
        print("Selected Message Index: " + str(self.SelectedMessageIndex))
        self.OpenFile['labelDataArray'][self.SelectedMessageIndex]['wordDataArray'] = newMsg['wordDataArray']
        print(self.OpenFile['labelDataArray'][self.SelectedMessageIndex])
        return
    
    def addMsg(self):
        msgLabel = "1-msg_" + self.ui.msgLabel.text()
        
        if os.path.exists(self.outputs) == False:
            os.makedirs(self.outputs)
              
        newMsg = worddata.convert2BDSP(self.ui.textEditNewMsg.toPlainText(), self.NextLabelIndex, self.NextArrayIndex, False, msgLabel)
        
        self.NextLabelIndex += 1
        self.NextArrayIndex += 1
        
        print (newMsg)
        self.OpenFile['labelDataArray'].append(newMsg)
        return
        
    def saveChanges(self):
        msgFile = self.ui.listFileNames.currentItem().text()

        with open(self.outputs+"\\new_" + msgFile, 'w+', encoding="utf-8") as outfile:
            json.dump(self.OpenFile, outfile)
    
    
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
        if None is self.ui.listMsgNames.currentItem():
            return
        self.SelectedMessageIndex = self.ui.listMsgNames.currentIndex().row()
        print(self.SelectedMessageIndex)
        print("dispMsgContents")
        labelName = self.ui.listMsgNames.currentItem().text()
        msg = ""
        
        for words in self.MessageList[labelName]['wordDataArray']:
            msg += words['str'] + '\n'
            
        self.ui.msgContents.setFont(QFont('Arial', 16))
        self.ui.msgContents.setText(msg)

if __name__=="__main__":
    app = QApplication(sys.argv)
    w = MyForm()
    w.show()
    sys.exit(app.exec_())