import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='photos_vote_bot')
cursor = conn.cursor()

places = {
    1: 'first_place',
    2: 'second_place',
    3: 'third_place'
}


def check_vote(id, place):
    cursor.execute("SELECT " + places[place] + " FROM votes WHERE id = " + id)
    result = cursor.fetchall()
    return result[0][0]


def vote(id, place, participants_number):
    cursor.execute("update votes SET " + places[place] + " = " + str(participants_number) + " WHERE id = " + id)
    conn.commit()


#print(check_vote('421421421', 1))
#vote('421421421', 1, 7)
#conn.commit()
#print(cursor.fetchall())
