from enum import Enum


class Theme(Enum):
    Dark = 1
    Light = 0


def get_btn_style_sheet(theme: Theme) -> str:
    """Get button style sheet."""
    if theme == Theme.Dark:
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


def get_table_widget_style_sheet(theme: Theme) -> str:
    """Get table style sheet."""
    if theme == Theme.Dark:
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


def get_combo_box_style_sheet(theme: Theme) -> str:
    """Get combo box style sheet."""
    if theme == Theme.Dark:
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


def get_date_picker_style_sheet(theme: Theme) -> str:
    """Get date picker style sheet."""
    if theme == Theme.Dark:
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


def get_main_window_style_sheet(theme: Theme) -> str:
    """Get main window style sheet."""
    if theme == Theme.Dark:
        return (
            'background-color: rgb(37,72,91);'  # Dark theme background color
            'color: white;'  # Dark theme text color
        )
    else:
        return (
            'background-color: rgb(197,236,241);'  # Light theme background color
            'color: black;'  # Light theme text color
        )


def get_action_style_sheet(theme: Theme) -> str:
    """Get action style sheet."""
    if theme == Theme.Dark:
        return (
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
