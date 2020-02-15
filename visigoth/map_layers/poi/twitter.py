import base64

twitter_template = """<div id="tweet" tweetID="%s"></div>

<script sync="sync" src="https://platform.twitter.com/widgets.js"></script>

<script>

  window.onload = (function(){

    var tweet = document.getElementById("tweet");
    var id = tweet.getAttribute("tweetID");

    twttr.widgets.createTweet(id, tweet);
  });

</script>"""

iframe_template = """
<iframe height="95%s" width="95%s" src="%s"></iframe>
"""

def encodeTweet(tweet_id):
    url = 'data:text/html;charset=utf-8;base64,'+str(base64.b64encode(bytes(twitter_template%(tweet_id),"utf-8")),"utf-8")
    return iframe_template%("%","%",url)