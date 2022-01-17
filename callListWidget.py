import sys
import json
import tkinter as tk
import os
import rapidjson
import worddatagenerator as worddata
from tkinter import filedialog
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtGui import QFont
from demoListWidget import *
class MyForm(QDialog):
    
    MessageList = {}
    FontSize = 54
    FontSizeAmp = 0.63
    path = "input"
    outputs = "output"
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.textEditNewMsg.textChanged.connect(self.dispNewMsgContents)
        self.ui.listFileNames.currentItemChanged.connect(self.popMessages)
        self.ui.listMsgNames.currentItemChanged.connect(self.dispMsgContents)
        self.ui.btnAddMsg.clicked.connect(self.addMsg)
        
        list = self.ui.listMsgNames
        files = self.ui.listFileNames
        
        
        fileList = os.listdir(self.path)
        
        for f in fileList:
            files.addItem(f)
        
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
    
    def addMsg(self):
        msgFile = self.ui.listFileNames.currentItem().text()
        
        if os.path.exists(self.outputs) == False:
            os.makedirs(self.outputs)
        
        with open(self.path+"\\"+msgFile, encoding="utf-8") as msgs:
            Messages = json.load(msgs)
            nextLabelIndex = 0
            nextArrayIndex = 0
            realIndex = 0
            for Msg in Messages['labelDataArray']:
                labelIndex = Msg['labelIndex']
                arrayIndex = Msg['arrayIndex']
                
                if labelIndex >= nextLabelIndex:
                    nextLabelIndex = labelIndex + 1
                if arrayIndex >= nextArrayIndex:
                    nextArrayIndex = arrayIndex + 1
                    
            newMsg = worddata.convert2BDSP(self.ui.textEditNewMsg.toPlainText(), False, "REPLACE THIS")
            print (newMsg)
            Messages['labelDataArray'].append(newMsg)
            
            with open(self.outputs+"\\new_" + msgFile, 'w+', encoding="utf-8") as outfile:
                json.dump(Messages, outfile)
            
        
        
    def popMessages(self):
        msgFile = self.ui.listFileNames.currentItem().text()
        list = self.ui.listMsgNames
        list.clear()
        self.MessageList = {}
        
        with open(self.path+"\\"+msgFile, encoding="utf-8") as msgs:
            Messages = json.load(msgs)
            FileName = Messages['m_Name']
            print(FileName)
            RealIndex = 0
            
            for Msg in Messages['labelDataArray']:
                labelIndex = Msg['labelIndex']
                arrayIndex = Msg['arrayIndex']
                labelName = Msg['labelName']
                
                if labelName == "":
                    continue;
                    
                self.MessageList[labelName] = Msg
                
                style = Msg['styleInfo']
                attribute = Msg['attributeValueArray']
                dialog = [{}]
                for WordData in Msg['wordDataArray']:
                    dialog.append(WordData)
                print(labelName)
                list.addItem(labelName)
        
    def dispNewMsgContents(self):
        self.ui.msgContents.setFont(QFont('Arial', round(self.FontSize*self.FontSizeAmp)))
        self.ui.msgContents.setText(self.ui.textEditNewMsg.toPlainText())
        
    def dispMsgContents(self):
        if None is self.ui.listMsgNames.currentItem():
            return
            
        labelName = self.ui.listMsgNames.currentItem().text()
        msg = ""
        
        for words in self.MessageList[labelName]['wordDataArray']:
            msg += words['str'] + '\n'
            
        self.ui.msgContents.setFont(QFont('Arial', round(self.MessageList[labelName]['styleInfo']['fontSize']*0.63)))
        self.ui.msgContents.setText(msg)
if __name__=="__main__":
    app = QApplication(sys.argv)
    w = MyForm()
    w.show()
    sys.exit(app.exec_())