#!flask/bin/python
# -*- coding: utf-8 -*-
"""
Requierments:
Python 2.7.x
pip install lxml-3.8.0 
pip install requests
pip install flask
pip install flask-httpauth

Description:

This program uses Yelp"s Fusion API to:
(1) Query for a specific business --->>> GET https://api.yelp.com/v3/businesses/search
    using the criteira: "categories", "location", "name" in the query string, and 
(2) Once the page url is extracted for a business, scrape the reivews and ratings for 
    that specific business
(3) Query for a set number of business reviews using the passed value in "reviews" 

For Detail API Documentation, please reference --->>> https://www.yelp.com/developers/documentation/v3

Sample usage of the program, but running at the command line --->>>
python get-yelp-reviews-v7.py --categories="pizza" --location="New York, NY" --name="Patsys Pizzeria" --reviews="5"

Alternatively, run without input ( hard-coded default values will take over... ), as such --->>>
python get-yelp-reviews.py

SAMPLE/ACTUAL YELP BUSINESS for PIZZA and NEW YORK, NY ( pick one )
    Juliana's Pizza, Prince Street Pizza, Lombardi's , L'industrie Pizzeria
    Patzeria Perfect Pizza, My Pie, Joe's Pizza, NY Pizza Suprema
    B Side Pizza & Wine Bar, Adrienne's Pizzabar, La Margarita Pizza
    Rubirosa, Stage Door Pizza, Patsys Pizzeria, Paulie Gee's
    Sottocasa Pizzeria- Boerum Hill, Barboncino Pizza & Bar, Joe's Pizza
    PN Wood Fired Pizza, B Squared
"""
from __future__ import print_function

#import json
import pprint
import requests
import sys
import string
import urllib

from flask import Flask, request, jsonify
from flask import abort, make_response, url_for

from flask.ext.httpauth import HTTPBasicAuth

from lxml import html
from urllib import quote, urlencode
from urllib2 import HTTPError


# Before accessing the Fuse API end-point, you must creat an 
# app and credentials.  Please go to the following link, and when
# you have them plug them in below, before attempting to run 
# the code --->>> https://www.yelp.com/developers/v3/manage_app
CLIENT_ID = 'insert-creds-here'
CLIENT_SECRET = 'insert-creds-here'

# API constants for YELP's API
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come AFTER slash.
REVIEWS_PATH = '/reviews'  # Business ID will come BEFORE slash.
TOKEN_PATH = '/oauth2/token'
GRANT_TYPE = 'client_credentials'

# DEFAULT search categories if none are provided by the User.
DEFAULT_CATEGORIES = 'pizza'
DEFAULT_LOCATION = 'New York, NY'
DEFAULT_REVIEWS_SEARCH_LIMIT = 3
DEFAULT_NAME = "Juliana's Pizza"

BUSINESS_SEARCH_LIMIT = 0
REVIEWS_SEARCH_LIMIT = 0

app = Flask(__name__, static_url_path = "")
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'claudia123':
        return 'reviews123'
    return None

@auth.error_handler
def unauthorized():
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'What you\'re looking for was not found.'}), 404)


#2 - Second funtion called - REMOVE this COMMENT AT WILL.
def get_bearer_token(host, path):
    """Given a bearer token, sends a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        str: OAuth bearer token -- using client_id and client_secret.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    assert CLIENT_ID, "Please supply your client_id."
    assert CLIENT_SECRET, "Please supply your client_secret."
    data = urlencode({
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': GRANT_TYPE,
    })
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
    }
    response = requests.request('POST', url, data=data, headers=headers)
    bearer_token = response.json()['access_token']
    return bearer_token

#5
def make_public_reviews(uri_params):
    '''
    return the full URI that controls the reviews, so that clients get the URIs ready to be used
    For this we can write a small helper function that generates a "public" version of a task to send to the client:
    '''
    new_final_reviews = []
    new_final_reviews = url_for('main', categories=uri_params[0], location=uri_params[1], \
                                        name=uri_params[2], reviews_limit=uri_params[3], \
                                        _external=True)
#    new_final_reviews.append(final_reviews)
    return new_final_reviews

#4 - Fourth function called - REMOVE this COMMENT AT WILL.
def get_reviews(name, business_id, page, reviews_limit):
    """
    Query the Business API by business ID.
      { "business_id": "julianas-pizza-brooklyn-5",
        "name": "Juliana's Pizza"
       }
    """
    page = requests.get(page)
    tree = html.fromstring(page.content)
    #This will create a list of reviews: 
    all_reviews = tree.xpath('//p[@itemprop="description"]/text()')
    ratings = tree.xpath(".//div[contains(@class,'rating-large')]//@title")

    review = {}
    final_reviews = []
    
    count = int(reviews_limit) #converts passed value to interger for proper processing
    new_count = 0
    for i in all_reviews:
        if new_count < count:
            review['review'] = filter(lambda x: x in string.printable, i)
            review['rating'] = ratings[new_count]
            final_reviews.append(review)
            review = {}
            new_count += 1  
    print('---------')     
    print(u'Returning {0} reviews for {1}...'.format(new_count, name))
    print('---------')   
    return final_reviews

#3 - Third funtion called - REMOVE this COMMENT AT WILL.
def send_request(host, path, bearer_token, url_params=None):
    """Given a bearer token, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        bearer_token (str): OAuth bearer token, obtained using client_id and client_secret.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {'Authorization': 'Bearer %s' % bearer_token}

    print(u'Querying {0} ...'.format(url))
    response = requests.request('GET', url, headers=headers, params=url_params)
    return response.json()

