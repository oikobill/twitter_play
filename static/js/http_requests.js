// make a get http requests
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
    vvar xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send(json_dict);
    return xmlHttp.responseText;
}