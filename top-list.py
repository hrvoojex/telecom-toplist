#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import datetime
from PySide import QtGui
from PySide import QtCore
from PySide.QtCore import Slot
from functools import partial


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

        # create instance of each 'select' menu widget and shows default one
        self.app = App(self)
        #self.app.show()  # Comment this out not to show default tab,but empty
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

        menuSelect = self.menuBar().addMenu("Mode")
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

        # add a label to write a file in it
        self.labelAbout = QtGui.QLabel(self)

        # write a file in a label
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
        
        
class BrowseAndSubmit(QtGui.QWidget):
    def __init__(self, parent=None):
        super(BrowseAndSubmit, self).__init__(parent)
        
        self.inputfileLabel = QtGui.QLabel("Input file:")
        self.inputfileLabel.setAlignment(QtCore.Qt.AlignRight)
        self.fileLabel = QtGui.QLabel()
        self.fileLabel.setFrameStyle(QtGui.QFrame.Box | QtGui.QFrame.Sunken)
        self.fileButton = QtGui.QPushButton("&Browse")
        self.fileButton.clicked.connect(self.select_file)
        self.outputfileLabel = QtGui.QLabel("Output file:")
        self.outputfileLabel.setAlignment(QtCore.Qt.AlignRight)
        self.outputfileLine = QtGui.QLineEdit()
        self.outputfileLine.setText("toplist-" + \
                                    str(datetime.date.today()) + ".csv")
        self.encodingLabel = QtGui.QLabel("Encoding:")
        self.encodingLabel.setAlignment(QtCore.Qt.AlignRight)
        self.submitButton = QtGui.QPushButton("&Submit")
        self.submitButton.setMinimumSize(50, 50)
        self.submitButton.setDisabled(True)
        
    @Slot()
    def select_file(self):
        """
        Select a file from a disk and return the name of that file
        """
        # (self.fname, _) is a tuple, we take only self.fname not the path
        self.fname, _ = QtGui.QFileDialog.getOpenFileName()
        print(self.fname)  # for debugging
        self.fileLabel.setText(self.fname)
        if self.fname:
            self.submitButton.setEnabled(True)
        else:
            self.submitButton.setDisabled(True)


class App(QtGui.QWidget):
    """
    application logic in a main window
    """
    def __init__(self, parent=None):
        super(App, self).__init__(parent)

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

        # Browse and Submit widgets
        self.browse_and_submit = BrowseAndSubmit()

        self.setMinimumSize(450, 300)
        self.setWindowTitle("Landline Toplist-Com")

        # layouts of widgets
        self.keywordeLabel = QtGui.QLabel("Choose a keyword:")
        self.keywordeLabel.setAlignment(QtCore.Qt.AlignRight)
        self.keywordComboBox = QtGui.QComboBox()
        self.keywordComboBox.addItems(self.toplist_keywords)
        self.browse_and_submit.encodingLabel = QtGui.QLabel("Encoding:")
        self.browse_and_submit.encodingLabel.setAlignment(QtCore.Qt.AlignRight)
        self.encodingLine = QtGui.QLineEdit()
        self.encodingLine.setText("windows-1250")
        self.browse_and_submit.outputfileLabel = QtGui.QLabel("Outputt file:")
        self.browse_and_submit.outputfileLabel.setAlignment(
                QtCore.Qt.AlignRight)
        self.browse_and_submit.outputfileLine = QtGui.QLineEdit()
        self.browse_and_submit.outputfileLine.setText(
                "toplist-landline-" + str(datetime.date.today()) + ".csv")
        self.addressLabel = QtGui.QLabel("Addressbook csv file:")
        self.addressLabel.setAlignment(QtCore.Qt.AlignRight)
        self.statusaddressLabel = QtGui.QLabel()
        self.statusaddressLabel.setFrameStyle(
                QtGui.QFrame.Box | QtGui.QFrame.Sunken)
        self.addressButton = QtGui.QPushButton("Browse", self)

        self.browse_and_submit.submitButton.clicked.connect(self.do_submit)
        self.addressButton.clicked.connect(self.select_addressbook)

        # set layout
        grid = QtGui.QGridLayout()
        grid.addWidget(self.keywordeLabel, 0, 0)
        grid.addWidget(self.keywordComboBox, 0, 1, 1, 2)
        grid.addWidget(self.browse_and_submit.encodingLabel, 1, 0)
        grid.addWidget(self.encodingLine, 1, 1, 1, 2)
        grid.addWidget(self.browse_and_submit.inputfileLabel, 2, 0)
        grid.addWidget(self.browse_and_submit.fileLabel, 2, 1)
        grid.addWidget(self.browse_and_submit.fileButton, 2, 2)
        grid.addWidget(self.browse_and_submit.outputfileLabel, 4, 0)
        grid.addWidget(self.browse_and_submit.outputfileLine, 4, 1, 1, 2)
        grid.addWidget(self.addressLabel, 3, 0)
        grid.addWidget(self.statusaddressLabel, 3, 1)
        grid.addWidget(self.addressButton, 3, 2)
        grid.addWidget(self.browse_and_submit.submitButton, 6, 2)
        self.setLayout(grid)

        # hide a widget
        self.hide()

    def lines(self, csv_file, encoding_code, user_choice):
        """
        Takes a csv file as an input, filters lines by keywords,
        returns a dictionary with selected lines and data of interest
        """
        dictionary = dict()
        try:
            data = open(csv_file)
        except:
            print("No such file %s" % self.fname)
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

    @Slot()
    def select_addressbook(self):
        """
        Select the addressbook file from file system
        """
        self.aname, _ = QtGui.QFileDialog.getOpenFileName()
        # assign first element in a tuple,
        # addressbook file name as statusLabel text
        self.statusaddressLabel.setText(filename_from_path(self.aname))

    @Slot()
    def do_submit(self):
        self.keyword_string = self.keywordComboBox.currentText()
        self.encode_string = self.encodingLine.text()
        dictionary = self.lines(self.browse_and_submit.fname,
                                self.encode_string,
                                self.keyword_string)
        self.list_of_tuples = sort_dictionary_to_list(dictionary)
        try:
            self.final_tuple = self.take_from_addressbook(self.list_of_tuples,
                                                          self.aname)
        except:
            self.final_tuple = self.list_of_tuples

        self.saving_to_file(self.browse_and_submit.outputfileLine.text(),
                            self.final_tuple)
        print(self.list_of_tuples)
        self.saving_to_file(self.browse_and_submit.outputfileLine.text(),
                            self.list_of_tuples)


