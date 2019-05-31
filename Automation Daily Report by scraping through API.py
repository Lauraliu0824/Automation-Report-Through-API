#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Packages needed for authentication
import httplib2 as lib2 #Example of the "as" function
from oauth2client import client #Importing a sub-package

#Packages needed for connecting with Google API
from googleapiclient.discovery import build as google_build #An example with all the statements together

#Data processing packages
import pandas as pd
import pandas
import numpy as np
import json
from datetime import date, datetime, timedelta #importing multiple sub-packages from one package
from dateutil import parser

from urllib.request import urlopen

import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
get_ipython().run_line_magic('matplotlib', 'inline')

import wikipedia
pd.set_option('display.max_colwidth', -1)


# In[2]:


#We have this from previous sections
access_token = "you access token"
refresh_token = "your refresh token"
client_id = "your client id"
client_secret = "you client secret"

#This is consistent for all Google services
token_uri = 'token url'

#We are essentially setting the expiry date to 1 day before today, which will make it always expire
token_expiry = datetime.now() - timedelta(days = 1)


user_agent = 'my-user-agent/1.0'

#The real code that initalized the client
credentials = client.GoogleCredentials(access_token=access_token, refresh_token=refresh_token, 
                                       client_id=client_id, client_secret=client_secret, 
                                       token_uri=token_uri, token_expiry=token_expiry, 
                                       user_agent=user_agent)

#Initialize Http Protocol    
http = lib2.Http()

#Authorize client
authorized = credentials.authorize(http)

#API Name and Verison, these don't change until 
#they release a new API version for us to play with. 
api_name = 'analyticsreporting'
api_version = 'v4'

#Let's build the client
api_client = google_build(serviceName=api_name, version=api_version, http=authorized)


# In[3]:


# Time range
start_date = (datetime.today()-timedelta(1)).strftime('%Y-%m-%d')    #change here, current report start date
#start_date = '2019-05-27'
running_time_range = 0      #change here, current report running time range
datetime_start_date = date(*map(int, start_date.split('-')))
end_date = str(datetime_start_date + timedelta(running_time_range))


# In[4]:


start_date


# In[5]:


end_date


# # Total Pageviews and Sessions

# In[6]:


#Scrape data from Googe Analytics

sample_request = {
      'viewId': '11392197',
      
      'dateRanges': [{'startDate': start_date, 'endDate':end_date }],

     
      'metrics': [{'expression': 'ga:pageviews'},{'expression': 'ga:sessions'}],
      
    

    }

response = api_client.reports().batchGet(
      body={
        'reportRequests': sample_request
      }).execute()

#Parse the response of API
def prase_response(report):

    """Parses and prints the Analytics Reporting API V4 response"""
    #Initialize results, in list format because two dataframes might return
    result_list = []

    #Initialize empty data container for the two dateranges (if there are two that is)
    data_csv = []
    data_csv2 = []

    #Initialize header rows
    header_row = []

    #Get column headers, metric headers, and dimension headers.
    columnHeader = report.get('columnHeader', {})
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
    dimensionHeaders = columnHeader.get('dimensions', [])

    #Combine all of those headers into the header_row, which is in a list format
    for dheader in dimensionHeaders:
        header_row.append(dheader)
    for mheader in metricHeaders:
        header_row.append(mheader['name'])

    #Get data from each of the rows, and append them into a list
    rows = report.get('data', {}).get('rows', [])
    for row in rows:
        row_temp = []
        dimensions = row.get('dimensions', [])
        metrics = row.get('metrics', [])
        for d in dimensions:
            row_temp.append(d)
        for m in metrics[0]['values']:
            row_temp.append(m)
            data_csv.append(row_temp)

        #In case of a second date range, do the same thing for the second request
        if len(metrics) == 2:
            row_temp2 = []
            for d in dimensions:
                row_temp2.append(d)
            for m in metrics[1]['values']:
                row_temp2.append(m)
            data_csv2.append(row_temp2)

    #Putting those list formats into pandas dataframe, and append them into the final result
    result_df = pandas.DataFrame(data_csv, columns=header_row)
    result_list.append(result_df)
    if data_csv2 != []:
        result_list.append(pandas.DataFrame(data_csv2, columns=header_row))

    return result_list


response_data = response.get('reports', [])[0]
get_table = prase_response(response_data)[0].reset_index()
Total_Pageviews = get_table.iloc[0]['ga:pageviews']
Total_Sessions = get_table.iloc[0]['ga:sessions']


# # Total Artist Pageviews

# In[7]:


#Scrape data from Googe Analytics

sample_request = {
      'viewId': '11392197',
      
      'dateRanges': [{'startDate': start_date, 'endDate':end_date }],

     
      'metrics': [{'expression': 'ga:pageviews'}],
      'dimensionFilterClauses': [{'filters': [{'dimensionName': 'ga:pageTitle','operator': 'ENDS_WITH','expressions':['Concert Setlists | setlist.fm'] }]}]
    
      
    

    }

response = api_client.reports().batchGet(
      body={
        'reportRequests': sample_request
      }).execute()

#Parse the response of API
def prase_response(report):

    """Parses and prints the Analytics Reporting API V4 response"""
    #Initialize results, in list format because two dataframes might return
    result_list = []

    #Initialize empty data container for the two dateranges (if there are two that is)
    data_csv = []
    data_csv2 = []

    #Initialize header rows
    header_row = []

    #Get column headers, metric headers, and dimension headers.
    columnHeader = report.get('columnHeader', {})
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
    dimensionHeaders = columnHeader.get('dimensions', [])

    #Combine all of those headers into the header_row, which is in a list format
    for dheader in dimensionHeaders:
        header_row.append(dheader)
    for mheader in metricHeaders:
        header_row.append(mheader['name'])

    #Get data from each of the rows, and append them into a list
    rows = report.get('data', {}).get('rows', [])
    for row in rows:
        row_temp = []
        dimensions = row.get('dimensions', [])
        metrics = row.get('metrics', [])
        for d in dimensions:
            row_temp.append(d)
        for m in metrics[0]['values']:
            row_temp.append(m)
            data_csv.append(row_temp)

        #In case of a second date range, do the same thing for the second request
        if len(metrics) == 2:
            row_temp2 = []
            for d in dimensions:
                row_temp2.append(d)
            for m in metrics[1]['values']:
                row_temp2.append(m)
            data_csv2.append(row_temp2)

    #Putting those list formats into pandas dataframe, and append them into the final result
    result_df = pandas.DataFrame(data_csv, columns=header_row)
    result_list.append(result_df)
    if data_csv2 != []:
        result_list.append(pandas.DataFrame(data_csv2, columns=header_row))

    return result_list


response_data = response.get('reports', [])[0]
get_table = prase_response(response_data)[0].reset_index()
Artist_homepageview = get_table.iloc[0]['ga:pageviews']


# In[8]:


sample_request = {
      'viewId': '11392197',
      
      'dateRanges': [{'startDate': start_date, 'endDate':end_date }],

     
      'metrics': [{'expression': 'ga:pageviews'}],
      'dimensionFilterClauses': [{'filters': [{'dimensionName': 'ga:pagePath','operator': 'BEGINS_WITH','expressions':['/setlist/'] }]}]
    

    }

response = api_client.reports().batchGet(
      body={
        'reportRequests': sample_request
      }).execute()




