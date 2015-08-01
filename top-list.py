#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import datetime
from PySide import QtGui
from PySide import QtCore
from PySide.QtCore import Slot



class App(QtGui.QWidget):

    def __init__(self, parent=None):
        super(App, self).__init__(parent)

        # todays date
        self.today = datetime.date.today()

        # What do you want to search in a file: maxadsl traffic, talk time
        # or amount of money
        self.toplist_keywords = ["TRAFFIC",
                                 "TIME",
                                 "AMOUNT"]

        # default list of keywords if user choice is maxadsl
        self.maxadsl_default = [u'MAXadsl promet']

        # default list of keywords if user choice is converation time
        self.conversation_time_default = [
            u'Promet uklju\u010Den u Business Minute Fix',
            u'Promet uklju\u010Den u Business Minute Mobile',
            u'Promet uklju\u010Den u Business Minute International',
            u'POS transakcija',
            u'Me\u0111unarodni promet - VoIP',
            u'Nacionalni VPN promet-VoIP']

        # default list of keywords if user choice is amount
        self.amount_default = [
            u'Mjese\u010Dna naknada',
            u'Mjese\u010Dna naknada za ADSL pristup',
            u'Usluge s posebnim tarifama',
            u'POS transakcija']

        self.initUI()

    def initUI(self):

        self.setMinimumSize(500, 300)
        self.setWindowTitle("Telecom Top list")
        self.setWindowIcon(QtGui.QIcon("phonebill.png"))

        # layouts of widgets
        self.keywordComboBox = QtGui.QComboBox()
        self.keywordComboBox.addItems(self.toplist_keywords)
        self.encodingLine = QtGui.QLineEdit()
        self.encodingLine.setText("windows-1250")
        self.encodingLine.setPlaceholderText("e.g. windows-1250 or utf-8")
        self.keywordeLabel = QtGui.QLabel("Choose a keyword:")
        self.encodingLabel = QtGui.QLabel("Enter an encoding:")
        self.fileLabel = QtGui.QLabel("Enter a T-HT csv file:")
        #self.fileLine = QtGui.QLineEdit()
        #self.fileLine.setPlaceholderText("e.g. somefile.csv")
        self.fileButton = QtGui.QPushButton("Browse", self)
        self.fileButton.resize(self.fileButton.sizeHint())
        self.statusLabel = QtGui.QLabel()
        self.statusLabel.setFrameStyle(QtGui.QFrame.Box | QtGui.QFrame.Sunken)
        self.statusLabel_left = QtGui.QLabel("Status:")
        self.statusLabel_left.setAlignment(QtCore.Qt.AlignTop)
        self.submitButton = QtGui.QPushButton("Submit")
        self.submitButton.setDisabled(True)
        self.outputfileLine = QtGui.QLineEdit()
        self.outputfileLabel = QtGui.QLabel("Output file:")
        self.outputfileLine.setText("toplist-" + str(self.today) + ".csv")
        self.addressLabel = QtGui.QLabel("Addressbook csv file:")
        self.addressButton = QtGui.QPushButton("Browse", self)

        # event when the button is clicked
        self.fileButton.clicked.connect(self.select_file)
        self.submitButton.clicked.connect(self.do_submit)
        self.addressButton.clicked.connect(self.select_addressbook)

        # set layout
        grid = QtGui.QGridLayout()
        grid.addWidget(self.keywordComboBox, 0, 1, 1, 2)
        grid.addWidget(self.encodingLine, 1, 1, 1, 2)
        grid.addWidget(self.keywordeLabel, 0, 0)
        grid.addWidget(self.encodingLabel, 1, 0)
        grid.addWidget(self.fileLabel, 2, 0)
        grid.addWidget(self.fileButton, 2, 2)
        grid.addWidget(self.statusLabel, 5, 1, 1, 2)
        grid.addWidget(self.statusLabel_left, 5, 0)
        grid.addWidget(self.submitButton, 6, 2)
        grid.addWidget(self.outputfileLabel, 3, 0)
        grid.addWidget(self.outputfileLine, 3, 1, 1, 2)
        grid.addWidget(self.addressLabel, 4, 0)
        grid.addWidget(self.addressButton, 4, 2)

        self.setLayout(grid)

        # show a widget
        self.show()

    def lines(self, csv_file,encoding_code, user_choice):
        """
        Takes a csv file as an input,
        filters lines by keywords,
        returns a dictionary with selected lines and data of interest
        """
        dictionary = dict()
        try:
            data = open(csv_file[0])
        except:
            print("No such file %s" % self.fname[0])
            sys.exit("Quitting...")

        for line in data:
            if line.startswith("DETAIL") == False:
                continue
            line = line.rstrip()
            line = line.decode(encoding_code)
            line = line.split(";")
            for word in line:
                if user_choice == "TRAFFIC":
                    mod_list = self.maxadsl_default
                elif user_choice == "TIME":
                    mod_list = self.conversation_time_default
                else:
                    mod_list = self.amount_default

                if word in mod_list:
                    if user_choice == "TRAFFIC":
                        dictionary[line[2]] = (
                            dictionary.get(line[2], 0) + int(line[5]))
                    elif user_choice == "TIME":
                        temp = line[6].split(":")
                        converted = float(temp[0]) + float(temp[1]) / 60.0
                        new_key = line[1] + ' ' + line[2]
                        dictionary[new_key] = (
                            dictionary.get(new_key, 0) + converted)
                    else:
                        new_key = line[1] + ' ' + line[2]
                        dictionary[new_key] = (
                            dictionary.get(new_key, 0) +
                            float(line[9].replace(',', '.')))  #15,2 to 15.2
        return dictionary

    def sort_dictionary_to_list(self, diction):
        """
        Takes dictionary diction and returns
        sorted list of tuples by value from dictionary
        """
        tmp = list()
        for key, val in diction.items():
            tmp.append((val, key))
            tmp.sort(reverse=True)
        return  tmp

    def saving_to_file(self, filename):

        f = open(filename, "w")
        count = 0
        for line in self.sorted_dictionary:
            count += 1
            f.write(str(count) + ".;" + str(line[1]) + \
                    ";" + str(line[0]) + "\n")
        f.close()

    def take_from_addressbook(self, list_of_tuples, csv_addressbook):
        """
        Takes a dictionary and addressbook and compares
        identificator from dictionary to a name from addressbook
        """
        dictionary = dict()
        li = list()
        try:
            data = open(csv_addressbook)
        except:
            print("No such file %s" % csv_addressbook)
        #print dicton
        for key in list_of_tuples:
            # append second member of tuple as a identifier from csv fname
            # e.g. (12, u"borovo77"), second is borovo77
            li.append(key[1])

        for line in data:
            line = line.rstrip()
            line = line.decode(self.encodingLine.text())
            line = line.split(";")
            for word in line:
                if word in li:
                    dictionary[word] = line[2]
        #print dictionary

        #######################################################################
        # this dictionary has to be saved with a function which
        # accepts list, fix this!!!
        return dictionary

    @Slot()
    def select_file(self):

        self.fname = QtGui.QFileDialog.getOpenFileName()
        # print first element in a tuple
        self.statusLabel.setText(str(self.fname[0]))
        self.statusLabel.setAlignment(QtCore.Qt.AlignTop)
        if str(self.fname[0]) is not "":
            self.submitButton.setEnabled(True)
        else:
            self.submitButton.setDisabled(True)

    @Slot()
    def select_addressbook(self):

        self.aname = QtGui.QFileDialog.getOpenFileName()
        # print first element in a tuple
        self.statusLabel.setText(str(self.aname[0]))
        #self.statusLabel.setAlignment(QtCore.Qt.AlignTop)

    @Slot()
    def do_submit(self):
        try:
            self.keyword_string = self.keywordComboBox.currentText()
            self.encode_string = self.encodingLine.text()
            dictionary = self.lines(self.fname,
                            self.encode_string,
                            self.keyword_string)
            self.sorted_dictionary = self.sort_dictionary_to_list(dictionary)
            print self.sorted_dictionary
            self.take_from_addressbook(self.sorted_dictionary,
                                       self.aname)
            # saving to a file
            self.saving_to_file(self.take_from_addressbook())
        except:
            self.statusLabel.setText("File not selected!")
            self.statusLabel.setAlignment(QtCore.Qt.AlignTop)


def main():

    app = QtGui.QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()