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
        return ('QPushButton{'
                'border-radius: 3px;'
                'background-color: rgb(37,72,91);'
                'color: rgb(255, 255, 255);'
                'font-size: 16px;'
                '}'
                'QPushButton:hover{'
                'background-color: rgb(103,187,198);' 
                'color: rgb(0, 0, 0);'
                '}')

def getTableWidgetStyleSheet(theame: Theame) -> str:
    if (theame == Theame.Dark):
        return (
                """
                QTableWidget {
                background-color: rgb(37,72,91); /* Фон свободного пространства */
                }

                QTableWidget QTableCornerButton::section {
                    background-color: rgb(197,236,241); /* Фон угловой ячейки */
                }

                QTableWidget::item {
                    background-color: rgb(197,236,241);
                     color: rgb(0, 0, 0);  /* Фон ячеек */
                }
                
                QHeaderView::section {
                background-color: #C5ECF1;
                color: #333;
                font-size: 16px;
                }
                """
                )
    else:
        return (
                """
                QTableWidget {
                background-color: rgb(197,236,241); /* Фон свободного пространства */
                }

                QTableWidget QTableCornerButton::section {
                    background-color: rgb(103,187,198); /* Фон угловой ячейки */
                }

                QTableWidget::item {
                    background-color: rgb(103,187,198);
                     color: rgb(0,0,0);  /* Фон ячеек */
                }
                
                QHeaderView::section {
                background-color: rgb(103,187,198);
                color: rgb(0, 0, 0);
                font-size: 16px;
                }
                """
                )

def getComboBoxStyleSheet(theame: Theame) -> str:
    if (theame == Theame.Dark):
        return ('QComboBox{'
                'border-radius: 3px;'
                'background-color: rgb(103,187,198);'
                'color: rgb(0, 0, 0);'
                'font-size: 16px;'
                '}')
    else:
        return ('QComboBox{'
                'border-radius: 3px;'
                'background-color: rgb(37,72,91);'
                'color: rgb(255, 255, 255);'
                'font-size: 16px;'
                '}')

def getDatePickerStyleSheet(theame: Theame) -> str:
    if (theame == Theame.Dark):
        return (
        'QDateEdit {'
        'background-color: rgb(197, 236, 241);'
        'color: rgb(0, 0, 0);'
        'font-size: 12px;'
        '}'
        )
    else:
        return (
        'QDateEdit {'
        'background-color: rgb(103,187,198);'
        'color: rgb(0, 0, 0);'
        'font-size: 12px;'
        '}'
        )

def getMainWindowStyleSheet(theame: Theame) -> str:
    if theame == Theame.Dark:
        return (
            "background-color: rgb(37,72,91);"  # Dark theme background color
            "color: white;"  # Dark theme text color
        )
    else:
        return (
            "background-color: rgb(197,236,241);"  # Light theme background color
            "color: black;"  # Light theme text color
        )

def getActionStyelSheet(theame : Theame) -> str:
    if theame == Theame.Dark:
        return(
            """
            QMenuBar {
                background-color: rgb(37,72,91); /* Цвет фона */
            }
            QMenuBar::item {
                background-color: rgb(37,72,91); /* Цвет фона элементов */
                color: rgb(255,255,255); /* Цвет текста элементов */
            }
            QMenuBar::item:selected  {
            background-color: rgb(103,187,198); /* Цвет фона элементов */
            color: rgb(0,0,0); /* Цвет текста элементов */
            }
            QMenu {
                background-color: rgb(103,187,198); /* Цвет фона */
            }
            QMenu::item {
                background-color: rgb(37,72,91); /* Цвет фона элементов */
                color: rgb(255,255,255); /* Цвет текста элементов */
            }
            QMenu::item:selected {
            background-color: rgb(103,187,198); /* Цвет фона элементов */
            color: rgb(0,0,0); /* Цвет текста элементов */
            }
            """
        )
    else:
        return (
            """
            QMenuBar {
                background-color: rgb(197, 236, 241); /* Цвет фона */
            }
            QMenuBar::item {
                background-color: rgb(197, 236, 241); /* Цвет фона элементов */
                color: rgb(0,0,0); /* Цвет текста элементов */
            }
            QMenuBar::item:selected  {
            background-color: rgb(103,187,198); /* Цвет фона элементов */
            color: rgb(0,0,0); /* Цвет текста элементов */
            }
            QMenu {
                background-color: rgb(103,187,198); /* Цвет фона */
            }
            QMenu::item {
                background-color: rgb(197, 236, 241); /* Цвет фона элементов */
                color: rgb(0,0,0); /* Цвет текста элементов */
            }
            QMenu::item:selected {
            background-color: rgb(37,72,91); /* Цвет фона элементов */
            color: rgb(255,255,255); /* Цвет текста элементов */
            }
            """
        )
