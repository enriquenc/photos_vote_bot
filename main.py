import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("PhotosVoteBot-b287f9a46ce7.json", scope)

client = gspread.authorize(creds)

sheet = client.open("photos_vote_bot").sheet1

data = sheet.get_all_records()

i = 0

sheet.update_cell(2,2, i + 1)
i = sheet.cell(2,2).value
sheet.update_cell(2,2, int(i) + 2)

pprint(data[1]['ФИО'])