class Search_result:
    def __init__(self, link, content):
        self.link = link
        self.content = content

class Advert:
    def __init__(self, link, content):
        self.link = link
        self.content = content



def sorted_ranked_results(unranked_results, search_words):
    #converting list of tuples to list of lists 
    results = [list(elem) for elem in unranked_results]

    for result in results:
        score = 0
        for word in search_words:
            score =  score + result[3].count(word)

        result.append(score)

    #with the new score field sort the values based on the (i.e. those with the highest scre are first in the list)
    # so they will be the first displayed on the page
    results = sorted(results, key=lambda x: x[4], reverse=True)
    return results
