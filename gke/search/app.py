from flask import Flask, render_template, request
app = Flask(__name__)
from search_result import Search_result, Advert, sorted_ranked_results
import mysql.connector as mysql
import os

advert_ip =  str(os.environ.get("ADVERTIP"))

page_ip = str(os.environ.get("PAGEIP"))

advert_database = "cloudcomputingadverts.advert"
pages_database = "cloudcomputingpages.page"

#No ranking part yet
@app.route('/')
def use_db():

    db_advert = mysql.connect(
        host = advert_ip,
        user = "root",
        passwd = "QUBccProject"
    )

    db_page = mysql.connect(
        host = page_ip,
        user = "root",
        passwd = "QUBccProject"
    )

    query_string = request.args.get("q")
    print(query_string)

   
    query_words = query_string.split() if query_string else [""]
    #query_words = query_string.split() # splits on " " blank spaces

    #db stuff
    #--------------------------------
    cursor_advert = db_advert.cursor()

    #could pull each db serach out into a method or something to make this nicer

    #will find all values so will it give duplicates?
    #####################
    # NOT A CHALLENGE ABOUT MOST EFFECTIVE SEARCH ALGORITHMS
    #####################
    # (THis works but it aint pretty)

    advert_query = "SELECT * FROM " + advert_database + " WHERE keyword LIKE '%" + query_words[0] + "%'"
    for word in query_words[1:]:
        advert_query = advert_query + " OR keyword LIKE '%" + word + "%'"

    #just uses the first word of the search term for the time being
    #advert_query = "SELECT * FROM cloudcomputing.advert WHERE keyword LIKE '%" + query_words[0] + "%';" #single wrd for now but will need to update to work with multiword query stings
    cursor_advert.execute(advert_query)
    adverts = cursor_advert.fetchall()
    print("Length of adverts: " + str(len(adverts)))

    advert_list = []
    for advert in adverts:
        new_advert = Advert("#", advert[2])
        advert_list.append(new_advert)

    #If adverts list comes back empty give a generic advert
    #Could do this on frontend bit but i think its better done here
    advert_list = advert_list if advert_list else [Advert("#", "Click here you've Won")]
    #-----------------------------------------------------------
    print("Length of adverts list: " + str(len(advert_list)))
    #################################
    #Results QUERY
    #gets all results that have any of the words

    cursor_page = db_page.cursor()

    page_query = "SELECT * FROM "+ pages_database +" WHERE content LIKE '%" + query_words[0] + "%'"
    if len(query_words) > 1:
        for word in query_words[1:]:
            page_query = page_query + " OR content LIKE '%" + word + "%'"

    #page_query = "SELECT * FROM cloudcomputing.page WHERE content LIKE '%" + query_string + "%';"
    cursor_page.execute(page_query)
    pages = cursor_page.fetchall()
    #####################################
    

    #RANKING PART
    if pages:
        pages = sorted_ranked_results(pages, query_words)
    
    result_list = []
    for item in pages:
        #index 1 is url and index3 is body text and only get the first 150 characters
        result = Search_result(item[1], item[3][0:150])
        result_list.append(result)
    
    #end db stuff

    search_term = query_string if query_string else "Search"

    return render_template("index.html", results = result_list, search_term = search_term, adverts = advert_list)


# @app.route('/')
# def hello_world():
#     return 'Hello, World!'

# @app.route('/template')
# def template_test():

#     query_string = request.args.get("q")

#     #Would do db stuff here
#     # Something like: SELECT * FROM table  WHERE column LIKE '%word1%' or column LIKE '%word2%' or column LIKE '%word3%' ...
#     # so before this would need to get and split words from the query string in order to make the SQL statement correctly 
#     # probably a better way to do it than using LIKE with wildcards but this should work for the basic synario 

#     result_list = []
#     result = Search_result("https://getbootstrap.com/docs/4.4/layout/grid/", "Bootstrap layout info")
#     result_list.append(result)
#     result_list.append(result)

#     for i in range(100):
#         result_list.append(result)

#     #QOL change to the placehold of the search bar if a serach has been done
#     search_term = query_string if query_string else "Search"

#     return render_template("index.html", results = result_list, search_term = search_term, advert = "Hello Advert")



if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))