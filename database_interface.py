import pymysql
from time import gmtime, strftime
import pprint

f = open('database_authorization', 'r')
database_info = f.read().splitlines()
f.close()

places = {
    1: 'first_place',
    2: 'second_place',
    3: 'third_place'
}


def check_vote(id, place):
    conn = pymysql.connect(host=database_info[0],
                           user=database_info[1],
                           passwd=database_info[2],
                           db=database_info[3])
    cursor = conn.cursor()

    cursor.execute("SELECT " + places[place] + " FROM votes WHERE id = " + id)
    result = cursor.fetchall()
    if result is ():
        return None
    return result[0][0]


def new_user(id):
    conn = pymysql.connect(host=database_info[0],
                           user=database_info[1],
                           passwd=database_info[2],
                           db=database_info[3])
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT into votes (id) values (" + id + ")")
        conn.commit()
    except Exception as msg:
        cursor.execute("delete from votes where id = " + id)
        print("new_user: " + id + ", error: " + str(msg))
        return False
    return True


def vote(id, place, participants_number):
    conn = pymysql.connect(host=database_info[0],
                           user=database_info[1],
                           passwd=database_info[2],
                           db=database_info[3])
    cursor = conn.cursor()

    try:
        cursor.execute("update votes SET " + places[place] + " = " + str(participants_number) + " WHERE id = " + id)
        conn.commit()
    except Exception as msg:
        print(strftime("[%a, %d %b %Y %H:%M:%S]", gmtime(2)) + str(participants_number) + " participant number is " + str(place) + ' place error: ' + str(msg))


def count_votes(sheet, participants):
    conn = pymysql.connect(host=database_info[0],
                           user=database_info[1],
                           passwd=database_info[2],
                           db=database_info[3])
    cursor = conn.cursor()

    try:
        sheet.null()
        result = []
        for i in range(len(participants)):
            result.append(
                {
                    'first_place': 0,
                    'second_place': 0,
                    'third_place': 0
                }
            )
        cursor.execute('SELECT id, first_place, second_place, third_place FROM votes')
    #pprint.pprint(cursor.fetchall())
        for id, first_place, second_place, third_place in cursor:
            #print('id: %d\n1place: %d\n2place: %d\n3place: %d\n' % (id, first_place, second_place, third_place))
            result[first_place - 1]['first_place'] = result[first_place - 1]['first_place'] + 1
            result[second_place - 1]['second_place'] = result[second_place - 1]['second_place'] + 1
            result[third_place - 1]['third_place'] = result[third_place - 1]['third_place'] + 1

        sheet.null()
        for i in range(len(result)):
            sheet.vote(i + 1, 1, result[i]['first_place'])
            sheet.vote(i + 1, 2, result[i]['second_place'])
            sheet.vote(i + 1, 3, result[i]['third_place'])

    except Exception as msg:
        f = open('errors', 'a+')
        f.write(strftime("[%a, %d %b %Y %H:%M:%S]", gmtime(2)) + ': count_votes: ' + str(msg) + '\n')
        f.close()
        return False
    return True


def free():
    conn = pymysql.connect(host=database_info[0],
                           user=database_info[1],
                           passwd=database_info[2],
                           db=database_info[3])
    cursor = conn.cursor()

    cursor.execute("DELETE from votes")
    conn.commit()




if __name__ == '__main__':

    conn = pymysql.connect(host=database_info[0],
                           user=database_info[1],
                           passwd=database_info[2],
                           db=database_info[3])
    cursor = conn.cursor()

    cursor.execute("SELECT * from votes")
    #cursor.execute("delete from votes")
    #conn.commit()
    print(cursor.fetchall())