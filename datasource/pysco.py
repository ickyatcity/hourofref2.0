#!/usr/bin/python
import psycopg2
import csv
from config import config
import wikipedia 
import datetime
# from datetime import datetime
import time


def read_csv():
    csvlist =[]
    with open('candidates.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            csvlist.append(row)
            print (csvlist)
        return csvlist  



def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
 
        # create a cursor
        cur = conn.cursor()
        
 # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
 
        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
       
     # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
 


def create_tables_wiki():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE vendorsp (
            vendor_id SERIAL PRIMARY KEY,
            vendor_name VARCHAR(255) NOT NULL
        )
        """,
        """
        CREATE TABLE candidates_wiki (
          candidate_id SERIAL PRIMARY KEY,
          candiate_name VARCHAR(255) NOT NULL,
          url_wiki VARCHAR(255),
          title_wiki VARCHAR(255) ,
          content_wiki TEXT ,
          images_wiki TEXT, 
          references_wiki TEXT,
          links_wiki TEXT, 
          sections_wiki TEXT,
          summary_wiki TEXT,
          fecha_ini_det TIMESTAMP,
          fecha_ini_f DATE,
          score Int, 
          score_up Int, 
          score_down Int, 
          slug VARCHAR(60),
          users TEXT
        )
       """
        )
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()




# stuff_in_string = "Shepherd {} is {} years old.".format(shepherd, age)
    # sql = """INSERT INTO vendors(vendor_name) VALUES(%s) RETURNING vendor_id;"""
   # sql = """INSERT INTO vendors(vendor_name)
   #           VALUES(%s) RETURNING vendor_id;"""

        # db.page_url.insert({"candiate_name":link, "url_wiki":page.url})
        #     db.page_title.insert({"candiate_name":link, "title_wiki":page.title})
        #     db.page_content.insert({"candiate_name":link, "content_wiki":page.content})
        #     db.page_images.insert({"candiate_name":link, "images_wiki":page.images})
        #     db.page_references.insert({"candiate_name":link, "references_wiki":page.references})
        #     db.page_links.insert({"candiate_name":link, "links_wiki":page.links})
        #     db.page_sections.insert({"candiate_name":link, "html_sections":page.sections})
        #     db.page_summary.insert({"candiate_name":link, "html_sections":page.summary})


# curs.execute("INSERT INTO sometable (col1, col2) VALUES (%s, %s)", (var1,var2))
     # sql = "INSERT INTO candidates_wiki ({}) VALUES({}) RETURNING candidate_id;".format(field, page_val)
     # sql = str(sql)


def insert_records_wiki(link, page):
     params = config()
     conn = psycopg2.connect(**params)
     cur = conn.cursor()

     # time - calculation 
     ts = time.time()
     st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

     # date - calculation 
     today = datetime.date.today()
     score = 0
     score_up = 0
     score_down = 0

     # summary to display at search 
     # summary_wiki = page.summary


     # slug
     candid =link
     slug = candid.replace(' ', '')
     conn = None
     users = 'admin'

     # vendor_id = None
     try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute("""INSERT INTO candidates_wiki(candiate_name, 
            url_wiki, title_wiki, content_wiki, images_wiki, references_wiki, 
            links_wiki,sections_wiki, summary_wiki, fecha_ini_det, fecha_ini_f, score, score_up, score_down, slug, users) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)""",
            (link, page.url, page.title, page.content, page.images, page.references, page.links, page.sections, page.summary, st, today, score, score_up, score_down, slug, users))

        # cur.execute(sql)
        # get the generated id back
        # candidate_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
     except (Exception, psycopg2.DatabaseError) as error:
        print(error)
     finally:
        if conn is not None:
            conn.close()
 
     # return candidate_id

def candidaterun(csvList):

        for cand_name in csvList[0]:
            # field_list = ["candidate_id", "candiate_name", "url_wiki", "title_wiki", "content_wiki", "images_wiki", "references_wiki","links_wiki", "sections_wiki", "summary_wiki"]
            try:
                page=wikipedia.page(cand_name, auto_suggest=False)
                # for field in field_list:
                insert_records_wiki(cand_name, page)
                print ("Still writing....")

            except wikipedia.exceptions.PageError:
                #if a "PageError" was raised, ignore it and continue to next link
                continue
      

if __name__ == '__main__':
    # create_tables_wiki()
    csvval = read_csv()
    candidaterun(csvval)



