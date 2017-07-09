host = 'http://0.0.0.0:5000/'

// make a get http request for hashtag count
function get_hashtag(url, callback, hashtag)
{
    // prepare json file
    var dict = []
    dict.push({
        key:   "hashtag",
        value: hashtag
    })
    var json_dict = JSON.stringify(dict)

    // make synchronous get request (to do: make it asyncrhonous)
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", url, false ); // false for synchronous request
    xmlHttp.send(json_dict);
    return xmlHttp.responseText;
}

// make a post http request for term mentions on tweets count
function start_search_mentions(term)
{   
    // prepare the request string
    query = '/search_term/'.concat(term.toString())
    url = host.concat(query)

    // make synchronous get request (to do: make it asyncrhonous)
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("POST", url, false); // false for synchronous request

    // parse data
    var data = xmlHttp.responseText;
    var jsonResponse = JSON.parse(data);
    console.log(data['status']);
}

// make a get http request for mentions on tweets count
function get_tweet_counts(time_window)
{   
    // prepare the request string
    query = '/time_plot/'.concat(time_window.toString())
    url = host.concat(query)

    // make synchronous get request (to do: make it asyncrhonous)
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", url, false); // false for synchronous request

    // parse data
    var data = xmlHttp.responseText;
    var jsonResponse = JSON.parse(data);
    console.log(data['status'])
    return data['data'];
}