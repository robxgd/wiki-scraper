from dotenv import load_dotenv
from atlassian import Confluence # See https://atlassian-python-api.readthedocs.io/index.html
import os

load_dotenv()

def get_url():
    return os.environ["confluence-url"]


def connect_to_Confluence():

    url = get_url()
    username = os.environ["confluence-username"]
    password = os.environ["confluence-api-token"]
    confluence = Confluence(
        url=url,
        # username=username,
        # password=password,
        token=password,
        cloud=True)
    
    return confluence
  

def get_all_pages(confluence, space):
    print("get_all_pages")
    '''
    Get all the pages within the MY-SPACE space.
    
    Parameters
    ----------
    confluence: a connector to Confluence
    space: Space of the Confluence (i.e. 'MY-SPACE')
    
    Return
    ------
    List of page objects. Each page object has all the information concerning
    a Confluence page (title, body, etc)
    '''
    
    # There is a limit of how many pages we can retrieve one at a time
    # so we retrieve 100 at a time and loop until we know we retrieved all of
    # them.
    keep_going = True
    start = 0
    limit = 100
    pages = []
    while keep_going:
        print("Retrieving pages from "+str(start)+" to "+str(start+limit))
        results = confluence.get_all_pages_from_space(space, start=start, limit=100, status=None, expand='body.storage', content_type='page')
        pages.extend(results)
        if len(results) < limit:
            keep_going = False
        else:
            start = start + limit
    return pages
  


def save_pages(pages):

    for page in pages:
        title = page['title']
        htmlbody = page['body']['storage']['value']
        # people use different characters in the title that are not valid for filenames
        parsed_title = title.replace(" ", "_").replace("/", "-").replace(">","_").replace("?","").replace(":","_").replace("<","_").replace("*","_").replace("|","_").replace('"',"_"	).replace("\\","_").replace(".","_").replace("(","_").replace(")","_").replace("[","_").replace("]","_").replace("{","_").replace("}","_").replace(",","_").replace(";","_").replace("=","_").replace("&","_").replace("^","_").replace("%","_").replace("$","_").replace("#","_").replace("@","_")
        # htmlParse = BeautifulSoup(htmlbody, 'html.parser')
        body = []
     
        try:
            f = open("pages/"+parsed_title+".html", "w", encoding="utf-8")
            f.write(htmlbody)
            f.close()

        
        except:
            print("could not save: "+parsed_title)
    return True

def main():
    confluence = connect_to_Confluence()
    space = os.environ["confluence-space"]
    pages = get_all_pages(confluence, space)
    # print(pages)
    save_pages(pages)

if __name__ == '__main__':
    main()
