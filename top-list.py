#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import datetime
from PySide import QtGui
from PySide import QtCore
from PySide.QtCore import Slot


class MyApp(QtGui.QMainWindow):
    """
    This class presents main application window
    """
    def __init__(self, parent=None):
        super(MyApp, self).__init__(parent)

        # main window size, title and icon
        self.setMinimumSize(500, 350)
        self.setWindowTitle("Toplist-Com")
        self.setWindowIcon(QtGui.QIcon("toplist-com.png"))

        # add status bar at the bottom of the main window
        self.statusBar().showMessage('Ready')

        # create instance of each tool widget and shows default one
        self.app = App(self)
        self.app.show()
        self.mobile = Mobile(self)
        # new pop up window for "About" info, no parent == new window
        self.about = About()

        # layout for central widget
        centralWidget = QtGui.QWidget()
        centralLayout = QtGui.QGridLayout()
        centralLayout.addWidget(self.app, 0, 0)
        centralLayout.addWidget(self.mobile, 1, 0)
        centralWidget.setLayout(centralLayout)

        self.setCentralWidget(centralWidget)

        # set the menu bar
        menuFile = self.menuBar().addMenu("File")
        menuFile.addAction("Exit", self.close)

        menuSelect = self.menuBar().addMenu("Select")
        menuSelect.addAction("Landline", self.show_app)
        menuSelect.addAction("Mobile", self.show_mobile)

        menuHelp = self.menuBar().addMenu("Help")
        menuHelp.addAction("About", self.show_about)

    def show_app(self):
        self.app.show()
        self.mobile.hide()
        self.statusBar().showMessage("Landline")
        self.setWindowTitle("Toplist-Com Landline")

    def show_mobile(self):
        self.app.hide()
        self.mobile.show()
        self.statusBar().showMessage("Mobile")
        self.setWindowTitle("Toplist-Com Mobile")

    def show_about(self):
        self.about = About()
        self.about.show()


class About(QtGui.QWidget):
    """
    New pop up "About" window
    """
    def __init__(self, parent=None):
        super(About, self).__init__(parent)

        # set minimus size and window title
        self.setMinimumSize(450, 300)
        self.setWindowTitle("About Toplist-Com")


        self.labelAbout = QtGui.QLabel(self)

        # write a file A"aboutfile" in a label
        aboutfile = "About.txt"
        fh = open(aboutfile, "r")
        with fh:
            data = fh.read()
            self.labelAbout.setText(data)

        # add a widget self.labelAbout to a layout
        layout = QtGui.QGridLayout()
        layout.addWidget(self.labelAbout)
        self.setLayout(layout)
        # hide a window by default when the application starts
        self.hide()


class Mobile(QtGui.QWidget):
    """
    mobile content in a main window App
    """
    def __init__(self, parent=None):
        super(Mobile, self).__init__(parent)

        # set minimus size and window title
        self.setMinimumSize(450, 300)
        self.setWindowTitle("Mobile Toplist-Com")

        # todays date
        self.today = datetime.datetime.today()

        # add a widget to a layout
        layout = QtGui.QGridLayout()
        layout.addWidget(QtGui.QLabel("Mobile"))
        self.setLayout(layout)
        self.hide()


