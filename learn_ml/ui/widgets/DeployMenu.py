''' Contains the definition of a DeployMenu widget for deploying the model to the coral board
'''

from nine import str

from Qt.QtWidgets import *
from Qt import QtCore, QtGui

from ui.widgets.BrowseLineEdit import BrowseLineEdit

from singleton_decorator import singleton


@singleton
class DeployMenu(QDialog):
    ''' QDialog widget that creates a menu for deploying the model to the coral board via ssh.

    This menu provides fields to enter the IP address and pass the identity file to connect to the coral.
    When the Ok button is pressed, the model is deployed to the coral. Currently, there is no prompt stating
    whether or not the deploy was successful. This is in the pipeline and will be added in the future.

    '''

    def __init__(self, parent=None, deploy_fn = None):
        ''' Initializes the DeployMenu

        Creates the deploy menu as a child of the parent widget that is pssed.

        Args:
            parent: A parent widget for the DeployMenu
            deploy_fn: A callback function that is used to deploy the model to the coral. This function
                should have the following signature: deploy_fn(ip_addr, iden_file)

        Returns:
            None

        '''
        QDialog.__init__(self, parent)

        assert deploy_fn is not None

        # Save the deploy function
        self.deploy_fn = deploy_fn

        self._create_form_group_box()
        self._create_button_box()

        # Build the main layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(self.buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("Deploy")

    def _create_form_group_box(self):
        ''' Creates the group box containing the ip address and identity file fields.

        The box contains a field (QLineEdit) for the ip address and a field (BrowseLineEdit)
        for the identity file.

        '''

        self.formGroupBox = QGroupBox("Deploy")
        layout = QFormLayout()

        self.ip_addr = QLineEdit()
        self.iden_file = BrowseLineEdit()

        layout.addRow(QLabel("IP Address:"), self.ip_addr)
        layout.addRow(QLabel("Identity File:"), self.iden_file)
        self.formGroupBox.setLayout(layout)

    def _create_button_box(self):
        ''' Creates the button box that contains the okay and cancel buttons.

        The buttons are connected to the self.accept and self.reject methods.

        '''
        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)



    def accept(self):
        ''' Runs the deploy_fn method and closes the window.

        This button overrides QDialog.accept to modify the accept functionality. This will also include
        a confirmation/error window to state if the deploy was (not yet implemented).

        '''

        self.deploy_fn(self.ip_addr.text(), self.iden_file.text())

        self.done(1)