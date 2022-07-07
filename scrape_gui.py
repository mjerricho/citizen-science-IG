from cProfile import label
import sys
from tkinter import Widget
from PyQt6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit, QPushButton,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider, QGridLayout, QWidget
)

from src.modules.IGDataCollection import IGDataCollection


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Scrape from Instagram")
        self.resize(700, 300)

        layout = QGridLayout()
        labels = {}
        self.line_edits = {}

        labels['username'] = QLabel('Username')
        labels['password'] = QLabel('Password')
        labels['hashtag'] = QLabel('Hashtag')
        labels['observation_days'] = QLabel('Number of Observation Days')
        labels['max_num_obv'] = QLabel('Maximum Number of Observations')
        labels['result_directory'] = QLabel('Results Directory')

        self.line_edits['username'] = QLineEdit()
        self.line_edits['password'] = QLineEdit()
        self.line_edits['hashtag'] = QLineEdit()
        self.line_edits['observation_days'] = QLineEdit()
        self.line_edits['max_num_obv'] = QLineEdit()
        self.line_edits['result_directory'] = QLineEdit()

        layout.addWidget(labels['username'],                  0, 0, 1, 1)
        layout.addWidget(self.line_edits['username'],         0, 1, 1, 3)

        layout.addWidget(labels['password'],                  1, 0, 1, 1)
        layout.addWidget(self.line_edits['password'],         1, 1, 1, 3)

        layout.addWidget(labels['hashtag'],                   2, 0, 1, 1)
        layout.addWidget(self.line_edits['hashtag'],          2, 1, 1, 3)

        layout.addWidget(labels['observation_days'],          3, 0, 1, 1)
        layout.addWidget(self.line_edits['observation_days'], 3, 1, 1, 3)

        layout.addWidget(labels['max_num_obv'],               4, 0, 1, 1)
        layout.addWidget(self.line_edits['max_num_obv'],      4, 1, 1, 3)

        layout.addWidget(labels['result_directory'],          5, 0, 1, 1)
        layout.addWidget(self.line_edits['result_directory'], 5, 1, 1, 3)

        button_scrape = QPushButton('Scrape', clicked=self.scrape)
        layout.addWidget(button_scrape,                       6, 0, 1, 4)

        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)
    
    def scrape(self):
        print("logging in")
        IGDC = IGDataCollection(
                username=self.line_edits['username'].text(), 
                password=self.line_edits['password'].text(), 
                hashtag=self.line_edits['hashtag'].text(), 
                num_days_collect=int(self.line_edits['observation_days'].text()), 
                result_dir=self.line_edits['result_directory'].text())
        print("logged in")
        print("scraping")
        IGDC.scrape_data(int(self.line_edits['max_num_obv'].text()), download=True, save_md=True)
        print("done")

def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()


if __name__ == '__main__':
    main()