#Parse the response of API
def prase_response(report):

    """Parses and prints the Analytics Reporting API V4 response"""
    #Initialize results, in list format because two dataframes might return
    result_list = []

    #Initialize empty data container for the two dateranges (if there are two that is)
    data_csv = []
    data_csv2 = []

    #Initialize header rows
    header_row = []

    #Get column headers, metric headers, and dimension headers.
    columnHeader = report.get('columnHeader', {})
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
    dimensionHeaders = columnHeader.get('dimensions', [])

    #Combine all of those headers into the header_row, which is in a list format
    for dheader in dimensionHeaders:
        header_row.append(dheader)
    for mheader in metricHeaders:
        header_row.append(mheader['name'])

    #Get data from each of the rows, and append them into a list
    rows = report.get('data', {}).get('rows', [])
    for row in rows:
        row_temp = []
        dimensions = row.get('dimensions', [])
        metrics = row.get('metrics', [])
        for d in dimensions:
            row_temp.append(d)
        for m in metrics[0]['values']:
            row_temp.append(m)
            data_csv.append(row_temp)

        #In case of a second date range, do the same thing for the second request
        if len(metrics) == 2:
            row_temp2 = []
            for d in dimensions:
                row_temp2.append(d)
            for m in metrics[1]['values']:
                row_temp2.append(m)
            data_csv2.append(row_temp2)

    #Putting those list formats into pandas dataframe, and append them into the final result
    result_df = pandas.DataFrame(data_csv, columns=header_row)
    result_list.append(result_df)
    if data_csv2 != []:
        result_list.append(pandas.DataFrame(data_csv2, columns=header_row))

    return result_list



response_data = response.get('reports', [])[0]
get_table = prase_response(response_data)[0].reset_index()

Artist_setlist = get_table.iloc[0]['ga:pageviews']


# In[9]:


Artist_Pageviews = int(Artist_setlist) + int(Artist_homepageview)
Artist_Pageviews


# In[10]:


#Scrape data from Googe Analytics

sample_request = {
      'viewId': '11392197',
      
      'dateRanges': [{'startDate': start_date, 'endDate':end_date }],

     
      'metrics': [{'expression': 'ga:pageviews'}],
      'dimensionFilterClauses': [{'filters': [{'dimensionName': 'ga:pagePath','operator': 'BEGINS_WITH','expressions':['/news/'] }]}]
     

    }

response = api_client.reports().batchGet(
      body={
        'reportRequests': sample_request
      }).execute()



#Parse the response of API
def prase_response(report):

    """Parses and prints the Analytics Reporting API V4 response"""
    #Initialize results, in list format because two dataframes might return
    result_list = []

    #Initialize empty data container for the two dateranges (if there are two that is)
    data_csv = []
    data_csv2 = []

    #Initialize header rows
    header_row = []

    #Get column headers, metric headers, and dimension headers.
    columnHeader = report.get('columnHeader', {})
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
    dimensionHeaders = columnHeader.get('dimensions', [])

    #Combine all of those headers into the header_row, which is in a list format
    for dheader in dimensionHeaders:
        header_row.append(dheader)
    for mheader in metricHeaders:
        header_row.append(mheader['name'])

    #Get data from each of the rows, and append them into a list
    rows = report.get('data', {}).get('rows', [])
    for row in rows:
        row_temp = []
        dimensions = row.get('dimensions', [])
        metrics = row.get('metrics', [])
        for d in dimensions:
            row_temp.append(d)
        for m in metrics[0]['values']:
            row_temp.append(m)
            data_csv.append(row_temp)

        #In case of a second date range, do the same thing for the second request
        if len(metrics) == 2:
            row_temp2 = []
            for d in dimensions:
                row_temp2.append(d)
            for m in metrics[1]['values']:
                row_temp2.append(m)
            data_csv2.append(row_temp2)

    #Putting those list formats into pandas dataframe, and append them into the final result
    result_df = pandas.DataFrame(data_csv, columns=header_row)
    result_list.append(result_df)
    if data_csv2 != []:
        result_list.append(pandas.DataFrame(data_csv2, columns=header_row))

    return result_list

response_data = response.get('reports', [])[0]
get_table = prase_response(response_data)[0].reset_index()

blogs_Pageviews = get_table.iloc[0]['ga:pageviews']
blogs_Pageviews


# In[ ]:





# In[11]:


Key_Metrics = pd.DataFrame(data = {'Key Indicator': ['Total Sessions', 'Total Pageviews', 'Artist Pageviews', 'News Article Pageviews'],
                                  'Count': [Total_Sessions,Total_Pageviews,Artist_Pageviews,blogs_Pageviews]})


# In[12]:


Key_Metrics


# # Key Indicators

# In[13]:


Key_Metrics['% of total Pageviews'] = (Key_Metrics['Count'].apply(int)/ int(Total_Pageviews))*100
Key_Metrics['% of total Pageviews']  =  round(Key_Metrics['% of total Pageviews'] ,1).astype(str) + '%'
Key_Metrics['% of total Pageviews'][0] = ''

Key_Metrics['Count'] = Key_Metrics['Count'].apply(int).apply('{:,}'.format)
Key_Metrics #this is the table I wanna insert into my email body and I did it


# # Total Pageviews Trend

# In[14]:


Weekly_total_pageviews = []
date_list = [6,5,4,3,2,1,0]
for i in date_list:
    
    daily_date_for_trend = str(date(*map(int, start_date.split('-'))) - timedelta(i))
    #Concert pageviews
    sample_request = {
          'viewId': '11392197',

          'dateRanges': [{'startDate':daily_date_for_trend , 'endDate':daily_date_for_trend }],


          'metrics': [{'expression': 'ga:pageviews'}],


        }

    response = api_client.reports().batchGet(
          body={
            'reportRequests': sample_request
          }).execute()




    #Parse the response of API
    def prase_response(report):

        """Parses and prints the Analytics Reporting API V4 response"""
        #Initialize results, in list format because two dataframes might return
        result_list = []

        #Initialize empty data container for the two dateranges (if there are two that is)
        data_csv = []
        data_csv2 = []

        #Initialize header rows
        header_row = []

        #Get column headers, metric headers, and dimension headers.
        columnHeader = report.get('columnHeader', {})
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
        dimensionHeaders = columnHeader.get('dimensions', [])

        #Combine all of those headers into the header_row, which is in a list format
        for dheader in dimensionHeaders:
            header_row.append(dheader)
        for mheader in metricHeaders:
            header_row.append(mheader['name'])

        #Get data from each of the rows, and append them into a list
        rows = report.get('data', {}).get('rows', [])
        for row in rows:
            row_temp = []
            dimensions = row.get('dimensions', [])
            metrics = row.get('metrics', [])
            for d in dimensions:
                row_temp.append(d)
            for m in metrics[0]['values']:
                row_temp.append(m)
                data_csv.append(row_temp)

            #In case of a second date range, do the same thing for the second request
            if len(metrics) == 2:
                row_temp2 = []
                for d in dimensions:
                    row_temp2.append(d)
                for m in metrics[1]['values']:
                    row_temp2.append(m)
                data_csv2.append(row_temp2)

        #Putting those list formats into pandas dataframe, and append them into the final result
        result_df = pandas.DataFrame(data_csv, columns=header_row)
        result_list.append(result_df)
        if data_csv2 != []:
            result_list.append(pandas.DataFrame(data_csv2, columns=header_row))

        return result_list

    response_data = response.get('reports', [])[0]
    Weekly_total_pageview = prase_response(response_data)[0]['ga:pageviews'][0]

    Weekly_total_pageviews.append(Weekly_total_pageview)

datetimes = []
date_list = [6,5,4,3,2,1,0]
for i in date_list:
    
    datetime = str(date(*map(int, start_date.split('-'))) - timedelta(i))
    datetimes.append(datetime)
Trend_total_Pageviews = pd.DataFrame({'Date': datetimes, 'Total Pageviews': Weekly_total_pageviews})
Trend_total_Pageviews['Total Pageviews'] = Trend_total_Pageviews['Total Pageviews'].apply(int)

#Formatting the table
weekdays = []
for i in datetimes:
    
    Weekday = parser.parse(i).strftime("%a")
    weekdays.append(Weekday)
    
Trend_total_Pageviews['Weekday'] =weekdays
    
Trend_total_Pageviews['Date'] = Trend_total_Pageviews['Date'].str.replace('2019-','')
Trend_total_Pageviews['DateTime']= Trend_total_Pageviews["Date"] +' ' + Trend_total_Pageviews["Weekday"].map(str)



Trend_total_Pageviews


# # Totaly Artist Pageviews Trend

# In[15]:


