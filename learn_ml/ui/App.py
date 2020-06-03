import os

from Qt import QtGui
from Qt import QtCore
from Qt.QtWidgets import *
#from ui.utils.stylesheet import editableStyleSheet

from ui.widgets.DeployMenu import DeployMenu

from deploy import deploy
from deploy import convert_to_edgetpu

from utils.log_configurator import LogConfigurator


EDITOR_TARGET_FPS = 60


class LearnML(QMainWindow):
    ''' Defines UI element of the Learn ML project.

        This class extends the QMainWindow class and serves as the entry point for the application.
        It will contain all of the main UI elements used to interact with our application.
    '''
    def __init__(self, parent=None):
        super(LearnML, self).__init__(parent=parent)

        # Configure the LogConfigurator and instantiate logger for this module
        self.logConfig = LogConfigurator()
        self.logger = self.logConfig.get_logger(__name__)

        self.logger.info("Starting application")

        # Use a strong focus policy
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

        # Flag storing whether the current project has been modified
        self.modified = False

        # Set title
        # App name
        self.title_name = "Learn ML"
        self.current_file_name = None
        self.set_title()
        #self.setContentsMargins(1, 1, 1, 1)

        self.menuBar = QMenuBar(self)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 863, 21))
        self.menuBar.setObjectName("menu_bar")
        self.setMenuBar(self.menuBar)

        self.setMouseTracking(True)

        self.fps = EDITOR_TARGET_FPS
        self.tick_timer = QtCore.QTimer()



    # def startMainLoop(self):
    #     self.tick_timer.timeout.connect(self.mainLoop)
    #     self.tick_timer.start(1000 / EDITOR_TARGET_FPS)

    # def stopMainLoop(self):
    #     self.tick_timer.stop()
    #     self.tick_timer.timeout.disconnect()

    # def mainLoop(self):
    #     deltaTime = currentProcessorTime() - self._lastClock
    #     ds = (deltaTime * 1000.0)
    #     if ds > 0:
    #         self.fps = int(1000.0 / ds)

    #     # Tick all graphs
    #     # each graph will tick owning raw nodes
    #     # each raw node will tick it's ui wrapper if it exists
    #     self.graphManager.get().Tick(deltaTime)

    #     # Tick canvas. Update ui only stuff such animation etc.
    #     self.canvasWidget.Tick(deltaTime)

    #     self._lastClock = currentProcessorTime()


    def set_title(self):
        ''' Sets the title of the application.

        The title will be Learn ML - {Current Project Name}.If the project has been modified,
        there will be an asterisk following the project name.
        '''

        label = "Untitled"
        if self.current_file_name is not None:
            if os.path.isdir(self.current_file_name):
                label = os.path.basename(self.current_file_name)
        if self.modified:
            label += "*"

        self.setWindowTitle("{} - {}".format(self.title_name, label))

    def populateMenu(self):
        ''' Adds all of the options to the menu bar.

        Currently, the only available options are the File option, which contains
        options to create a new project or open an existing project.
        '''

        file_menu = self.menuBar.addMenu("File")

        # Define new project action
        new_project_action = file_menu.addAction("New Project")
        # newFileAction.setIcon(QtGui.QIcon(":/new_file_icon.png"))
        # newFileAction.triggered.connect(self.newFile)

        # Define open project option
        load_project_action = file_menu.addAction("Open Project")
        # loadAction.setIcon(QtGui.QIcon(":/folder_open_icon.png"))
        load_project_action.triggered.connect(self.load)

        # Define deploy project action
        deploy_project_action = file_menu.addAction("Deploy Project")
        deploy_project_action.triggered.connect(self.deploy)

        # saveAction = fileMenu.addAction("Save")
        # saveAction.setIcon(QtGui.QIcon(":/save_icon.png"))
        # saveAction.triggered.connect(self.save)

        # saveAsAction = fileMenu.addAction("Save as")
        # saveAsAction.setIcon(QtGui.QIcon(":/save_as_icon.png"))
        # saveAsAction.triggered.connect(lambda: self.save(True))

        # IOMenu = fileMenu.addMenu("Custom IO")
        # for packageName, package in GET_PACKAGES().items():
        #     # exporters
        #     exporters = None
        #     try:
        #         exporters = package.GetExporters()
        #     except:
        #         continue
        #     pkgMenu = IOMenu.addMenu(packageName)
        #     for exporterName, exporterClass in exporters.items():
        #         fileFormatMenu = pkgMenu.addMenu(exporterClass.displayName())
        #         fileFormatMenu.setToolTip(exporterClass.toolTip())
        #         if exporterClass.createExporterMenu():
        #             exportAction = fileFormatMenu.addAction("Export")
        #             exportAction.triggered.connect(lambda checked=False, app=self, exporter=exporterClass: exporter.doExport(app))
        #         if exporterClass.createImporterMenu():
        #             importAction = fileFormatMenu.addAction("Import")
        #             importAction.triggered.connect(lambda checked=False, app=self, exporter=exporterClass: exporter.doImport(app))

        # editMenu = self.menuBar.addMenu("Edit")
        # preferencesAction = editMenu.addAction("Preferences")
        # preferencesAction.setIcon(QtGui.QIcon(":/options_icon.png"))
        # preferencesAction.triggered.connect(self.showPreferencesWindow)

        # pluginsMenu = self.menuBar.addMenu("Plugins")
        # packagePlugin = pluginsMenu.addAction("Create package...")
        # packagePlugin.triggered.connect(PackageWizard.run)

        # helpMenu = self.menuBar.addMenu("Help")
        # helpMenu.addAction("Homepage").triggered.connect(lambda _=False, url="https://wonderworks-software.github.io/PyFlow/": QtGui.QDesktopServices.openUrl(url))
        # helpMenu.addAction("Docs").triggered.connect(lambda _=False, url="https://pyflow.readthedocs.io/en/latest/": QtGui.QDesktopServices.openUrl(url))

    def load(self):
        ''' Opens the file dialog window to allow the user to load a project.

        This is currently configured to select a project directory. There are no checks performed
        to ensure that the project directory is valid.
        '''

        # We can define a filter to filter the acceptable file names
        # Simpler way to create a FileDialog if we have a file at some point
        #name_filter = "Graph files (*.pygraph)"
        #savepath = QFileDialog.getOpenFileName(filter=name_filter)

        # Create File Dialog and configure to select a directory
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setViewMode(QFileDialog.Detail)

        if dialog.exec_():
            project_dir = dialog.selectedFiles()

        if type(project_dir) in [tuple, list]:
            path = project_dir[0]
        else:
            path = project_dir
        if path != '':
            self.load_from_file(path)

        # Update the title with the newly opened project directory
        self.set_title()

    def load_from_file(self, project_dir):
        ''' Contains operations to execute when a project is loaded

        Currently, the only operation performed is updating the current_file_name property.
        '''
        self.current_file_name = project_dir
        # with open(filePath, 'r') as f:
        #     data = json.load(f)
        #     self.loadFromData(data, clearHistory=True)
        #     self.currentFileName = filePath
        #     EditorHistory().saveState("Open {}".format(os.path.basename(self.currentFileName)))

    def deploy(self):
        ''' Deploys the loaded model to the coral board.

        Currently, deploy can only deploy the compiled model and does not handle converting the model
        to a tflite edgetpu model. This functionality will be added once USB serial communication with
        the coral board is achieved.

        '''

        # Instantiate the deploy dialog
        # Pass a function to deploy the edgetpu model to the coral board
        deploy_dialog = DeployMenu(self,
            lambda ip_addr, iden_file : deploy.deploy(
                ip_addr,
                os.path.join(self.current_file_name, "model_edgetpu.tflite"),
                identity_file = iden_file
            )
        )
        val = deploy_dialog.exec_()
        print(val)


    @staticmethod
    def instance(parent=None):
        ''' Creates a new instance of the LearnML Main Window.

        This will configure the LearnML window and return the object

        Args:
            parent: [Optional] The parent window, if this instance is a child of another window

        Returns:
            LearnML: A configured instance of the LearnML window

        '''
        #assert(software != ""), "Invalid arguments. Please pass you software name as second argument!"

        instance = LearnML(parent)
        instance.showMaximized()
        #instance.currentSoftware = software

        #TODO What does this do
        # SessionDescriptor().software = instance.currentSoftware

        # if software == "standalone":
        #     editableStyleSheet(instance)

        # instance.startMainLoop()

        # populate tools
        # canvas = instance.getCanvas()
        # toolbar = instance.getToolbar()

        # populate menus
        instance.populateMenu()

        # geo = settings.value('Editor/geometry')
        # if geo is not None:
        #     instance.restoreGeometry(geo)
        # state = settings.value('Editor/state')
        # if state is not None:
        #     instance.restoreState(state)
        # settings.beginGroup("Tools")
        # for packageName, registeredToolSet in GET_TOOLS().items():
        #     for ToolClass in registeredToolSet:
        #         if issubclass(ToolClass, ShelfTool):
        #             ToolInstance = ToolClass()
        #             # prevent to be garbage collected
        #             instance.registerToolInstance(ToolInstance)
        #             ToolInstance.setAppInstance(instance)
        #             action = QAction(instance)
        #             action.setIcon(ToolInstance.getIcon())
        #             action.setText(ToolInstance.name())
        #             action.setToolTip(ToolInstance.toolTip())
        #             action.setObjectName(ToolInstance.name())
        #             action.triggered.connect(ToolInstance.do)
        #             # check if context menu data available
        #             menuBuilder = ToolInstance.contextMenuBuilder()
        #             if menuBuilder:
        #                 menuGenerator = ContextMenuGenerator(menuBuilder)
        #                 menu = menuGenerator.generate()
        #                 action.setMenu(menu)
        #             toolbar.addAction(action)

        #             # step to ShelfTools/ToolName group and pass settings inside
        #             settings.beginGroup("ShelfTools")
        #             settings.beginGroup(ToolClass.name())
        #             ToolInstance.restoreState(settings)
        #             settings.endGroup()
        #             settings.endGroup()

        #         if issubclass(ToolClass, DockTool):
        #             menus = instance.menuBar.findChildren(QMenu)
        #             pluginsMenuAction = [m for m in menus if m.title() == "Plugins"][0].menuAction()
        #             toolsMenu = getOrCreateMenu(instance.menuBar, "Tools")
        #             instance.menuBar.insertMenu(pluginsMenuAction, toolsMenu)
        #             packageSubMenu = getOrCreateMenu(toolsMenu, packageName)
        #             toolsMenu.addMenu(packageSubMenu)
        #             showToolAction = packageSubMenu.addAction(ToolClass.name())
        #             icon = ToolClass.getIcon()
        #             if icon:
        #                 showToolAction.setIcon(icon)
        #             showToolAction.triggered.connect(lambda pkgName=packageName, toolName=ToolClass.name(): instance.invokeDockToolByName(pkgName, toolName))

        #             settings.beginGroup("DockTools")
        #             childGroups = settings.childGroups()
        #             for dockToolGroupName in childGroups:
        #                 # This dock tool data been saved on last shutdown
        #                 settings.beginGroup(dockToolGroupName)
        #                 if dockToolGroupName in [t.uniqueName() for t in instance._tools]:
        #                     settings.endGroup()
        #                     continue
        #                 toolName = dockToolGroupName.split("::")[0]
        #                 instance.invokeDockToolByName(packageName, toolName, settings)
        #                 settings.endGroup()
        #             settings.endGroup()

        # LearnML.appInstance = instance
        # EditorHistory().saveState("New file")

        # for name, package in GET_PACKAGES().items():
        #     prefsWidgets = package.PrefsWidgets()
        #     if prefsWidgets is not None:
        #         for categoryName, widgetClass in prefsWidgets.items():
        #             PreferencesWindow().addCategory(categoryName, widgetClass())
        #         PreferencesWindow().selectByName("General")
        return instance