#1 - First funtion called - REMOVE this COMMENT AT WILL.
def get_businesses(categories, location, name, reviews_limit): 
    """
    (1) gets a user token
    (2) Sends a fully qualified request to the API for a business with specific criteria
    (3) Searches response JSON objec for a specific business by name
    (4) If name is found and the business has a review count > 0, retrieves a specified
        number of reviews but < 10 per requirements ( this can be changed ... )
    """
    business_id = ''
    business_rating = ''
    uri_params = []
    url_params = {'categories': categories.replace(' ', '+'),
                  'location': location.replace(' ', '+'),
                  'limit': BUSINESS_SEARCH_LIMIT #not currently being used - set to 0, no param passed in
    }
  
    #2 - gets token 
    bearer_token = get_bearer_token(API_HOST, TOKEN_PATH)

    #3 - sends fully qualified request
    response = send_request(API_HOST, SEARCH_PATH, bearer_token, url_params)
    businesses = response.get('businesses')
    
    print(len(businesses)) #print lenght businesses object -- REMOVE AT WILL
    print('---------')
    name_found = 0
    for i in businesses:
        if i['name'] == name:
            name_found = 1
            business_id = i['id']
            business_name = i['name']
            business_rating = i['rating']
            review_count = i['review_count']
            page = i['url']
            print(u'ID: {0} NAME: {1} RATING: {2} REVIEW COUNT: {3} PAGE: {4}'.format(business_id, \
                    business_name, business_rating, review_count, page))
            break
   
    if name_found == 0:
        print(u'No businesses for {0} in {1} with the name {2} found.'.format(categories, location, name))
        return      
    
    print('---------')
    print(u'Match found, querying for ratings for: "{0}" in {1}...'.format(business_name, location))
    print('---------')

    #4 - If business has reviews, get reviews using retrieved business_id
    if review_count > 0:
        if review_count < int(reviews_limit): #only retrieve the number of reviews specifed by criteria
            print('---------')
            print(u'actual review count: {0} vs. reviews limit you provided: {1}'.format(review_count, reviews_limit))
            print('---------')
            print(u'Less reviews than you requested were found for {0}'.format(name))
        
        #4 - gets a public version of the reviews 
        uri_params.extend([categories, location, name, reviews_limit])
        final_reviews = {'name':'',
                         'uri':'',
                         'reviews':''}
        final_reviews['name'] = name
        final_reviews['uri'] = make_public_reviews(uri_params)
        
        #5 - gets reviews for the business based on limit passed
        reviews = get_reviews(name, business_id, page, reviews_limit)
        final_reviews['reviews'] = reviews
        pprint.pprint(final_reviews)
        return final_reviews
    else:
        print(u'No Reviews are available for {0}.'.format(name))
    return

#0 Logic starting point - REMOVE this COMMENT AT WILL.
@app.route('/get-reviews/api/v1.0/reviews/<categories>/<location>/<name>/<reviews_limit>', methods=['GET'])
@auth.login_required
def main(categories, location, name, reviews_limit):
    """
    (1) Makes a call to "get_business" passing the user defined args.
    (2) Arguments are:
        --- categories (str): Defines the categories to search for ( e.g. "pizza")
        --- location (str): Limits the query to a geographic location (e.g. "New York, NY")
        --- name (str): Limits the query to spacific locale, by name
        --- reviews (str): Limits the number of reviews to be returned as < 10
    (3) If no arguments are provided, default values will kick in
    """
    name = name.replace('+', ' ') #clean up all the things ... 
    location = location.replace('+', ' ')
    print('---------')
    print(name, location)
    print('---------')
    try:
        #1 Look up if a business exists with the passed criteria
        reviews = get_businesses(categories, location, name, reviews_limit)           
        if not reviews:
            abort(404)
        return jsonify(reviews)

    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )

if __name__ == '__main__':
    app.run(debug=True)


