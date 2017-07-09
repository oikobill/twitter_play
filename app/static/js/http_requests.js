host = 'http://localhost:5000/'

// make a get http request for hashtag count
// function get_hashtag(url, callback, hashtag)
// {
//     // prepare json file
//     var dict = []
//     dict.push({
//         key:   "hashtag",
//         value: hashtag
//     })
//     var json_dict = JSON.stringify(dict)

//     // make synchronous get request (to do: make it asyncrhonous)
//     var xmlHttp = new XMLHttpRequest();
//     xmlHttp.open( "GET", url, false ); // false for synchronous request
//     xmlHttp.send(json_dict);
//     return xmlHttp.responseText;
// }

// make a post http request for term mentions on tweets count
function start_search_mentions(term)
{    
    var ajax = new XMLHttpRequest();
    ajax.open("GET", host.concat('search_term/'.concat(term.toString())), true);
    ajax.send(null);
    ajax.onreadystatechange = function () {
         if (ajax.readyState == 4 && (ajax.status == 200)) {

            console.log("ready")            
            var Data = JSON.parse(ajax.responseText);
            console.log(Data);
            console.log(Data.status);

        } else {
            console.log("not ready yet")            
        }
    }   
}

// make a get http request for mentions on tweets count
function get_tweet_counts(time_window)
{   
    var ajax = new XMLHttpRequest();
    ajax.open("GET", host.concat('time_plot/'.concat(time_window.toString())), false);
    ajax.send(null);     
    console.log("ready");            
    var Data = JSON.parse(ajax.responseText);
    console.log(Data);
    return Number(Data.data);       
}