Weekly_artist_pageviews = []
date_list = [6,5,4,3,2,1,0]
for i in date_list:
    
    daily_date_for_trend = str(date(*map(int, start_date.split('-'))) - timedelta(i))

    sample_request = {
          'viewId': '11392197',

          'dateRanges': [{'startDate':daily_date_for_trend , 'endDate':daily_date_for_trend }],


          'metrics': [{'expression': 'ga:pageviews'}],
          'dimensionFilterClauses': [{'filters': [{'dimensionName': 'ga:pageTitle','operator': 'ENDS_WITH','expressions':['Concert Setlists | setlist.fm'] }]}]


        }

    response = api_client.reports().batchGet(
          body={
            'reportRequests': sample_request
          }).execute()

    #Parse the response of API
    def prase_response(report):

        """Parses and prints the Analytics Reporting API V4 response"""
        #Initialize results, in list format because two dataframes might return
        result_list = []

        #Initialize empty data container for the two dateranges (if there are two that is)
        data_csv = []
        data_csv2 = []

        #Initialize header rows
        header_row = []

        #Get column headers, metric headers, and dimension headers.
        columnHeader = report.get('columnHeader', {})
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
        dimensionHeaders = columnHeader.get('dimensions', [])

        #Combine all of those headers into the header_row, which is in a list format
        for dheader in dimensionHeaders:
            header_row.append(dheader)
        for mheader in metricHeaders:
            header_row.append(mheader['name'])

        #Get data from each of the rows, and append them into a list
        rows = report.get('data', {}).get('rows', [])
        for row in rows:
            row_temp = []
            dimensions = row.get('dimensions', [])
            metrics = row.get('metrics', [])
            for d in dimensions:
                row_temp.append(d)
            for m in metrics[0]['values']:
                row_temp.append(m)
                data_csv.append(row_temp)

            #In case of a second date range, do the same thing for the second request
            if len(metrics) == 2:
                row_temp2 = []
                for d in dimensions:
                    row_temp2.append(d)
                for m in metrics[1]['values']:
                    row_temp2.append(m)
                data_csv2.append(row_temp2)

        #Putting those list formats into pandas dataframe, and append them into the final result
        result_df = pandas.DataFrame(data_csv, columns=header_row)
        result_list.append(result_df)
        if data_csv2 != []:
            result_list.append(pandas.DataFrame(data_csv2, columns=header_row))

        return result_list

    response_data = response.get('reports', [])[0]
    Metrics_Artist_homepage = prase_response(response_data)[0]

    sample_request = {
          'viewId': '11392197',

          'dateRanges': [{'startDate':start_date , 'endDate':start_date }],


          'metrics': [{'expression': 'ga:pageviews'}],
          'dimensionFilterClauses': [{'filters': [{'dimensionName': 'ga:pagePath','operator': 'BEGINS_WITH','expressions':['/setlist/'] }]}]


        }

    response = api_client.reports().batchGet(
          body={
            'reportRequests': sample_request
          }).execute()

    #Parse the response of API
    def prase_response(report):

        """Parses and prints the Analytics Reporting API V4 response"""
        #Initialize results, in list format because two dataframes might return
        result_list = []

        #Initialize empty data container for the two dateranges (if there are two that is)
        data_csv = []
        data_csv2 = []

        #Initialize header rows
        header_row = []

        #Get column headers, metric headers, and dimension headers.
        columnHeader = report.get('columnHeader', {})
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
        dimensionHeaders = columnHeader.get('dimensions', [])

        #Combine all of those headers into the header_row, which is in a list format
        for dheader in dimensionHeaders:
            header_row.append(dheader)
        for mheader in metricHeaders:
            header_row.append(mheader['name'])

        #Get data from each of the rows, and append them into a list
        rows = report.get('data', {}).get('rows', [])
        for row in rows:
            row_temp = []
            dimensions = row.get('dimensions', [])
            metrics = row.get('metrics', [])
            for d in dimensions:
                row_temp.append(d)
            for m in metrics[0]['values']:
                row_temp.append(m)
                data_csv.append(row_temp)

            #In case of a second date range, do the same thing for the second request
            if len(metrics) == 2:
                row_temp2 = []
                for d in dimensions:
                    row_temp2.append(d)
                for m in metrics[1]['values']:
                    row_temp2.append(m)
                data_csv2.append(row_temp2)

        #Putting those list formats into pandas dataframe, and append them into the final result
        result_df = pandas.DataFrame(data_csv, columns=header_row)
        result_list.append(result_df)
        if data_csv2 != []:
            result_list.append(pandas.DataFrame(data_csv2, columns=header_row))

        return result_list

    response_data = response.get('reports', [])[0]
    Metrics_Concert_Setlist = prase_response(response_data)[0]

    Metrics_Artist_Pageviews = Metrics_Concert_Setlist['ga:pageviews'].apply(int) + Metrics_Artist_homepage['ga:pageviews'].apply(int) 
    Weekly_artist_pageviews.append(Metrics_Artist_Pageviews[0])
Weekly_artist_pageviews
Trend_Artist_Pageviews = pd.DataFrame({'Date': datetimes, 'Artist Pageviews': Weekly_artist_pageviews})
Trend_Artist_Pageviews['Artist Pageviews'] = Trend_Artist_Pageviews['Artist Pageviews'].apply(int)

#Formatting the table
weekdays = []
for i in datetimes:
    
    Weekday = parser.parse(i).strftime("%a")
    weekdays.append(Weekday)
    
Trend_Artist_Pageviews['Weekday'] =weekdays
    
Trend_Artist_Pageviews['Date'] = Trend_Artist_Pageviews['Date'].str.replace('2019-','')
Trend_Artist_Pageviews['DateTime']= Trend_Artist_Pageviews["Date"] +' ' + Trend_Artist_Pageviews["Weekday"].map(str)
Trend_Artist_Pageviews


Trend_Artist_Pageviews


# # Total Blog Pageviews Trend

# In[16]:


Weekly_blogs_pageviews = []
date_list = [6,5,4,3,2,1,0]
for i in date_list:
    
    daily_date_for_trend = str(date(*map(int, start_date.split('-'))) - timedelta(i))

    sample_request = {
          'viewId': '11392197',
          'pageSize': 30000,

          'dateRanges': [{'startDate':daily_date_for_trend , 'endDate':daily_date_for_trend }],
          'dimensions': [{'name': 'ga:pagePath'},{'name': 'ga:pageTitle'},{'name': 'ga:sourceMedium'}],

          'metrics': [{'expression': 'ga:pageviews'}],
          'dimensionFilterClauses': [{'filters': [{'dimensionName': 'ga:pagePath','operator': 'BEGINS_WITH','expressions':['/news/'] }]}]


        }

    response = api_client.reports().batchGet(
          body={
            'reportRequests': sample_request
          }).execute()

    #Parse the response of API
    def prase_response(report):

        """Parses and prints the Analytics Reporting API V4 response"""
        #Initialize results, in list format because two dataframes might return
        result_list = []

        #Initialize empty data container for the two dateranges (if there are two that is)
        data_csv = []
        data_csv2 = []

        #Initialize header rows
        header_row = []

        #Get column headers, metric headers, and dimension headers.
        columnHeader = report.get('columnHeader', {})
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
        dimensionHeaders = columnHeader.get('dimensions', [])

        #Combine all of those headers into the header_row, which is in a list format
        for dheader in dimensionHeaders:
            header_row.append(dheader)
        for mheader in metricHeaders:
            header_row.append(mheader['name'])

        #Get data from each of the rows, and append them into a list
        rows = report.get('data', {}).get('rows', [])
        for row in rows:
            row_temp = []
            dimensions = row.get('dimensions', [])
            metrics = row.get('metrics', [])
            for d in dimensions:
                row_temp.append(d)
            for m in metrics[0]['values']:
                row_temp.append(m)
                data_csv.append(row_temp)

            #In case of a second date range, do the same thing for the second request
            if len(metrics) == 2:
                row_temp2 = []
                for d in dimensions:
                    row_temp2.append(d)
                for m in metrics[1]['values']:
                    row_temp2.append(m)
                data_csv2.append(row_temp2)

        #Putting those list formats into pandas dataframe, and append them into the final result
        result_df = pandas.DataFrame(data_csv, columns=header_row)
        result_list.append(result_df)
        if data_csv2 != []:
            result_list.append(pandas.DataFrame(data_csv2, columns=header_row))

        return result_list

    response_data = response.get('reports', [])[0]
    get_table = prase_response(response_data)[0].reset_index()

    Source_Pageviews = get_table.drop(['ga:pagePath','index'], axis=1)
    Last_Blog_Pageviews = Source_Pageviews['ga:pageviews'].apply(int).sum()
    Weekly_blogs_pageviews.append(Last_Blog_Pageviews)
    
