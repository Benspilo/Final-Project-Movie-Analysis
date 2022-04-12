print("hello world")

'''
def get_movie_data(title):
    endpoint='https://www.omdbapi.com/'
    param = {}
    param['t'] = title
    param['r'] = 'json'
    this_page_cache = requests_with_caching.get(endpoint, params=param)
    return json.loads(this_page_cache.text)

    *
    No Api key was needed for this but for imbd we use 
    param[documentation for api key] = our api key
    then we can do requests or requests with caching (makes no difference here)
    and add params as shown above. 
'''
