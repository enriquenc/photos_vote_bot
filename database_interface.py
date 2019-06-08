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
    if result is ():
        return None
    return result[0][0]


def new_user(id):
    cursor.execute("INSERT into votes (id) values (" + id + ")")
    conn.commit()


def vote(id, place, participants_number):
    cursor.execute("update votes SET " + places[place] + " = " + str(participants_number) + " WHERE id = " + id)
    conn.commit()


if __name__ == '__main__':
    cursor.execute("SELECT * from votes")
    print(cursor.fetchall())