Trend_Blogs_Pageviews = pd.DataFrame({'Date': datetimes, 'Blogs Pageviews': Weekly_blogs_pageviews})
Trend_Blogs_Pageviews['Blogs Pageviews'] = Trend_Blogs_Pageviews['Blogs Pageviews'].apply(int)

#Formatting the table
weekdays = []
for i in datetimes:
    
    Weekday = parser.parse(i).strftime("%a")
    weekdays.append(Weekday)
    
Trend_Blogs_Pageviews['Weekday'] =weekdays
    
Trend_Blogs_Pageviews['Date'] = Trend_Blogs_Pageviews['Date'].str.replace('2019-','')
Trend_Blogs_Pageviews['DateTime']= Trend_Blogs_Pageviews["Date"] +' ' + Trend_Blogs_Pageviews["Weekday"].map(str)
Trend_Blogs_Pageviews


# In[17]:


# Plot


# In[18]:


####################################
###### Artist
#######################################
def func(x, pos):  # formatter function takes tick label and tick position
    s = '%d' % x
    groups = []
    while s and s[-1].isdigit():
        groups.append(s[-3:])
        s = s[:-3]
    return s + ','.join(reversed(groups))

y_format = tkr.FuncFormatter(func)  # make formatter

x = Trend_Artist_Pageviews['DateTime']
y = Trend_Artist_Pageviews['Artist Pageviews']
ax = plt.subplot(111)
ax.plot(x,y)
ax.yaxis.set_major_formatter(y_format)# set formatter to needed axis
plt.title('Weekly Artist Pageviews')
plt.xticks(rotation=40)
plt.xlabel('Date')
plt.ylabel('Pageviews')

plt.savefig('Artist'+ start_date +'.png',bbox_inches='tight')



# In[19]:


####################################
###### Blog
#######################################
def func(x, pos):  # formatter function takes tick label and tick position
    s = '%d' % x
    groups = []
    while s and s[-1].isdigit():
        groups.append(s[-3:])
        s = s[:-3]
    return s + ','.join(reversed(groups))

y_format = tkr.FuncFormatter(func)  # make formatter

x = Trend_Blogs_Pageviews['DateTime']
y = Trend_Blogs_Pageviews['Blogs Pageviews']
ax = plt.subplot(111)
ax.plot(x,y)
ax.yaxis.set_major_formatter(y_format)# set formatter to needed axis
plt.title('Weekly News Article Pageviews')
plt.xticks(rotation=40)
plt.xlabel('Date')
plt.ylabel('Pageviews')

plt.savefig('Blogs'+ start_date +'.png',bbox_inches='tight')
plt.show()


# In[20]:


####################################
###### Total Pageviews
#######################################

def func(x, pos):  # formatter function takes tick label and tick position
    s = '%d' % x
    groups = []
    while s and s[-1].isdigit():
        groups.append(s[-3:])
        s = s[:-3]
    return s + ','.join(reversed(groups))

y_format = tkr.FuncFormatter(func)  # make formatter

x = Trend_total_Pageviews['DateTime']
y = Trend_total_Pageviews['Total Pageviews']
ax = plt.subplot(111)
ax.plot(x,y)
ax.yaxis.set_major_formatter(y_format)# set formatter to needed axis
plt.title('Weekly Total Pageviews')
plt.xticks(rotation=40)
plt.xlabel('Date')
plt.ylabel('Pageviews')

plt.savefig('Total'+ start_date +'.png',bbox_inches='tight')

plt.show()


# ### from matplotlib.pyplot import figure
# 
# ####################################
# ###### Artist
# #######################################
# 
# 
# 
# def func(x, pos):  # formatter function takes tick label and tick position
#     s = '%d' % x
#     groups = []
#     while s and s[-1].isdigit():
#         groups.append(s[-3:])
#         s = s[:-3]
#     return s + ','.join(reversed(groups))
# 
# y_format = tkr.FuncFormatter(func)  # make formatter
# 
# x = Trend_Artist_Pageviews['DateTime']
# y = Trend_Artist_Pageviews['Artist Pageviews']
# ax = plt.subplot(3,3,2)
# ax.plot(x,y)
# ax.yaxis.set_major_formatter(y_format)# set formatter to needed axis
# plt.title('Weekly Artist Pageviews')
# plt.xticks(rotation=40)
# plt.xlabel('Date')
# 
# 
# plt.rcParams['figure.figsize'] = (20,10)
# 
# #plt.savefig('Artist'+ start_date +'.png')
# 
# ####################################
# ###### Blog
# #######################################
# def func(x, pos):  # formatter function takes tick label and tick position
#     s = '%d' % x
#     groups = []
#     while s and s[-1].isdigit():
#         groups.append(s[-3:])
#         s = s[:-3]
#     return s + ','.join(reversed(groups))
# 
# y_format = tkr.FuncFormatter(func)  # make formatter
# 
# x = Trend_Blogs_Pageviews['DateTime']
# y = Trend_Blogs_Pageviews['Blogs Pageviews']
# ax = plt.subplot(3,3,3)
# ax.plot(x,y)
# ax.yaxis.set_major_formatter(y_format)# set formatter to needed axis
# plt.title('Weekly Blogs Pageviews')
# plt.xticks(rotation=40)
# plt.xlabel('Date')
# 
# plt.rcParams['figure.figsize'] = (20,10)
# 
# #plt.savefig('Blogs'+ start_date +'.png')
# def func(x, pos):  # formatter function takes tick label and tick position
#     s = '%d' % x
#     groups = []
#     while s and s[-1].isdigit():
#         groups.append(s[-3:])
#         s = s[:-3]
#     return s + ','.join(reversed(groups))
# 
# y_format = tkr.FuncFormatter(func)  # make formatter
# 
# x = Trend_total_Pageviews['DateTime']
# y = Trend_total_Pageviews['Total Pageviews']
# ax = plt.subplot(3,3,1)
# ax.plot(x,y)
# ax.yaxis.set_major_formatter(y_format)# set formatter to needed axis
# plt.title('Weekly Total Pageviews')
# plt.xticks(rotation=40)
# plt.xlabel('Date')
# plt.ylabel('Pageviews')
# 
# plt.rcParams['figure.figsize'] =(20,10)
# 
# plt.subplots_adjust(wspace = 0.4)
# plt.show()
# 
# plt.savefig('pageviews'+ start_date +'.png',bbox_inches='tight')

# # Artists to Look Our For

# In[21]:


sample_request = {
      'viewId': '11392197',
      'pageSize': 10000,
      'dateRanges': [{'startDate':start_date , 'endDate':start_date }],

      'dimensions': [{'name': 'ga:pageTitle'}],
      'metrics': [{'expression': 'ga:pageviews'}],
      "orderBys":[{'fieldName':'ga:pageviews',"sortOrder": "DESCENDING"}],
      'metricFilterClauses': [{'filters': [{'metricName': 'ga:pageviews','operator': 'GREATER_THAN','comparisonValue':'0' }]}],
      'dimensionFilterClauses': [{'filters': [{'dimensionName': 'ga:pageTitle','operator': 'ENDS_WITH','expressions':['Concert Setlists | setlist.fm'] }]}]
    

    }

response = api_client.reports().batchGet(
      body={
        'reportRequests': sample_request
      }).execute()



