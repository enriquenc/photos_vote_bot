import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint


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

    def vote(self, number, place):
        votes_number = self.sheet.cell(number + 1, place + 2).value
        self.sheet.update_cell(number + 1, place + 2, int(votes_number) + 1)

    def unvote(self, number, place):
        votes_number = self.sheet.cell(number + 1, place + 2).value
        self.sheet.update_cell(number + 1, place + 2, int(votes_number) - 1)

    def null(self):
        data = self.sheet.get_all_values()
        for row in range(2, len(data) +1):
            self.sheet.update_cell(row, 3, 0)
            self.sheet.update_cell(row, 4, 0)
            self.sheet.update_cell(row, 5, 0)
        #pprint(data)
        #print(len(data))

    def get_participants(self):
        return self.sheet.col_values(2)[1:]

#s = Sheet()
#print(s.get_participants())

#i = 0

#sheet.update_cell(2,2, i + 1)
#i = sheet.cell(2,2).value
#sheet.update_cell(2,2, int(i) + 2)

#pprint(data[1]['ФИО'])