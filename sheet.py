import gspread
from oauth2client.service_account import ServiceAccountCredentials
from database_interface import *
from time import gmtime, strftime
import time


class Sheet:
    def __init__(self, name):
        self.scope = ["https://spreadsheets.google.com/feeds",
                    "https://www.googleapis.com/auth/spreadsheets",
                    "https://www.googleapis.com/auth/drive.file",
                    "https://www.googleapis.com/auth/drive"]

        self.creds = ServiceAccountCredentials.\
            from_json_keyfile_name("PhotosVoteBot-b287f9a46ce7.json", self.scope)
        self.client = gspread.authorize(self.creds)
        self.sheet = self.client.open(name).sheet1

    def vote(self, number, place, votes_number):
        if number == 0:
            return
        self.sheet.update_cell(number + 1, place + 2, votes_number)
        #vote(user_id, place, number)

    def unvote(self, place, number):
        votes_number = int(self.sheet.cell(number + 1, place + 2).value)
        self.sheet.update_cell(number + 1, place + 2, votes_number - 1)

    def null(self):
        data = self.sheet.col_values(1)
        for row in range(2, len(data)):
            self.sheet.update_cell(row, 3, 0)
            self.sheet.update_cell(row, 4, 0)
            self.sheet.update_cell(row, 5, 0)
        #pprint(data)
        #print(len(data))

    def get_participants(self):
        return self.sheet.col_values(1)[1:]

