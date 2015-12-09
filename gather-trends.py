#!/usr/bin/env python

import os
import os.path
import sys
import datetime as dt
import json
import twitter
import urllib3
from time import sleep
from pandas import Series, DataFrame
import pandas as pd
import csv

# to force utf-8 encoding on entire program
reload(sys)  
sys.setdefaultencoding('utf8')

# Files and paths.

FN_TWITTER_CREDENTIALS = 'credentials.json'
FP_WORKDIR="//var/www/twitter_trends/"
FP_TWITTER_CREDENTIALS = os.path.join(FP_WORKDIR, FN_TWITTER_CREDENTIALS)

def createTwitterObject(credentialsFilePath):
            """
            Create twitter access object.
            credentialsFilePath is a json file containing Twitter credentials from twitter.
            """
            configFP = open(credentialsFilePath)
            mydict = json.load(configFP)

            oauth_consumerKey = mydict['consumerKey']
            oauth_consumerSecret = mydict['consumerSecret']
            oauth_token = mydict['token']
            oauth_tokenSecret = mydict['tokenSecret']
	   
            # Twitter class to get data from Twitter, format is json by default.
            t = twitter.Twitter(
                        auth=twitter.OAuth(oauth_token, oauth_tokenSecret,
                                           oauth_consumerKey, oauth_consumerSecret),
                        api_version='1.1'
                        )
            return t


# Column names in Places & Trends CSV files
COL_PLACE = 'Place'
COL_PLACE_TYPE = 'PlaceType'
COL_COUNTRY = 'Country'
COL_COUNTRY_CODE = 'CountryCode'
COL_WOEID = 'Woeid'
COL_URL = 'Url'
COL_LOCATIONS ='Locations'
COL_TRENDS = 'Trends'


def createPlacesDataFrameFromJson(data):
            """
	   Extracts the trends/available data from Twitter into something useful
	   and save it in a DataFrame. Data is not sorted. Param(data) is expected
	   to be the JSON text from Twitter's response.
            """
            # Generate data arrays
            dPlace = []
            dType = []
            dCty = []
            dCtyCode = []
            dWoeid = []
            dUrl = []
            for record in data:
                        dPlace.append(record['name'])
                        dType.append(record['placeType']['name'])
                        dCty.append(record['country'])
                        dCtyCode.append(record['countryCode'])
                        dWoeid.append(record['woeid'])
                        dUrl.append(record['url'])

	   # Data frame data
                        df = {
		      COL_PLACE: dPlace,
		      COL_PLACE_TYPE: dType,
		      COL_COUNTRY: dCty,
		      COL_COUNTRY_CODE: dCtyCode,
		      COL_WOEID: dWoeid,
		      COL_URL: dUrl
            }
	   # Fix order of columns
            return DataFrame(df, columns=[COL_PLACE, COL_COUNTRY, COL_COUNTRY_CODE,
            COL_PLACE_TYPE, COL_WOEID, COL_URL])




def getTwitterPlaces(credentialsFilePath):
            """
            Calls Twitter's REST API to get trends/available.json result as a data frame.
            credentialsFilePath is a json file containing Twitter credentials.
            """
            # Twitter class to get data from Twitter, format is json by default.
            t = createTwitterObject(credentialsFilePath)

            # Contact twitter
            jsonData = t.trends.available()# Returns python object json representation.
            print("start printing here ...")
            #print(jsonData);
            # Process into data frame
            frame = createPlacesDataFrameFromJson(jsonData)

            # Sort according to ...
            fsorted = frame.sort_index(by=[COL_COUNTRY])
            return fsorted
	   
	   

def createTrendsDataFrameFromJson(data):
            """
            Extracts the trends/place.json data from Twitter into something useful
            and save it in a DataFrame. Data is not sorted. Param(data) is expected
            to be the JSON text from Twitter's response.
            This uses woeid from places.json data to get the trends for every city.
            """
            # Warn that we only process the first element
            if (len(data) > 1):
                        print('WARNING: only the first item of place.json result is processed.')
            dataItem = data[0]
            # Generate data columns
            dTimestamp = dataItem['created_at']
            print ('dTimestamp:',dTimestamp)
            dTrends = []
            dLocs = []
            for record in dataItem['trends']:
                        trendName = record['name']
                        if (record['promoted_content'] is not None):
                                    trendName += '(promoted content)'
                        dTrends.append(trendName)
	   
                                    # Combine trends into a single cell. Escape comma characters.
            trendCell = '|'.join(dTrends)
            trendCell = trendCell.replace(',', ';')

            # Now process locations, also an array.
            for record in dataItem['locations']:
                        locName = record['name']
                        dLocs.append(locName)

            locCell = '|'.join(dLocs)
            locCell = locCell.replace(',', ';')
            # Format datetime into 2 columns, date and time.
            naiveTimestampObj = dt.datetime.strptime(dTimestamp, '%Y-%m-%dT%H:%M:%SZ')
            # Data frame data
            dframe = {COL_TRENDS: trendCell, COL_LOCATIONS: locCell}
            # Fix order of columns
            return DataFrame(dframe, index=[0], columns=[COL_LOCATIONS, COL_TRENDS])

