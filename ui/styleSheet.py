from enum import Enum


class Theame(Enum):
    Dark = 1 
    Light = 0


def getBtnStyleSheet(theame: Theame) -> "":
    if (theame == Theame.Dark):
        return ("QPushButton{"
                "border-radius: 6px;"
                "background-color: rgb(103,187,198);"
                "color: rgb(0, 0, 0);"
                "font-size: 24px;"
                "}"
                "QPushButton:hover{"
                "background-color: rgb(176, 196, 222);" 
                "}")
    else:
        return "NOtlalalal"

def getTableWidgetStyleSheet(theame: Theame) -> "":
    if (theame == Theame.Dark):
        return ("QTableWidget{"
                "border-radius: 6px;"
                "background-color: rgb(197,236,241);"
                "color: rgb(0, 0, 0);"
                "font-size: 24px;"
                "}"
                "QHeaderView::section {"
                 "background-color: #C5ECF1;"
                "color: #333;"
                "}")
    else:
        return "lalala"