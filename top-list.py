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

    def lines(self, csv_file, encoding_code, user_choice):
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
                        dictionary[line[2]] = (dictionary.get(line[2], 0) +
                                               int(line[5]))
                    elif user_choice == "TIME":
                        temp = line[6].split(":")
                        converted = float(temp[0]) + float(temp[1]) / 60.0
                        new_key = line[1] + ' ' + line[2]
                        dictionary[new_key] = (dictionary.get(new_key, 0) +
                                               converted)
                    else:
                        new_key = line[1] + ' ' + line[2]
                        dictionary[new_key] = (
                            dictionary.get(new_key, 0) +
                            # 15,2 to 15.2
                            float(line[9].replace(',', '.')))

        return dictionary

    def sort_dictionary_to_list(self, diction):
        """
        Takes dictionary (e.g. from lines() function) diction
        and returns sorted list of tuples by value from dictionary.
        """
        tmp = list()
        for key, val in diction.items():
            tmp.append((val, key))
            tmp.sort(reverse=True)
        return tmp

    def saving_to_file(self, filename):
        """
        Saves result to a csv file. Takes listname and saves it
        to a csv file named filename
        """
        f = open(filename, "w")
        count = 0
        for line in self.final_tuple:
            count += 1
            f.write("{0:3}; {1:10}; {2:3}\n".format(count,
                                                    line[1],
                                                    line[0]))
        f.close()

    def take_from_addressbook(self, list_of_tuples, csv_addressbook):
        """
        Takes a dictionary and addressbook file and compares
        identificator from dictionary to a name from addressbook
        """
        new_list = list_of_tuples
        old_list = list()
        try:
            csv_file = open(csv_addressbook)
        except:
            print("No such file %s" % csv_addressbook)

        for tpl in list_of_tuples:
            # adds second value from tuple
            # into the list "old_list" as identifier
            old_list.append(tpl[1])

        for line in csv_file:
            line = line.rstrip()
            line = line.decode(self.encodingLine.text())
            line = line.split(";")
            for word_from_csv_file in line:
                if word_from_csv_file in old_list:
                    index = old_list.index(word_from_csv_file)
                    new_list[index] = (list_of_tuples[index][0], line[2])
        return new_list

    @Slot()
    def select_file(self):
        """
        You choose a file from a disk
        """
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
        # assign first element in a tuple,
        # addressbook file name as statusLabel text
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
            self.list_of_tuples = self.sort_dictionary_to_list(dictionary)
            self.final_tuple = self.take_from_addressbook(self.list_of_tuples,
                                                          str(self.aname[0]))
            #print self.list_of_tuples
            print(self.final_tuple)
            #self.saving_to_file(self.outputfileLine.text())
            self.saving_to_file(self.outputfileLine.text())
        except ValueError:
            print ValueError
            self.statusLabel.setText("File not selected!")
            self.statusLabel.setAlignment(QtCore.Qt.AlignTop)


def main():

    app = QtGui.QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