#Parse the response of API
def prase_response(report):

    """Parses and prints the Analytics Reporting API V4 response"""
    #Initialize results, in list format because two dataframes might return
    result_list = []

    #Initialize empty data container for the two dateranges (if there are two that is)
    data_csv = []
    data_csv2 = []

    #Initialize header rows
    header_row = []

    #Get column headers, metric headers, and dimension headers.
    columnHeader = report.get('columnHeader', {})
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
    dimensionHeaders = columnHeader.get('dimensions', [])

    #Combine all of those headers into the header_row, which is in a list format
    for dheader in dimensionHeaders:
        header_row.append(dheader)
    for mheader in metricHeaders:
        header_row.append(mheader['name'])

    #Get data from each of the rows, and append them into a list
    rows = report.get('data', {}).get('rows', [])
    for row in rows:
        row_temp = []
        dimensions = row.get('dimensions', [])
        metrics = row.get('metrics', [])
        for d in dimensions:
            row_temp.append(d)
        for m in metrics[0]['values']:
            row_temp.append(m)
            data_csv.append(row_temp)

        #In case of a second date range, do the same thing for the second request
        if len(metrics) == 2:
            row_temp2 = []
            for d in dimensions:
                row_temp2.append(d)
            for m in metrics[1]['values']:
                row_temp2.append(m)
            data_csv2.append(row_temp2)

    #Putting those list formats into pandas dataframe, and append them into the final result
    result_df = pandas.DataFrame(data_csv, columns=header_row)
    result_list.append(result_df)
    if data_csv2 != []:
        result_list.append(pandas.DataFrame(data_csv2, columns=header_row))

    return result_list

#Formatting the table
response_data = response.get('reports', [])[0]
get_table = prase_response(response_data)[0].reset_index()
get_table['ga:pageviews'] = get_table['ga:pageviews'].astype(int)

Artist_pageviews = get_table.dropna()[0:250]



Artist_pageviews = Artist_pageviews.rename(index=str, columns={"ga:pageTitle": "Artist Name","ga:pageviews": "Pageviews"})
Artist_pageviews['Artist Name'] = Artist_pageviews['Artist Name'].str.replace(' Concert Setlists|setlist.fm', '').str.replace('|','')

Artist_pageviews['Artist Name'] = Artist_pageviews['Artist Name'].str.rstrip()

##########################################################################################################
sample_request = {
      'viewId': '11392197',
      'pageSize': 10000,
      'dateRanges': [{'startDate':start_date , 'endDate':start_date }],

      'dimensions': [{'name': 'ga:pagePath'},{'name': 'ga:pageTitle'}],
      'metrics': [{'expression': 'ga:pageviews'}],
      "orderBys":[{'fieldName':'ga:pageviews',"sortOrder": "DESCENDING"}],
      'metricFilterClauses': [{'filters': [{'metricName': 'ga:pageviews','operator': 'GREATER_THAN','comparisonValue':'0' }]}],
      'dimensionFilterClauses': [{'filters': [{'dimensionName': 'ga:pagePath','operator': 'BEGINS_WITH','expressions':['/setlist/'] }]}]
    

    }

response = api_client.reports().batchGet(
      body={
        'reportRequests': sample_request
      }).execute()




#Parse the response of API
def prase_response(report):

    """Parses and prints the Analytics Reporting API V4 response"""
    #Initialize results, in list format because two dataframes might return
    result_list = []

    #Initialize empty data container for the two dateranges (if there are two that is)
    data_csv = []
    data_csv2 = []

    #Initialize header rows
    header_row = []

    #Get column headers, metric headers, and dimension headers.
    columnHeader = report.get('columnHeader', {})
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
    dimensionHeaders = columnHeader.get('dimensions', [])

    #Combine all of those headers into the header_row, which is in a list format
    for dheader in dimensionHeaders:
        header_row.append(dheader)
    for mheader in metricHeaders:
        header_row.append(mheader['name'])

    #Get data from each of the rows, and append them into a list
    rows = report.get('data', {}).get('rows', [])
    for row in rows:
        row_temp = []
        dimensions = row.get('dimensions', [])
        metrics = row.get('metrics', [])
        for d in dimensions:
            row_temp.append(d)
        for m in metrics[0]['values']:
            row_temp.append(m)
            data_csv.append(row_temp)

        #In case of a second date range, do the same thing for the second request
        if len(metrics) == 2:
            row_temp2 = []
            for d in dimensions:
                row_temp2.append(d)
            for m in metrics[1]['values']:
                row_temp2.append(m)
            data_csv2.append(row_temp2)

    #Putting those list formats into pandas dataframe, and append them into the final result
    result_df = pandas.DataFrame(data_csv, columns=header_row)
    result_list.append(result_df)
    if data_csv2 != []:
        result_list.append(pandas.DataFrame(data_csv2, columns=header_row))

    return result_list



response_data = response.get('reports', [])[0]
get_table = prase_response(response_data)[0].reset_index()
Concert_Pageviews = get_table.drop(['ga:pagePath','index'], axis=1)
#Concert_Pageviews['Rank'] = np.arange(1,len(get_table)+1)
Concert_Pageviews = Concert_Pageviews.rename(index=str, columns={"ga:pageTitle": "Artist Name","ga:pageviews": "Pageviews"})
Concert_Pageviews = Concert_Pageviews[['Artist Name','Pageviews']]
Concert_Pageviews['Artist Name'] = Concert_Pageviews['Artist Name'].str.replace('setlist.fm','').str.replace('|','')
Concert_Pageviews['Pageviews'] = Concert_Pageviews['Pageviews'].astype(int)

Concert_Pageviews["Artist Name"]= Concert_Pageviews["Artist Name"].str.split("Concert", n = 1, expand = True)
Concert_Pageviews["Artist Name"] = Concert_Pageviews["Artist Name"].str.rstrip()

Concert_Pageviews = Concert_Pageviews.groupby('Artist Name').sum().sort_values(by=['Pageviews'],ascending=False)
Concert_Pageviews = Concert_Pageviews.fillna(0)


Artist_pageviews_merge = Artist_pageviews.merge(Concert_Pageviews, how = 'left', on = 'Artist Name')
Artist_pageviews_merge = Artist_pageviews_merge.fillna(0)
Artist_pageviews_merge['Pageviews'] =  Artist_pageviews_merge['Pageviews_x'] + Artist_pageviews_merge['Pageviews_y']
Artist_pageviews_merge = Artist_pageviews_merge.drop(['Pageviews_x','Pageviews_y'], axis=1)
Artist_pageviews_merge['Pageviews'] = Artist_pageviews_merge['Pageviews'].apply(int)

Artist_pageviews_merge = Artist_pageviews_merge.sort_values(by='Pageviews', ascending=False)
Artist_pageviews_merge['Rank'] = np.arange(1,len(Artist_pageviews_merge)+1)
Artist_pageviews_merge.head()


# In[22]:


Artist_pageviews_merge.shape


# In[23]:


last_start_date = str(date(*map(int, start_date.split('-'))) - timedelta(1))
last_start_date


# In[24]:


#Scrape data from Googe Analytics

sample_request = {
      'viewId': '11392197',
      'pageSize': 10000,
      'dateRanges': [{'startDate':last_start_date , 'endDate':last_start_date }],

      'dimensions': [{'name': 'ga:pageTitle'}],
      'metrics': [{'expression': 'ga:pageviews'}],
      "orderBys":[{'fieldName':'ga:pageviews',"sortOrder": "DESCENDING"}],
      'metricFilterClauses': [{'filters': [{'metricName': 'ga:pageviews','operator': 'GREATER_THAN','comparisonValue':'0' }]}],
      'dimensionFilterClauses': [{'filters': [{'dimensionName': 'ga:pageTitle','operator': 'ENDS_WITH','expressions':['Concert Setlists | setlist.fm'] }]}]
    

    }

response = api_client.reports().batchGet(
      body={
        'reportRequests': sample_request
      }).execute()


