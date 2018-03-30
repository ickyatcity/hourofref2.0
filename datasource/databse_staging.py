import os
import sqlite3
import time




def connect(sqlite_file):
    """ Make connection to an SQLite database file """
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    return conn, c


def close(conn):
    """ Commit changes and close connection to the database """
    conn.commit()
    conn.close()


def createDatabase_source_latest(c, conn):
    try:
        conn.execute('''CREATE TABLE News_sources_latest
            (ID            INT      NOT NULL,
            author         TEXT     NOT NULL,
            title          TEXT     NOT NULL,
            description    TEXT     NOT NULL,
            url             TEXT     NOT NULL,
            urlToImage      TEXT     NOT NULL,
            publishedAt     TEXT     NOT NULL, 
            PKEY            TEXT     primary key NOT NULL);''')

        print "Table created successfully";


        conn.close()
        dbcreateflag = 0

    except sqlite3.Error as er:
        print 'database already availble:', er.message
        dbcreateflag = 1
    return dbcreateflag


def comitetoDatabase_latest(c, conn, table_name, dataexport, dbcreateflag,sourcepart):
    lenx = len(dataexport['articles']) 
    p = c.execute('SELECT max(ID) FROM {}'.format(table_name))
    maxid = p.fetchone()[0]

    if dbcreateflag == 0:
        maxid = 0

    for i in xrange(lenx):
        validid = i
        author = dataexport['articles'][i]['author']
        title = dataexport['articles'][i]['title']
        description = dataexport['articles'][i]['description']
        url = dataexport['articles'][i]['url']
        urltoimage = dataexport['articles'][i]['urlToImage']
        publishedAt = dataexport['articles'][i]['publishedAt']


        try:
            PKEY = str(sourcepart) + str(publishedAt) + str(author) 

        except ValueError:
            print("Oops!  That was no valid number.  Try again...")   

        # print 'writing to database'
        c.execute("INSERT OR IGNORE into News_sources_latest  values (?, ?,?,?,?,?,?,?)", (validid, author, title, description, url, urltoimage,publishedAt, PKEY))


        # c.execute("insert into API_Store  values (?, ?,?,?)", (valf + maxid + 1, titlea, linka, texta))


def databasepost_latest(dataexport,sourcepart):

        if 'articles' in dataexport:
            sqlite_file = '/Users/siyanetissera/development/project_four/projectNews/db.sqlite3'
            conn, c = connect(sqlite_file)
            table_name = "News_sources_latest"
            print 'about to write to database-----'
            dbcreateflag = createDatabase_source_latest(c, conn)
            comitetoDatabase_latest(c, conn, table_name, dataexport, dbcreateflag,sourcepart)
            close(conn)

        else:
            print "articles key not available"


