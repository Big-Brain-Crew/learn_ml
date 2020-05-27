import sys
from App import LearnML
from Qt.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)

    instance = LearnML.instance(software="standalone")
    if instance is not None:
        app.setActiveWindow(instance)
        instance.show()

        try:
            sys.exit(app.exec_())
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