class App(QtGui.QWidget):
    """
    application logic in a main window
    """
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
            u'POS transakcija'
            u'Pozivi prema mobilnoj HT mre\u017di']

        self.initUI()

    def initUI(self):

        self.setMinimumSize(450, 300)
        self.setWindowTitle("Landline Toplist-Com")

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
        self.statusfileLabel = QtGui.QLabel()
        self.statusfileLabel.setFrameStyle(
            QtGui.QFrame.Box | QtGui.QFrame.Sunken)
        self.statusaddressLabel = QtGui.QLabel()
        self.statusaddressLabel.setFrameStyle(
            QtGui.QFrame.Box | QtGui.QFrame.Sunken)
        self.statusLabel_left = QtGui.QLabel("Status:")
        self.statusLabel_left.setAlignment(QtCore.Qt.AlignTop)
        self.submitButton = QtGui.QPushButton("&Submit")
        self.submitButton.setMinimumSize(50, 50)

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
        grid.addWidget(self.keywordComboBox, 1, 1, 1, 2)
        grid.addWidget(self.encodingLine, 2, 1, 1, 2)
        grid.addWidget(self.keywordeLabel, 1, 0)
        grid.addWidget(self.encodingLabel, 2, 0)
        grid.addWidget(self.fileLabel, 3, 0)
        grid.addWidget(self.fileButton, 3, 2)
        grid.addWidget(self.statusfileLabel, 3, 1)
        grid.addWidget(self.statusaddressLabel, 5, 1)
        grid.addWidget(self.submitButton, 7, 2)
        grid.addWidget(self.outputfileLabel, 4, 0)
        grid.addWidget(self.outputfileLine, 4, 1, 1, 2)
        grid.addWidget(self.addressLabel, 5, 0)
        grid.addWidget(self.addressButton, 5, 2)

        self.setLayout(grid)

        # hide a widget
        self.hide()

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

    def saving_to_file(self, filename, resulting_tuple_list):
        """
        Saves result to a csv file. Takes listname and saves it
        to a csv file named filename
        """
        f = open(filename, "w")
        count = 0
        for tuple_list_item in resulting_tuple_list:
            count += 1
            location = tuple_list_item[1].encode(self.encode_string)
            f.write("{0:5}; {1:25}; {2:5}\n".format(count,
                                                    location,
                                                    tuple_list_item[0]))
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

    def filename_from_path(self, file_path):
        """
        Takes file path as string and returns
        only a file name without path
        """
        count = 0
        file_name = ""
        for char in file_path:
            count += 1
            if file_path[-count] == "/" or file_path[-count] == "\\":
                break
            file_name = file_name + file_path[-count]

        num = 0
        new_file_name = ""
        for char in file_name:
            num += 1
            new_file_name += file_name[-num]

        return  new_file_name

    @Slot()
    def select_file(self):
        """
        You choose a file from a disk
        """
        self.fname = QtGui.QFileDialog.getOpenFileName()
        # print first element in a tuple self.fname[0] which is a file name
        # that it calls file_name_from_path to print only a file name
        self.statusfileLabel.setText(str(
            self.filename_from_path(self.fname[0])))
        # self.statusfileLabel.setAlignment(QtCore.Qt.AlignTop)
        if str(self.fname[0]) is not "":
            self.submitButton.setEnabled(True)
        else:
            self.submitButton.setDisabled(True)

    @Slot()
    def select_addressbook(self):
        """
        Select the addressbook file from file system
        """
        self.aname = QtGui.QFileDialog.getOpenFileName()
        # assign first element in a tuple,
        # addressbook file name as statusLabel text
        self.statusaddressLabel.setText(
            self.filename_from_path(str(self.aname[0])))
        #self.statusLabel.setAlignment(QtCore.Qt.AlignTop)

    @Slot()
    def do_submit(self):
        self.keyword_string = self.keywordComboBox.currentText()
        self.encode_string = self.encodingLine.text()
        dictionary = self.lines(self.fname,
                                self.encode_string,
                                self.keyword_string)
        self.list_of_tuples = self.sort_dictionary_to_list(dictionary)
        try:
            self.final_tuple = self.take_from_addressbook(self.list_of_tuples,
                                                          str(self.aname[0]))
        except:
            self.final_tuple = self.list_of_tuples

        self.saving_to_file(self.outputfileLine.text(),
                            self.final_tuple)
        print(self.list_of_tuples)
        self.saving_to_file(self.outputfileLine.text(),
                            self.list_of_tuples)


def main():

    app = QtGui.QApplication(sys.argv)
    instance = MyApp()
    instance.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