def getTwitterTrendsDataFrame(credentialsFilePath, woeid):
            """
            Call Twitter REST API to get trends/place.json data and return it
            as a single row data frame.
            credentialsFilePath is the json file containing Twitter credentials.
            woeid identifies the place you want trend information for.
            """
            # Twitter class to get data from Twitter, format is json by default.
            t = createTwitterObject(credentialsFilePath)

            # Use _id instead of id, because id would end up been appended to the base URL.
            # See source code api.py line 169.


            jsonTrends = t.trends.place(_id=woeid)   # Response is python object json representation
            #print(jsonTrends);

            fs = createTrendsDataFrameFromJson(jsonTrends)
            return fs
            # Process into data frame
            frame = createPlacesDataFrameFromJson(jsonData)

	   
##### Functions for getting places and trends from twitter


def getPlaces():
            # No places.csv file available, so we have to create it
            #by first calling function to get places in json format

            df = getTwitterPlaces(FP_TWITTER_CREDENTIALS);
            #print(df)
            df.to_csv(FP_WORKDIR+'/output/places.csv', header=False)
            print("csv file for places written..")
            #for line in cdata:
                        #print(line[0])


def getWOEIDandTrends():
            '''
            This function is used to get woeid from places.csv to get trends
            for each city and save it in trends.csv (appending it every time a city trends are got)
            and create locations.csv for maintaining a latest trends record
            '''
            #f = getPlaces();
            with open(FP_WORKDIR+'/output/places.csv') as cfile:
                        data=[]
                        cdata = csv.reader(cfile)
                        has_rows = False

                        for row in cdata:
                                    #if row != '':
                                    if cdata.line_num >= 2:
                                                has_rows = True
                                                data.append(row[5])
                                                #print(data) 
                                                for result in data:
                                                            #print(result)                                                            
                                                            r=[]
                                    loc=None
                                    loc = open(FP_WORKDIR+'/output/locations.csv', "a")
                        if not has_rows:
                                    print("places.csv file empty.. So calling places ..")
                                    f = getPlaces();
                                    loc = open(FP_WORKDIR+'/output/locations.csv', "w")
                                    print(f)                        
                        
            with open(FP_WORKDIR+'/output/trends.csv', 'a') as f:
                        index = 0
                        for index in range(1):
                                    r = data[index]
                                    print("printing new place trends for....................................")
                                    #print(r)
                                    dframe = getTwitterTrendsDataFrame(FP_TWITTER_CREDENTIALS, r)
                                    dframe.to_csv(f, header=False)
                                    if loc is not None :
                                                dframe.to_csv(loc, header=False)

                                    re = deleteRowsFromPlaces();           
                                    print("removing rows from places.csv..")
                                    #index += 1

def writeCities():
            '''
            For displaying the cities in front-end webpage - with auto complete feature
            '''
            cities_set = set() # holds cities already written 
            f1 = csv.reader(open(FP_WORKDIR+'/output/trends.csv', 'r'))
            with open(FP_WORKDIR+'/output/city.txt', 'w') as city:
                                    for row in f1:
                                                if row[1] not in cities_set:
                                                            city.write(row[1])
                                                            city.write('\n')
                                                            cities_set.add(row[1])



def deleteRowsFromPlaces():
	      # From the places file, obtain the first entry of the places data.
	      placesDframe = pd.read_csv(FP_WORKDIR+'/output/places.csv')
	      firstRow = placesDframe.ix[0] ##placesDframe[0:1] # returns a Series
	      # Delete the first row and save the places file, overwriting original.
	      # Hence we have removed the place we have successfully processed.
	      newDframe = placesDframe.drop([0], axis=0)
	      newDframe.to_csv(FP_WORKDIR+'/output/places.csv', sep=',', index=False)
	      
res = getWOEIDandTrends();
print(res)

print("program end/ csv file for Trends written..")

at_end = writeCities()  # calling/writing city.txt towards end - to get all trends.csv location access.

