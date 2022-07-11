import sys
from PyQt6.QtWidgets import ( QMainWindow, QApplication, QLabel, QLineEdit, QPushButton, QLineEdit, QGridLayout, QWidget )
from src.modules.IGDataCollection import IGDataCollection

# Constants
USERNAME = 'username'
PASSWORD = 'password'
HASHTAG = 'hashtag'
OBV_DAYS = 'observation_days'
MAX_NUM_OBV = 'max_num_obv_posts'
RES_DIR = 'result_directory'
inputs = [USERNAME, PASSWORD, HASHTAG, OBV_DAYS, MAX_NUM_OBV, RES_DIR]

PADDING_STYLE = 'padding: 10px'

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Scrape from Instagram")
        self.resize(700, 300)

        layout = QGridLayout()
        self.labels = {}
        self.line_edits = {}

        self.labels[USERNAME] = QLabel('Username')
        self.labels[PASSWORD] = QLabel('Password')
        self.labels[HASHTAG] = QLabel('Hashtag')
        self.labels[OBV_DAYS] = QLabel('Number of Observation Days')
        self.labels[MAX_NUM_OBV] = QLabel('Maximum Number of Observation Posts')
        self.labels[RES_DIR] = QLabel('Results Directory')

        self.line_edits[USERNAME] = QLineEdit()
        self.line_edits[USERNAME].setToolTip('[String] Username of Instagram account used for scraping.')
        self.line_edits[USERNAME].setStyleSheet(PADDING_STYLE)
        self.line_edits[PASSWORD] = QLineEdit()
        self.line_edits[PASSWORD].setToolTip('[String] Password of Instagram account used for scraping.')
        self.line_edits[PASSWORD].setStyleSheet(PADDING_STYLE)
        self.line_edits[HASHTAG] = QLineEdit()
        self.line_edits[HASHTAG].setToolTip('[String] Hashtag to scrape from Instagram. Do not include the "#". e.g. sgotterproject')
        self.line_edits[HASHTAG].setStyleSheet(PADDING_STYLE)
        self.line_edits[OBV_DAYS] = QLineEdit()
        self.line_edits[OBV_DAYS].setPlaceholderText('7')
        self.line_edits[OBV_DAYS].setToolTip('[Number] The time period at which posts will be scraped from the day of scraping.')
        self.line_edits[OBV_DAYS].setStyleSheet(PADDING_STYLE)
        self.line_edits[MAX_NUM_OBV] = QLineEdit()
        self.line_edits[MAX_NUM_OBV].setPlaceholderText('30')
        self.line_edits[MAX_NUM_OBV].setToolTip('[Number] The maximum number posts to look at, which is useful for testing and sampling purposes.')
        self.line_edits[MAX_NUM_OBV].setStyleSheet(PADDING_STYLE)
        self.line_edits[RES_DIR] = QLineEdit()
        self.line_edits[RES_DIR].setPlaceholderText('result')
        self.line_edits[RES_DIR].setToolTip('[String] The directory at which the program will download the videos. If the directory does not exist, the program will create it. e.g. results')
        self.line_edits[RES_DIR].setStyleSheet(PADDING_STYLE)

        layout.addWidget(self.labels[USERNAME],                  0, 0, 1, 1)
        layout.addWidget(self.line_edits[USERNAME],         0, 1, 1, 3)

        layout.addWidget(self.labels[PASSWORD],                  1, 0, 1, 1)
        layout.addWidget(self.line_edits[PASSWORD],         1, 1, 1, 3)

        layout.addWidget(self.labels[HASHTAG],                   2, 0, 1, 1)
        layout.addWidget(self.line_edits[HASHTAG],          2, 1, 1, 3)

        layout.addWidget(self.labels[OBV_DAYS],                  3, 0, 1, 1)
        layout.addWidget(self.line_edits[OBV_DAYS],         3, 1, 1, 3)

        layout.addWidget(self.labels[MAX_NUM_OBV],               4, 0, 1, 1)
        layout.addWidget(self.line_edits[MAX_NUM_OBV],      4, 1, 1, 3)

        layout.addWidget(self.labels[RES_DIR],                   5, 0, 1, 1)
        layout.addWidget(self.line_edits[RES_DIR],          5, 1, 1, 3)

        button_scrape = QPushButton('Scrape', clicked=self.scrape)
        layout.addWidget(button_scrape,                     6, 0, 1, 4)

        self.update_text = QLabel('Please fill up form and then click on Scrape')
        layout.addWidget(self.update_text,                  7, 0, 1, 4)

        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)
    
    def check_input(self):
        self.update_text.setText('Checking input')
        for input in inputs:
            if len(self.line_edits[input].text()) == 0:
                self.update_text.setText(f'{self.labels[input].text()} cannot be empty')
                return False
        if not str(self.line_edits[OBV_DAYS].text()).isnumeric():
            self.update_text.setText('The number of observation days must be numeric.')
            return False
        if not str(self.line_edits[MAX_NUM_OBV].text()).isnumeric():
            self.update_text.setText('The maximum number of observation posts must be numeric.')
            return False
        return True

    def scrape(self):
        if self.check_input():
            self.update_text.setText('Logging in.')
            IGDC = IGDataCollection(
                username=self.line_edits[USERNAME].text(), 
                password=self.line_edits[PASSWORD].text(), 
                hashtag=self.line_edits[HASHTAG].text(), 
                num_days_collect=int(self.line_edits[OBV_DAYS].text()), 
                result_dir=self.line_edits[RES_DIR].text())
            self.update_text.setText('Logged in.... Scraping now. Check terminal for logs.')
            IGDC.scrape_data(int(self.line_edits[MAX_NUM_OBV].text()), download=True, save_md=True)
            self.update_text.setText('Done')

def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()


if __name__ == '__main__':
    main()
