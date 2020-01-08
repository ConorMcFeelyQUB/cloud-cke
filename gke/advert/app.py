from flask import Flask, render_template, request, make_response
import mysql.connector as mysql
import os
import json
app = Flask(__name__)

advert_ip = str(os.environ.get("ADVERTIP"))

database_name = "cloudcomputingadverts.advert"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":

        db = mysql.connect(
            host = advert_ip,
            user = "root",
            passwd = "QUBccProject"
        )


        error = False

        advert_content = request.form["advertContent"]
        advert_URL = request.form["advertURL"]
        advert_keywords = request.form["advertKeywords"].split(" ")[0]
        
        print(advert_keywords)
        print(len(advert_keywords))
        if(advert_content == None or len(advert_content) < 1 or advert_keywords == None or len(advert_keywords) < 1):
            error = True
            return render_template("advertResult.html", error = error, content = "", keywords = "", URL = "")

        #if url was provided keep it as is else just put in a # to make links nice in search section
        advert_URL = advert_URL if advert_URL else "#"

        cursor = db.cursor()
        sql = "INSERT INTO "+ database_name + " (keyword, advert, url) VALUES (%s, %s, %s)"
        values = (advert_keywords, advert_content, advert_URL)
        cursor.execute(sql, values)
        db.commit()
        
        return render_template("advertResult.html", error = error, content = advert_content, keywords = advert_keywords, URL = advert_URL)

    return render_template("index.html")


@app.route('/advertid')
def getadvertid():

    db = mysql.connect(
        host = advert_ip,
        user = "root",
        passwd = "QUBccProject"
    )

    query_string = request.args.get("id")
    print(query_string)

    if(str(query_string).isdigit()):
        cursor = db.cursor()
        sql_query = "SELECT * FROM " + database_name + " WHERE advertid=" + str(query_string)
        cursor.execute(sql_query)
        advert = cursor.fetchall()
        print(advert)

        if(advert):
            advert = advert[0]

            advert_id = advert[0]
            advert_content = advert[2]
            advert_keyword = advert[1]
            advert_url = advert[3]

            dictionary_advert = {
                "id":advert_id,
                "content":advert_content,
                "keywords":advert_keyword,
                "url":advert_url
            }

            json_object = json.dumps(dictionary_advert)
            resp = make_response(json_object)
            resp.headers['Access-Control-Allow-Origin'] = '*'
            resp.headers['Content-Type'] = 'application/json'
            return(resp)
        else:
            return "no such advert"
        
    return "invalid id"


@app.route('/advertkeyword')
def getadvertkeyword():

    db = mysql.connect(
        host = advert_ip,
        user = "root",
        passwd = "QUBccProject"
    )

    query_string = request.args.get("keyword")
    print(query_string)

    if(query_string):
        cursor = db.cursor()
        sql_query = "SELECT * FROM " + database_name + " WHERE keyword=" +  "'" + str(query_string) + "'"
        print()
        cursor.execute(sql_query)
        advert = cursor.fetchall()
        print(advert)

        if(advert):
            advert = advert[0]

            advert_id = advert[0]
            advert_content = advert[2]
            advert_keyword = advert[1]
            advert_url = advert[3]

            dictionary_advert = {
                "id":advert_id,
                "content":advert_content,
                "keywords":advert_keyword,
                "url":advert_url
            }

            json_object = json.dumps(dictionary_advert)
            resp = make_response(json_object)
            resp.headers['Access-Control-Allow-Origin'] = '*'
            resp.headers['Content-Type'] = 'application/json'
            return(resp)
        else:
            return "no such advert"
        
    return "invalid id"



@app.route('/test')
def test():

    db = mysql.connect(
        host = advert_ip,
        user = "root",
        passwd = "QUBccProject"
    )


    cursor = db.cursor()
    sql = "SELECT * FROM " + database_name +";"
    cursor.execute(sql)
    adverts = cursor.fetchall()

    return str(len(adverts))

@app.route('/new')
def new():
    osvar = os.environ.get("TESTTT")
    if osvar == None:
        return "Was none"
    else:
        return str(osvar)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
