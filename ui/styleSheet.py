from enum import Enum


class Theame(Enum):
    Dark = 1 
    Light = 0


def getBtnStyleSheet(theame: Theame) -> str:
    if (theame == Theame.Dark):
        return ('QPushButton{'
                'border-radius: 3px;'
                'background-color: rgb(103,187,198);'
                'color: rgb(0, 0, 0);'
                'font-size: 16px;'
                '}'
                'QPushButton:hover{'
                'background-color: rgb(176, 196, 222);' 
                '}')
    else:
        return "NOtlalalal"

def getTableWidgetStyleSheet(theame: Theame) -> str:
    if (theame == Theame.Dark):
        return ('QTableWidget{'
                'border-radius: 3px;'
                'background-color: rgb(197,236,241);'
                'color: rgb(0, 0, 0);'
                'font-size: 16px;'
                '}'
                'QHeaderView::section {'
                 'background-color: #C5ECF1;'
                'color: #333;'
                'font-size: 16px;'
                '}')
    else:
        return "lalala"

def getComboBoxStyleSheet(theame: Theame) -> str:
    if (theame == Theame.Dark):
        return ('QComboBox{'
                'border-radius: 3px;'
                'background-color: rgb(103,187,198);'
                'color: rgb(0, 0, 0);'
                'font-size: 16px;'
                '}')
    else:
        return "lalala"

def getDatePickerStyleSheet(theame: Theame) -> str:
    if (theame == Theame.Dark):
        return (
        'QCalendarWidget {'
        'background-color: rgb(197, 236, 241);'
        'color: rgb(0, 0, 0);'
        'font-size: 16px;'
        )
    else:
        return "lalala"

def getMenuStyleSheet(theame: Theame) -> str:
    if (theame == Theame.Dark):
        return ('QMainWindow {'
                'background-color: white;'
                'color: black;'
                '}')
    else:
        return('QMainWindow {'
                'background-color: rgb(50,50,50);'
                'color: white;'
                '}')

