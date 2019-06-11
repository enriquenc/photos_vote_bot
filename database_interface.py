import pymysql
from time import gmtime, strftime
import pprint

f = open('database_authorization', 'r')
database_info = f.read().splitlines()
f.close()
conn = pymysql.connect(host=database_info[0],
                       user=database_info[1],
                       passwd=database_info[2],
                       db=database_info[3])
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
    try:
        cursor.execute("INSERT into votes (id) values (" + id + ")")
        conn.commit()
    except Exception as msg:
        print("new_user: " + id + ", error: " + str(msg))


def vote(id, place, participants_number):
    try:
        cursor.execute("update votes SET " + places[place] + " = " + str(participants_number) + " WHERE id = " + id)
        conn.commit()
    except Exception as msg:
        print(strftime("[%a, %d %b %Y %H:%M:%S]", gmtime(2)) + str(participants_number) + " participant number is " + str(place) + ' place error: ' + str(msg))

def count_votes(sheet):
    global conn
    global cursor

    try:
        sheet.null()
        #p_count = len(sheet.get_participants())
        #result = [[None]] * p_count
        #print(result)
        cursor.execute('SELECT id, first_place, second_place, third_place FROM votes')
    #pprint.pprint(cursor.fetchall())
        for id, first_place, second_place, third_place in cursor:
            #print('id: %d\n1place: %d\n2place: %d\n3place: %d\n' % (id, first_place, second_place, third_place))
            sheet.vote(1, first_place)
            sheet.vote(2, second_place)
            sheet.vote(3, third_place)
    except Exception as msg:
        conn = pymysql.connect(host=database_info[0],
                               user=database_info[1],
                               passwd=database_info[2],
                               db=database_info[3])
        cursor = conn.cursor()

        f = open('errors', 'a+')
        f.write(strftime("[%a, %d %b %Y %H:%M:%S]", gmtime(2)) + ': count_votes: ' + str(msg) + '\n')
        f.close()
        return False
    return True



if __name__ == '__main__':
    cursor.execute("SELECT * from votes")
    #cursor.execute("delete from votes")
    #conn.commit()
    print(cursor.fetchall())