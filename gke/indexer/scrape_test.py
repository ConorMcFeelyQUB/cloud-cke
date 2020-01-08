import bs4
import requests

def get_page_text(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    body = soup.find("body")

    #removing script tags from the document body
    unwanted_script = body.find_all("script")
    for script in unwanted_script:
        script.extract()

    unwanted_style = body.find_all("style")
    for style in unwanted_style:
        style.extract()

    page_text = body.text
    return page_text

#has ability to "crawl" to other "adjecent" pages
def get_links_within_page(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    body = soup.find("body")
    
    a_tags = body.find_all('a', href=True)
    links = []
    base_url = url
    for atag in a_tags:
        page_url = atag["href"]

        if atag["href"].startswith("//"):
            page_url = "https:" + page_url
        elif atag["href"].startswith("/"):
            #split url and get the start (should work afaik and can tell)
            page_url = "https://" + url.split("/")[2] + atag["href"]
        elif not atag["href"].startswith("http"):
            page_url = base_url + atag["href"]
        
        links.append(page_url)

    return links
