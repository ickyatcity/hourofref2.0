import csv
import wikipedia 
from pymongo import MongoClient
# def news_sources_latest(extsource,lenx):

#   for i in xrange(lenx):
#       sourcepart = extsource["sources"][i]['id']
#       sortby = "latest"
#       stringBuild = "https://newsapi.org/v1/articles" +"?" +"source=" + sourcepart + "&" + "sortBy" + "=latest" + "&"+ 'apiKey' + '=' + api_key 
#       # print stringBuild 
#       source_latest = requests.get(stringBuild)
#       source_latest_tx = json.loads(source_latest.text)
#       databasepost_latest(source_latest_tx,sourcepart)


def get_db():
    client = MongoClient('localhost:27017')
    db = client.wikipedia_candidates
    return db


def read_csv():
	csvlist =[]
	with open('candidates.csv') as csvDataFile:
	    csvReader = csv.reader(csvDataFile)
	    for row in csvReader:
	        csvlist.append(row)
	        print csvlist
        return csvlist  

def read_wikipedia(csvList, db):
     print csvList[0]
     for link in csvList[0]:
        try:
            #try to load the wikipedia page
            page=wikipedia.page(link, auto_suggest=False)
            print page.url, 'writing.. '
            candid =link
            candidateSlug = candid.replace(' ', '')
            db.page_url.insert({"candiate_name":link, "url_wiki":page.url})
            db.page_title.insert({"candiate_name":link, "title_wiki":page.title})
            db.page_content.insert({"candiate_name":link, "content_wiki":page.content})
            db.page_images.insert({"candiate_name":link, "images_wiki":page.images})
            db.page_references.insert({"candiate_name":link, "references_wiki":page.references})
            db.page_links.insert({"candiate_name":link, "links_wiki":page.links})
            db.page_sections.insert({"candiate_name":link, "html_sections":page.sections})
            db.page_summary.insert({"candiate_name":link, "html_sections":page.summary})
            db.PageAllCandidates.insert({"candiate_name":link, "url_wiki":page.url, "title_wiki":page.title, "content_wiki": page.content, "reference_wiki":page.references, "candidate_slug":candidateSlug})
            db.page_all.insert({"candiate_name":link, "url_wiki":page.url, "title_wiki":page.title, "content_wiki": page.content, "reference_wiki":page.references})
            db.page_rec.insert({"candiate_name":link, "url_wiki":page.url, "title_wiki":page.title, "content_wiki": page.content, "reference_wiki":page.references, "candidate_slug":candidateSlug})
        except wikipedia.exceptions.PageError:
            #if a "PageError" was raised, ignore it and continue to next link
            continue

if __name__ == "__main__":
    db = get_db()
    csvval = read_csv()
    read_wikipedia(csvval, db)

