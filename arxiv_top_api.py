'''
By - Neel Shah
On - March/2017

'''
import falcon
import json
import urllib.request
import feedparser

# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class ArxivLatest(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200  # This is the default status
        search_for = int(req.params['num'])
        result_json = {}
        # Base api query url
        base_url = 'http://export.arxiv.org/api/query?';
        # Search parameters
        search_query = 'cat:cs.CV+OR+cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CL+OR+cat:cs.NE+OR+cat:stat.ML' # search for CV,CL,AI,LG,NE,ML field papers
        start = 0
        # retreive the first 1000 results
        max_results = search_for
        count = 0
        fail_count = 0
        while start < search_for:
            #time.sleep(5)
            query = 'search_query=%s&start=%i&max_results=%i&sortBy=lastUpdatedDate&sortOrder=descending' % (search_query,start,max_results)
            start = start + search_for
            # Opensearch metadata such as totalResults, startIndex,
            # and itemsPerPage live in the opensearch namespase.
            # Some entry metadata lives in the arXiv namespace.
            # This is a hack to expose both of these namespaces in
            # feedparser v4.1
            feedparser._FeedParserMixin.namespaces['http://a9.com/-/spec/opensearch/1.1/'] = 'opensearch'
            feedparser._FeedParserMixin.namespaces['http://arxiv.org/schemas/atom'] = 'arxiv'
            # perform a GET request using the base_url and query
            response = urllib.request.urlopen(base_url+query).read()
            # parse the response using feedparser
            feed = feedparser.parse(response)
            # print opensearch metadata
            # print('totalResults for this query: %s' % feed.feed.opensearch_totalresults)
            # print('itemsPerPage for this query: %s' % feed.feed.opensearch_itemsperpage)
            # print('startIndex for this query: %s'   % feed.feed.opensearch_startindex)
            x = 1
            ans = 'paper'
            final_str = ''
            # Run through each entry, and print out information
            for entry in feed.entries:

                # print('Published: %s' % entry.published)
                # print('Title:  %s' % entry.title)
                p_date = str(entry.published)
                title = str(entry.title)
                f_title = title.replace("\\n","")
                # feedparser v5.0.1 correctly handles multiple authors, print them all
                # feedparser v4.0 don't support for muliple authors handling
                try:
                    old_author_list = ', '.join(author.name for author in entry.authors)
                    new_author_list = old_author_list.replace("'","")
                    #print('Authors:  %s' % ', '.join(author.name for author in entry.authors))
                    #print(new_author_list)
                except AttributeError:
                    pass
                final_str = final_str+title+' <break time="500ms"/> '+' By '+new_author_list+' <break time="1500ms"/> '
                x += 1

            result_json[ans]=final_str

        resp.body = json.dumps(result_json)

# falcon.API instances are callable WSGI apps
app = falcon.API()
# things will handle all requests to the '/things' URL path
app.add_route('/submit', ArxivLatest())
