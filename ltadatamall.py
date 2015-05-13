import json
import urllib
from urlparse import urlparse
import httplib2 as http

#External library

#Authentication parameter
headers = { 'AccountKey' : 'MnvwjNVGDVKl8Ig9uipL3Q==',
        'UniqueUserID' : 'ee84f4e2-caae-4ab5-afa3-02a7348efd2f',
        'accept' : 'application/json'} #Request results in JSON

#API parameters
uri = 'http://datamall.cloudapp.net' #Resource URL



def traffic():
        path = '/ltaodataservice.svc/IncidentSet?'
        #Query parameters
        params = {}#'Latitude':'1.304980', #Search within a radius
        #       'Longitude':'103.831984', # from a central point
        #       'Distance':'5000'}; # Distance in metres

        #Build query string & specify type of API call
        target = urlparse(uri + path + urllib.urlencode( params ) )
        print target.geturl()
        method = 'GET'
        body = ''

        #Get handle to http
        h = http.Http()

        #Obtain results
        response, content = h.request(
                target.geturl(),
                method,
                body,
                headers)

        #Parse JSON to print
        jsonObj = json.loads(content)

        return jsonObj

def bus():
        path = '/ltaodataservice/BusArrival?'

        #Query parameters
        params = {'BusStopID':'44961', #bef blk 484
                'ServiceNo':'922'}

        #'Latitude':'1.304980', #Search within a radius
        #       'Longitude':'103.831984', # from a central point
        #       'Distance':'5000'}; # Distance in metres

        #Build query string & specify type of API call
        target = urlparse(uri + path + urllib.urlencode( params ) )
        print target.geturl()
        method = 'GET'
        body = ''

        #Get handle to http
        h = http.Http()

        #Obtain results
        response, content = h.request(
                target.geturl(),
                method,
                body,
                headers)
        
        #Parse JSON to print
        jsonObj = json.loads(content)

        return jsonObj