class Mobile(QtGui.QWidget):
    """
    Mobile widget in a main window App, inherits from App class
    Overwrites the initUI GUI method
    """
    def __init__(self, parent=None):
        super(Mobile, self).__init__(parent)

        self.initUI()

    def initUI(self):
        # set minimus size and window title
        self.setWindowTitle("Mobile Toplist-Com")

        # Browse and Submit meta widgets
        self.browse_and_submit = BrowseAndSubmit()
        self.app = App()

        # add a widget to a layout
        layout = QtGui.QGridLayout()
        
        self.outputfileLabel = QtGui.QLabel("Output file:")
        self.outputfileLabel.setAlignment(QtCore.Qt.AlignRight)
        self.outputfileLine = QtGui.QLineEdit()
        self.outputfileLine.setText(
            "toplist-mobile-" + str(datetime.date.today()) + ".csv")
        self.encodingLabel = QtGui.QLabel("Encoding:")
        self.encodingLabel.setAlignment(QtCore.Qt.AlignRight)
        self.encodingLine = QtGui.QLineEdit()
        self.encodingLine.setText("windows-1250")
        self.addressLabel = QtGui.QLabel("Addressbook csv file:")
        self.addressLabel.setAlignment(QtCore.Qt.AlignRight)
        self.statusaddressLabel = QtGui.QLabel()
        self.statusaddressLabel.setFrameStyle(
                QtGui.QFrame.Box | QtGui.QFrame.Sunken)
        self.addressButton = QtGui.QPushButton("&Browse", self)

        # grid layout
        layout.addWidget(self.encodingLabel, 0, 0)
        layout.addWidget(self.encodingLine, 0, 1, 1, 2)
        layout.addWidget(self.browse_and_submit.inputfileLabel, 1, 0)
        layout.addWidget(self.browse_and_submit.fileLabel, 1, 1)
        layout.addWidget(self.browse_and_submit.fileButton, 1, 2)
        layout.addWidget(self.addressLabel, 2, 0)
        layout.addWidget(self.statusaddressLabel, 2, 1)
        layout.addWidget(self.addressButton, 2, 2)
        layout.addWidget(self.outputfileLabel, 3, 0)
        layout.addWidget(self.outputfileLine, 3, 1, 1, 2)

        layout.addWidget(self.browse_and_submit.submitButton, 4, 2, 1, 1)
        self.setLayout(layout)
        self.hide()
        
        self.browse_and_submit.submitButton.clicked.connect(self.do_submit)
        self.addressButton.clicked.connect(self.app.select_addressbook)

    def mobile_csv(self, mobile_file, encoding_code, book=None):
        """
        Takes T-Com csv (from xslx) mobile file and
        returns dictionary with names from
        addressbook or if there is no addressbook,
        phone naumbers and amount of money spent e.g.
        {"123 456 789": 123.45} or {"Ivan H": 123.45"}
        """
        d = dict()
        try:
            data = open(mobile_file)
        except:
            print("No such file %s" % mobile_file)
            sys.exit("Quitting...")

        for line in data:
            if line.startswith("+") == False:
                continue
            line = line.rstrip()
            line = line.decode(encoding_code)
            line = line.split(";")
            #  print(line)  # for debugging
            for word in line:
                try:
                    for name in book:
                        if name == word:
                            # enters {"name":422.16}, not name:422,16
                            d[name] = float(line[35].replace(',', '.'))
                # if there is no addressbook, use phone number aka line[0]
                except:
                    d[line[0]] = float(line[35].replace(',', '.'))
        #print(d)  # for debugging
        return d

    def do_submit(self):
        #print(filename_from_path(self.browse_and_submit.fname))
        # need to add dictionary file here later
        encoding_code = str(self.encodingLine.text())
        #print(encoding_code)  # for debugging
        dictionary = self.mobile_csv(self.browse_and_submit.fname,
                                      encoding_code)
        # takes dictionary and returns sorted list of tuples
        lst = sort_dictionary_to_list(dictionary)
        print(lst)

def filename_from_path(file_path):
    """
    Takes a file path as a string and returns only a file name
    """

    return os.path.basename(file_path)
    
def sort_dictionary_to_list(diction):
        """
        Takes dictionary (e.g. from lines() function) diction
        and returns sorted list of tuples by value from dictionary.
        """
        tmp = list()
        for key, val in diction.items():
            tmp.append((val, key))
            tmp.sort(reverse=True)
        return tmp
    
def main():
    app = QtGui.QApplication(sys.argv)
    instance = MyApp()
    instance.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