def prase_response(report):

    """Parses and prints the Analytics Reporting API V4 response"""
    #Initialize results, in list format because two dataframes might return
    result_list = []

    #Initialize empty data container for the two dateranges (if there are two that is)
    data_csv = []
    data_csv2 = []

    #Initialize header rows
    header_row = []

    #Get column headers, metric headers, and dimension headers.
    columnHeader = report.get('columnHeader', {})
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
    dimensionHeaders = columnHeader.get('dimensions', [])

    #Combine all of those headers into the header_row, which is in a list format
    for dheader in dimensionHeaders:
        header_row.append(dheader)
    for mheader in metricHeaders:
        header_row.append(mheader['name'])

    #Get data from each of the rows, and append them into a list
    rows = report.get('data', {}).get('rows', [])
    for row in rows:
        row_temp = []
        dimensions = row.get('dimensions', [])
        metrics = row.get('metrics', [])
        for d in dimensions:
            row_temp.append(d)
        for m in metrics[0]['values']:
            row_temp.append(m)
            data_csv.append(row_temp)

        #In case of a second date range, do the same thing for the second request
        if len(metrics) == 2:
            row_temp2 = []
            for d in dimensions:
                row_temp2.append(d)
            for m in metrics[1]['values']:
                row_temp2.append(m)
            data_csv2.append(row_temp2)

    #Putting those list formats into pandas dataframe, and append them into the final result
    result_df = pandas.DataFrame(data_csv, columns=header_row)
    result_list.append(result_df)
    if data_csv2 != []:
        result_list.append(pandas.DataFrame(data_csv2, columns=header_row))

    return result_list


response_data = response.get('reports', [])[0]
get_table = prase_response(response_data)[0].reset_index()
get_table['ga:pageviews'] = get_table['ga:pageviews'].astype(int)
Last_Artist_pageviews = get_table[0:10000]
#Last_Artist_pageviews['index'] = np.arange(1,len(Last_Artist_pageviews)+1)
Last_Artist_pageviews = Last_Artist_pageviews.rename(index=str, columns={"ga:pageTitle": "Artist Name","ga:pageviews": "Pageviews"})
Last_Artist_pageviews['Artist Name'] = Last_Artist_pageviews['Artist Name'].str.replace(' Concert Setlists|setlist.fm', '').str.replace('|','')

Last_Artist_pageviews['Artist Name'] = Last_Artist_pageviews['Artist Name'].str.rstrip()

###############################################################################################################
#Concert pageviews
sample_request = {
      'viewId': '11392197',
      'pageSize': 10000,
      'dateRanges': [{'startDate':last_start_date , 'endDate':last_start_date }],

      'dimensions': [{'name': 'ga:pagePath'},{'name': 'ga:pageTitle'}],
      'metrics': [{'expression': 'ga:pageviews'}],
      "orderBys":[{'fieldName':'ga:pageviews',"sortOrder": "DESCENDING"}],
      'metricFilterClauses': [{'filters': [{'metricName': 'ga:pageviews','operator': 'GREATER_THAN','comparisonValue':'0' }]}],
      'dimensionFilterClauses': [{'filters': [{'dimensionName': 'ga:pagePath','operator': 'BEGINS_WITH','expressions':['/setlist/'] }]}]
    

    }

response = api_client.reports().batchGet(
      body={
        'reportRequests': sample_request
      }).execute()




#Parse the response of API
def prase_response(report):

    """Parses and prints the Analytics Reporting API V4 response"""
    #Initialize results, in list format because two dataframes might return
    result_list = []

    #Initialize empty data container for the two dateranges (if there are two that is)
    data_csv = []
    data_csv2 = []

    #Initialize header rows
    header_row = []

    #Get column headers, metric headers, and dimension headers.
    columnHeader = report.get('columnHeader', {})
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
    dimensionHeaders = columnHeader.get('dimensions', [])

    #Combine all of those headers into the header_row, which is in a list format
    for dheader in dimensionHeaders:
        header_row.append(dheader)
    for mheader in metricHeaders:
        header_row.append(mheader['name'])

    #Get data from each of the rows, and append them into a list
    rows = report.get('data', {}).get('rows', [])
    for row in rows:
        row_temp = []
        dimensions = row.get('dimensions', [])
        metrics = row.get('metrics', [])
        for d in dimensions:
            row_temp.append(d)
        for m in metrics[0]['values']:
            row_temp.append(m)
            data_csv.append(row_temp)

        #In case of a second date range, do the same thing for the second request
        if len(metrics) == 2:
            row_temp2 = []
            for d in dimensions:
                row_temp2.append(d)
            for m in metrics[1]['values']:
                row_temp2.append(m)
            data_csv2.append(row_temp2)

    #Putting those list formats into pandas dataframe, and append them into the final result
    result_df = pandas.DataFrame(data_csv, columns=header_row)
    result_list.append(result_df)
    if data_csv2 != []:
        result_list.append(pandas.DataFrame(data_csv2, columns=header_row))

    return result_list

response_data = response.get('reports', [])[0]
get_table = prase_response(response_data)[0].reset_index()


Last_Concert_Pageviews = get_table.drop(['ga:pagePath','index'], axis=1)
#Last_Concert_Pageviews['Rank'] = np.arange(1,len(get_table)+1)
Last_Concert_Pageviews = Last_Concert_Pageviews.rename(index=str, columns={"ga:pageTitle": "Artist Name","ga:pageviews": "Pageviews"})
Last_Concert_Pageviews = Last_Concert_Pageviews[['Artist Name','Pageviews']]
Last_Concert_Pageviews['Artist Name'] = Last_Concert_Pageviews['Artist Name'].str.replace('setlist.fm','').str.replace('|','')
Last_Concert_Pageviews['Pageviews'] = Last_Concert_Pageviews['Pageviews'].astype(int)

Last_Concert_Pageviews["Artist Name"]= Last_Concert_Pageviews["Artist Name"].str.split("Concert", n = 1, expand = True)
Last_Concert_Pageviews["Artist Name"] = Last_Concert_Pageviews["Artist Name"].str.rstrip()

Last_Concert_Pageviews = Last_Concert_Pageviews.groupby('Artist Name').sum().sort_values(by=['Pageviews'],ascending=False)



Last_Artist_Pageviews_Merge = Last_Artist_pageviews.merge(Last_Concert_Pageviews, how = 'left', on= 'Artist Name')
Last_Artist_Pageviews_Merge['Pageviews'] = Last_Artist_Pageviews_Merge['Pageviews_x'] +Last_Artist_Pageviews_Merge['Pageviews_y']
Last_Artist_Pageviews_Merge = Last_Artist_Pageviews_Merge.drop(['Pageviews_x','Pageviews_y'], axis=1)
Last_Artist_Pageviews_Merge = Last_Artist_Pageviews_Merge.sort_values(by='Pageviews', ascending=False)

Last_Artist_Pageviews_Merge['Rank'] = np.arange(1,len(Last_Artist_Pageviews_Merge)+1)

Artist_to_Look = Artist_pageviews_merge.merge(Last_Artist_Pageviews_Merge, how = 'left', on= 'Artist Name')
Artist_to_Look['Rank_Delta'] = Artist_to_Look['Rank_y'] - Artist_to_Look['Rank_x']
Artist_to_Look = Artist_to_Look.drop(['index_x','index_y','Pageviews_y','Rank_y'], axis=1)
Artist_to_Look = Artist_to_Look.rename(index=str, columns={"Pageviews_x": "Pageviews","Rank_x": "Rank"})
Artist_to_Look = Artist_to_Look[['Rank','Rank_Delta','Artist Name','Pageviews']]
Artist_to_Look.head()


# In[25]:


Artist_to_Look = Artist_to_Look[~Artist_to_Look['Artist Name'].str.contains('USA')]
Artist_to_Look = Artist_to_Look[~Artist_to_Look['Artist Name'].str.contains('England')]
Artist_to_Look = Artist_to_Look[~Artist_to_Look['Artist Name'].str.contains('Canada')]


# In[26]:


