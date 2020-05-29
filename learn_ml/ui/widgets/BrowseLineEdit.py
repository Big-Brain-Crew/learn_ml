from Qt.QtWidgets import *
from Qt import QtCore, QtGui


class BrowseLineEdit(QWidget):
    ''' Widget similar to QLineEdit that includes a file browse button.

    This method acts very similar to a QLineEdit, except that it also includes a browse file button.
    When a file is selected from the FileDialog, the selected file will automatically populate the LineEdit field.

    '''

    def __init__(self, parent=None):
        ''' Initializes the BrowseLineEdit widget.

        args:
            parent: parent widget

        '''
        QWidget.__init__(self, parent)


        # Define the line edit field for file path
        self.field = QLineEdit()

        # Define the browse button and connect to the browse action
        self.button = QPushButton("Browse")
        self.button.clicked.connect(self._browse)

        # Create horizontal layout and add widgets
        layout = QHBoxLayout()
        layout.addWidget(self.field)
        layout.addWidget(self.button)

        # Set margin around contents
        layout.setContentsMargins(1,1,1,1)

        # Add layout to self
        self.setLayout(layout)

    def _browse(self):
        ''' Opens the File Dialog to choose a file.

        '''

        # Open the File Dialog to select a file
        file_name = QFileDialog.getOpenFileName(self,
            caption = "Select Identity File")

        if type(file_name) in [tuple, list]:
            path = file_name[0]
        else:
            path = file_name
        if path != '':
            self.field.setText(path)

    def text(self):
        ''' Returns the text in the field.

        Returns:
            String containing the text in the field.

        '''

        return self.field.text()