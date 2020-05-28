'''Main entry-point to launch the application.

This will launch the learn_ml application to a new project.
'''

import sys
from ui.App import LearnML
from Qt.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)

    instance = LearnML.instance()
    if instance is not None:
        app.setActiveWindow(instance)
        instance.show()

        try:
            sys.exit(app.exec_())
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
