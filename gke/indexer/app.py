from flask import Flask, render_template, request
from datetime import datetime
import mysql.connector as mysql
import scrape_test
import time
import os

page_ip = str(os.environ.get("PAGEIP"))


database_name = "cloudcomputingpages.page"

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def indexer():
    if request.method == "POST":

        db = mysql.connect(
            host = page_ip,
            user = "root",
            passwd = "QUBccProject"
        )
        url = request.form.get("scraperURL")

        if url == None:
            return "error no url"
            
        date_time_string = datetime.now().strftime("%Y-/%m/%d %H:%M:%S")

        #NEED a try catch here
        try:
            content = scrape_test.get_page_text(url)
            cursor = db.cursor()
            sql = "INSERT INTO "+ database_name + " (uri, indexedat, content) VALUES (%s, %s, %s)"
            values = (url, date_time_string, content)
            cursor.execute(sql, values)
            db.commit()

            page_additional_links = scrape_test.get_links_within_page(url)
            number_of_links = len(page_additional_links)
            #coud just pass url to page then get url back with post request then use that in the next method


            return render_template("additionalCrawl.html", url = url, total_links = number_of_links)
        except :
            return "Error with" + str(url)

    return render_template("index.html")

@app.route('/crawl',  methods=['GET', 'POST'])
def crawl():

    db = mysql.connect(
        host = page_ip,
        user = "root",
        passwd = "QUBccProject"
    )

    if request.method == "POST":
        if request.form.get("exampleCheck1") == None:
            return render_template("error.html")
        else:
            url = request.form.get("exampleCheck1")
            urls_to_scrape = scrape_test.get_links_within_page(url)
            number_of_links = len(urls_to_scrape)

            count_successful_pages = 0
            for list_url in urls_to_scrape:
                date_time_string = datetime.now().strftime("%Y-/%m/%d %H:%M:%S")

                try:
                    content = scrape_test.get_page_text(list_url)
                    time.sleep(5) # 5 second sleep to adhere to best practices
                    
                    #insert into database
                    cursor = db.cursor()
                    sql = "INSERT INTO "+ database_name + " (uri, indexedat, content) VALUES (%s, %s, %s)"
                    values = (list_url, date_time_string, content)
                    cursor.execute(sql, values)
                    db.commit()

                    count_successful_pages = count_successful_pages + 1
                    print(count_successful_pages)
                except :
                    print("Error")

            print(count_successful_pages)

            return render_template("additionalCrawlSuccess.html", url = url, total_links = number_of_links, successful_links = count_successful_pages)
                
    return render_template("error.html")


@app.route('/error')
def error():

    return render_template("error.html")



@app.route('/testscrape')
def test_scrape():

    return render_template("testscrape.html")

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))