table_Artist_to_Look = Artist_to_Look.iloc[0:200].sort_values(by = 'Rank_Delta', ascending = False).iloc[0:20].sort_values(by = 'Pageviews', ascending = False)
table_Artist_to_Look = table_Artist_to_Look.rename(index = str, columns ={"Rank_Delta": "△ Rank","Rank": "Current Rank"}) 
table_Artist_to_Look = table_Artist_to_Look[['Artist Name','Pageviews','Current Rank','△ Rank']]
table_Artist_to_Look['△ Rank'] = table_Artist_to_Look['△ Rank'].apply(int)


# In[27]:


table_Artist_to_Look


# In[28]:


table_Artist_to_Look['arrow'] = '↑'
table_Artist_to_Look
table_Artist_to_Look["△ Rank"] = table_Artist_to_Look["△ Rank"].map(str) + table_Artist_to_Look["arrow"]
table_Artist_to_Look = table_Artist_to_Look.drop(['arrow'],axis =1)
table_Artist_to_Look


# # Concert Setlists to Look Out For

# In[29]:


sample_request = {
      'viewId': '11392197',
      'pageSize': 10000,
      'dateRanges': [{'startDate':start_date , 'endDate':start_date }],

      'dimensions': [{'name': 'ga:pagePath'},{'name': 'ga:pageTitle'}],
      'metrics': [{'expression': 'ga:pageviews'}],
      "orderBys":[{'fieldName':'ga:pageviews',"sortOrder": "DESCENDING"}],
      'metricFilterClauses': [{'filters': [{'metricName': 'ga:pageviews','operator': 'GREATER_THAN','comparisonValue':'0' }]}],
      'dimensionFilterClauses': [{'filters': [{'dimensionName': 'ga:pagePath','operator': 'BEGINS_WITH','expressions':['/setlist/'] }]}]
    

    }

response = api_client.reports().batchGet(
      body={
        'reportRequests': sample_request
      }).execute()




#Parse the response of API
def prase_response(report):

    """Parses and prints the Analytics Reporting API V4 response"""
    #Initialize results, in list format because two dataframes might return
    result_list = []

    #Initialize empty data container for the two dateranges (if there are two that is)
    data_csv = []
    data_csv2 = []

    #Initialize header rows
    header_row = []

    #Get column headers, metric headers, and dimension headers.
    columnHeader = report.get('columnHeader', {})
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
    dimensionHeaders = columnHeader.get('dimensions', [])

    #Combine all of those headers into the header_row, which is in a list format
    for dheader in dimensionHeaders:
        header_row.append(dheader)
    for mheader in metricHeaders:
        header_row.append(mheader['name'])

    #Get data from each of the rows, and append them into a list
    rows = report.get('data', {}).get('rows', [])
    for row in rows:
        row_temp = []
        dimensions = row.get('dimensions', [])
        metrics = row.get('metrics', [])
        for d in dimensions:
            row_temp.append(d)
        for m in metrics[0]['values']:
            row_temp.append(m)
            data_csv.append(row_temp)

        #In case of a second date range, do the same thing for the second request
        if len(metrics) == 2:
            row_temp2 = []
            for d in dimensions:
                row_temp2.append(d)
            for m in metrics[1]['values']:
                row_temp2.append(m)
            data_csv2.append(row_temp2)

    #Putting those list formats into pandas dataframe, and append them into the final result
    result_df = pandas.DataFrame(data_csv, columns=header_row)
    result_list.append(result_df)
    if data_csv2 != []:
        result_list.append(pandas.DataFrame(data_csv2, columns=header_row))

    return result_list


response_data = response.get('reports', [])[0]
get_table = prase_response(response_data)[0].reset_index()


# In[30]:


get_table['ga:pageviews'] = get_table['ga:pageviews'].apply(int)
get_table = get_table.groupby('ga:pageTitle').sum().sort_values('ga:pageviews', ascending=False)
get_table = get_table.reset_index()
get_table.head()


# In[31]:


Setlist = get_table.iloc[0:20].drop(['index'], axis=1)
Setlist = Setlist["ga:pageTitle"].str.split("Concert Setlist", n = 1, expand = True)
Venue = Setlist[1].str.split(" on ", n = 1, expand = True)
Setlist['Venue'] = Venue [0]

Setlist['Concert Date']  = Venue[1].str.replace('setlist.fm','').str.replace('|','')
Setlist = Setlist.drop([1], axis=1)
Setlist['Venue'] = Setlist['Venue'].str.replace('setlist.fm','').str.replace('at ','')


# In[32]:


Setlist['Pageviews'] = get_table['ga:pageviews']
Setlist =  Setlist.rename(index=str, columns={0: "Artist Name"})


# In[33]:


Setlist['Rank'] = np.arange(1,len(Setlist)+1)
Setlist = Setlist[['Rank','Artist Name','Venue','Concert Date','Pageviews']]
Setlist


# # Top 10 blogs

# In[34]:


#Scrape data from Googe Analytics

sample_request = {
      'viewId': '11392197',
      'pageSize': 10000,
      'dateRanges': [{'startDate':start_date , 'endDate':start_date }],

      'dimensions': [{'name': 'ga:pagePath'},{'name': 'ga:pageTitle'}],
      'metrics': [{'expression': 'ga:pageviews'},{'expression': 'ga:uniquePageviews'},
                 {'expression': 'ga:avgTimeOnPage'}],
      "orderBys":[{'fieldName':'ga:pageviews',"sortOrder": "DESCENDING"}],
      'metricFilterClauses': [{'filters': [{'metricName': 'ga:pageviews','operator': 'GREATER_THAN','comparisonValue':'0' }]}],
      'dimensionFilterClauses': [{'filters': [{'dimensionName': 'ga:pagePath','operator': 'BEGINS_WITH','expressions':['/news/'] }]}]
    

    }

response = api_client.reports().batchGet(
      body={
        'reportRequests': sample_request
      }).execute()



#Parse the response of API
def prase_response(report):

    """Parses and prints the Analytics Reporting API V4 response"""
    #Initialize results, in list format because two dataframes might return
    result_list = []

    #Initialize empty data container for the two dateranges (if there are two that is)
    data_csv = []
    data_csv2 = []

    #Initialize header rows
    header_row = []

    #Get column headers, metric headers, and dimension headers.
    columnHeader = report.get('columnHeader', {})
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
    dimensionHeaders = columnHeader.get('dimensions', [])

    #Combine all of those headers into the header_row, which is in a list format
    for dheader in dimensionHeaders:
        header_row.append(dheader)
    for mheader in metricHeaders:
        header_row.append(mheader['name'])

    #Get data from each of the rows, and append them into a list
    rows = report.get('data', {}).get('rows', [])
    for row in rows:
        row_temp = []
        dimensions = row.get('dimensions', [])
        metrics = row.get('metrics', [])
        for d in dimensions:
            row_temp.append(d)
        for m in metrics[0]['values']:
            row_temp.append(m)
            data_csv.append(row_temp)

        #In case of a second date range, do the same thing for the second request
        if len(metrics) == 2:
            row_temp2 = []
            for d in dimensions:
                row_temp2.append(d)
            for m in metrics[1]['values']:
                row_temp2.append(m)
            data_csv2.append(row_temp2)

    #Putting those list formats into pandas dataframe, and append them into the final result
    result_df = pandas.DataFrame(data_csv, columns=header_row)
    result_list.append(result_df)
    if data_csv2 != []:
        result_list.append(pandas.DataFrame(data_csv2, columns=header_row))

    return result_list


# In[35]:


response_data = response.get('reports', [])[0]
get_table = prase_response(response_data)[0].drop_duplicates(subset=None, keep='first')
get_table['Rank'] = np.arange(1,len(get_table)+1)

Blog_Pageviews = get_table.drop(['ga:pagePath'], axis=1)
Blog_Pageviews = Blog_Pageviews.rename(index=str, columns={"ga:pageTitle": "Page Title","ga:pageviews": "Pageviews",
                                                           "ga:uniquePageviews": "UniquePageviews",
                                                          
                                                           'ga:avgTimeOnPage':'Avg Time on Page'})
