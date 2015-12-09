#LatestTrendsinTwitter

OVERVIEW:

Twitter – the micro blogging social media platform, has an awesome feature called “Trends” which displays Hot topics being shared or tweeted on Twitter.
Twitter APIs gives developers access to the real time data  comprising of tweets & trends. The Twitter REST API can be used to connect with and get  the trending data from Twitter.
With various visualization techniques available like D3.js and Google Fusion Table, the Twitter trends (hot topics) can be visualized and projected in a higher standard .
Creating a tool which will allow the user find out trending topics from locations all across the World, will be of great help. And visualizing the twitter topics will give a clear analytics of trending topics.


TECHNOLOGY OVERVIEW:

PYTHON programming language is used to write scripts to gather data from Twitter 
Twitter API is used to authenticate and establish connection with Twitter. Also, gather trending data from Twitter in JSON format
The Python script Gather.py also modifies JSON data, using Data Frames to store data as CSV files
After the High level Data Gathering, csv files containing Data are used as a Database for generating Word Cloud using D3.js
Again, python script named Tagcloud.py is used to get the trends.csv file and generate a huge database of cities.json files
Google Fusion Table API is then used to create a Map containing current trends by location – geo-tagged on the map.
Java program is scripted as a project, which is then used to connect & authenticate with Google API and clear old fusion table data to import new updated rows in to the Google Fusion Table.


MODULEs INVOLVED & HOW IT WORKS:

HIGH LEVEL DATA GATHERING
Python script gather-trends.py connects and authenticates with Twitter API and gets trending places data in JSON format from Twitter.
The data in JSON format is stored as Places.csv, from which the WOIED is got. 
The WOEID is again used to get Trends place by place in real time using Twitter REST API
These trends by place are also collected in JSON format, which is again changed as a csv named trends.csv
Trends.csv is appended every time a new trending data is collected from twitter. A simultaneous csv called locations.csv is used to write only the current information for all trending places; which will be later used for creating Google Fusion  Table.

TAG CLOUD
Python script tagcloud.py is used to generate cities.json with trending topics from the Trends.csv file.
The cities .json files form the database for generating word cloud using D3.js, individually for every city/location.

FUSION TABLE
Fusion table is used to visualize the trending information from Twitter.
A java program along with Google API is used to authenticate and connect.
Also to delete previous information in fusion table and update / import new records of data.