Blog_Pageviews = Blog_Pageviews[['Rank','Page Title','Pageviews','UniquePageviews','Avg Time on Page']]
Blog_Pageviews['Page Title'] = Blog_Pageviews['Page Title'].str.replace('setlist.fm','').str.replace('|','')
Blog_Pageviews = Blog_Pageviews.head(10)


# In[36]:


Blog_Pageviews


# In[ ]:





# In[ ]:





# In[37]:


Blog_Pageviews['Avg Time on Page'] = pd.to_datetime(Blog_Pageviews['Avg Time on Page'],unit='s').apply(lambda x: x.strftime('%M:%S'))


# In[38]:


Blog_Pageviews


# # Top 20 Searches

# In[39]:


sample_request = {
      'viewId': '11392197',
      'pageSize': 10000,
      'dateRanges': [{'startDate':start_date , 'endDate':start_date }],

      'dimensions': [{'name': 'ga:searchKeyword'}],
      'metrics': [{'expression': 'ga:searchUniques'}],
      "orderBys":[{'fieldName':'ga:searchUniques',"sortOrder": "DESCENDING"}],
      #'metricFilterClauses': [{'filters': [{'metricName': 'ga:pageviews','operator': 'GREATER_THAN','comparisonValue':'0' }]}],
      #'dimensionFilterClauses': [{'filters': [{'dimensionName': 'ga:pagePath','operator': 'BEGINS_WITH','expressions':['/setlist/'] }]}]
    

    }

response = api_client.reports().batchGet(
      body={
        'reportRequests': sample_request
      }).execute()




#Parse the response of API
def prase_response(report):

    """Parses and prints the Analytics Reporting API V4 response"""
    #Initialize results, in list format because two dataframes might return
    result_list = []

    #Initialize empty data container for the two dateranges (if there are two that is)
    data_csv = []
    data_csv2 = []

    #Initialize header rows
    header_row = []

    #Get column headers, metric headers, and dimension headers.
    columnHeader = report.get('columnHeader', {})
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
    dimensionHeaders = columnHeader.get('dimensions', [])

    #Combine all of those headers into the header_row, which is in a list format
    for dheader in dimensionHeaders:
        header_row.append(dheader)
    for mheader in metricHeaders:
        header_row.append(mheader['name'])

    #Get data from each of the rows, and append them into a list
    rows = report.get('data', {}).get('rows', [])
    for row in rows:
        row_temp = []
        dimensions = row.get('dimensions', [])
        metrics = row.get('metrics', [])
        for d in dimensions:
            row_temp.append(d)
        for m in metrics[0]['values']:
            row_temp.append(m)
            data_csv.append(row_temp)

        #In case of a second date range, do the same thing for the second request
        if len(metrics) == 2:
            row_temp2 = []
            for d in dimensions:
                row_temp2.append(d)
            for m in metrics[1]['values']:
                row_temp2.append(m)
            data_csv2.append(row_temp2)

    #Putting those list formats into pandas dataframe, and append them into the final result
    result_df = pandas.DataFrame(data_csv, columns=header_row)
    result_list.append(result_df)
    if data_csv2 != []:
        result_list.append(pandas.DataFrame(data_csv2, columns=header_row))

    return result_list


response_data = response.get('reports', [])[0]
get_table = prase_response(response_data)[0].reset_index()


# In[40]:


get_table['low_case'] =  get_table['ga:searchKeyword'].str.lower().str.replace('2019', '')
get_table['ga:searchUniques'] = get_table['ga:searchUniques'].apply(int)
get_table["low_case"] = get_table["low_case"].str.rstrip()
search = get_table.groupby('low_case').sum().sort_values(by=['ga:searchUniques'], ascending=False).reset_index()
search = search.drop(['index'],axis = 1)
search = search.rename(index=str, columns={"low_case": "Term","ga:searchUniques": "Search Times"})
search = search.head(20)
search['Rank'] = np.arange(1,len(search)+1)
search = search[['Rank','Term','Search Times']]
search


# In[ ]:





# In[41]:


###########################HTML FOR key blog to look out for table
import io

df3 = Blog_Pageviews

str_io3 = io.StringIO()

df3.to_html(buf=str_io3, classes='table table-striped', index = False)

html_str_keyind3 = str_io3.getvalue()


# In[42]:


###########################HTML FOR key concert setlist to look out for table
import io

df2 = Setlist

str_io2 = io.StringIO()

df2.to_html(buf=str_io2, classes='table table-striped', index = False)

html_str_keyind2 = str_io2.getvalue()


# In[43]:


###########################HTML FOR key Artists to look out for table
import io

df1 = table_Artist_to_Look

str_io1 = io.StringIO()

df1.to_html(buf=str_io1, classes='table table-striped', index = False)

html_str_keyind1 = str_io1.getvalue()


# In[44]:


################# HTML FOR key indicators table
import io

df = Key_Metrics

str_io = io.StringIO()

df.to_html(buf=str_io, classes='table table-striped', index = False)

html_str_keyind = str_io.getvalue()


# In[45]:


################# HTML FOR key indicators table
import io

df4 = search

str_io = io.StringIO()

df4.to_html(buf=str_io, classes='table table-striped', index = False)

html_str_keyind4 = str_io.getvalue()


# In[46]:


#import win32com.client
from win32com.client import Dispatch
import datetime 
import win32com.client

########################################
### Set up file to attach
########################################



########################################
## Connect to Outlook inbox
#########################################


#####################
### Craete new Email
#####################
const=win32com.client.constants
olMailItem = 0x0
obj = win32com.client.Dispatch("Outlook.Application")
newMail = obj.CreateItem(olMailItem)

###########################################PLOT!!!!!!!
attachment1 = newMail.Attachments.Add(r"C:\Users\mengyin.liu\Desktop\Coding Project\Interior Report\Total"+start_date+'.png')
attachment2 = newMail.Attachments.Add(r"C:\Users\mengyin.liu\Desktop\Coding Project\Interior Report\Artist"+start_date+'.png')
attachment3 = newMail.Attachments.Add(r"C:\Users\mengyin.liu\Desktop\Coding Project\Interior Report\Blogs"+start_date+'.png')



attachment1.PropertyAccessor.SetProperty("http://schemas.microsoft.com/mapi/proptag/0x3712001F", "MyId1")
attachment2.PropertyAccessor.SetProperty("http://schemas.microsoft.com/mapi/proptag/0x3712001F", "MyId2")
attachment3.PropertyAccessor.SetProperty("http://schemas.microsoft.com/mapi/proptag/0x3712001F", "MyId3")

#mail.HTMLBody = "<html><body>Test image <img src=""cid:MyId1""></body></html>"

##################################
##Mail content
##################################
newMail.Subject = "Setlist Daily Report " + start_date
#newMail.Attachments.Add(filename)
newMail.HtmlBody = (r""" <p><font face="verdana">
                        
                         Daily summary data from """ + start_date + """  <br><br>
                         
                         <br><br><p><font size="5"><b>Key Indicators<b></font></p>"""  + html_str_keyind +
                        """
                         
                         <img src="cid:MyId1"><img src="cid:MyId2"><img src="cid:MyId3">
                         
                       <br> <br><p><font face="verdana">"""  + """ <br><br><p><font size="5">Artists to Look Out For:</font></p><br> 
                       
                      
                        """ +  
                        html_str_keyind1 + """<br><br> <p><font size="5">Top 20 Concert Setlists:</font></p>""" +
                        html_str_keyind2 +"""<br><br> <p><font size="5">Top 10 News Articles:</font></p>""" + 
                        html_str_keyind3 +"""<br><br> <p><font size="5">Top 20 Terms Users Search:</font></p>""" +
                        html_str_keyind4
                    
                    
                        
                       
                    
                        )

                      
##################################
### Set recipients to maillist
#################################
newMail.To = 'your email address'
#newMail.CC = 'my@email.com'

################################
## Show E-mail (change to send to send)
################################

newMail.display()


# In[ ]:





# In[ ]:




