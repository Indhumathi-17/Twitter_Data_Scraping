#import all necessary modules
import pandas as pd
import streamlit as st
from streamlit_lottie import st_lottie
import requests
import json
import snscrape.modules.twitter as sntwitter
import pymongo
from pymongo import MongoClient
import base64

#giving my webpage a name
st.set_page_config(page_title="NewGen",layout='centered')

#make the header with specific style,color,font
st.markdown("<h1 style='text-align:center ; color: #e2cbfe; font-family:'PoppinsRegular'; font-weight: bold;'>Twitter Data Scraping", unsafe_allow_html=True)

#set image with streamlit_lottie 
def image(url: str):
    r = requests.get(url)
    if r.status_code !=200:
        return None
    return r.json()

#download the link from lottiefiles
laptop_image = image ("https://assets2.lottiefiles.com/packages/lf20_2glqweqs.json")

#giving some customized specification to the image
st_lottie(laptop_image,height=700,width=None,speed = 1,reverse = False,loop=True,quality='high',key='laptop')

#getting required details from user
keyword = st.text_input('Enter the hashtag:')
start_date = st.date_input('Choose the start date:',key = 'start_date')
end_date = st.date_input('Choose the end date:', key = 'end_date')
tweet_count = st.number_input('Enter the number of tweets to be scraped:', key ='limit')

#data scraping function
def Scraping_TwitterData(keyword, start_date, end_date, tweet_count):
    scrape = sntwitter.TwitterSearchScraper(f"#{keyword} since:{start_date} until:{end_date}")
    ScrapedData = []
    
    for i, tweet in enumerate(scrape.get_items()):
        Tweet_Info = {
            'Date': tweet.date,
            'Id': tweet.id,
            'url': tweet.url,
            'Content': tweet.content,
            'User': tweet.user.username,
            'Reply_count': tweet.replyCount,
            'Retweet_count': tweet.retweetCount,
            'language': tweet.lang,
            'source': tweet.source,
            'like_count': tweet.likeCount
        }
        ScrapedData.append(Tweet_Info)
        if i >= tweet_count:
            break
    return ScrapedData

#create a dataframe to store all collected data
def create_data (ScrapedData):
    Tweet_Info = pd.DataFrame(ScrapedData, columns=['Date','Id','url','Content','User','Reply_count','Retweet_count','language','source','like_count'])
    return Tweet_Info

#give option to scrape the data using a button
if st.button('Scrape the Data'):
    ScrapedData = Scraping_TwitterData(keyword, start_date, end_date, tweet_count)
    Tweet_Info=create_data(ScrapedData)
    st.dataframe(Tweet_Info)

#with help of st.radio I can create visually appealing options to download the data
options = ['Download as CSV file','Download as Json']
selected_option = st.radio('Select an option to Download:',options,index=1)

#for download data as csv file, here I use base64 a built_in module to transmit the encoded data safely over the internet, also use b64decode() to decode the data
if selected_option == 'Download as CSV file':
    ScrapedData = Scraping_TwitterData(keyword, start_date, end_date, tweet_count)
    Tweet_Info=create_data(ScrapedData)
    csv = Tweet_Info.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="Tweet_Info.csv">Download CSV File</a>'
    st.markdown(href,unsafe_allow_html=True)

#to download data as Json, again I used base64 function
if selected_option =='Download as Json':
    ScrapedData = Scraping_TwitterData(keyword, start_date, end_date, tweet_count)
    Tweet_Info=create_data(ScrapedData)
    json_str = Tweet_Info.to_json(indent=2)
    b64 = base64.b64encode(json_str.encode()).decode()
    href =  href = f'<a href="data:file/json;base64,{b64}" download="Tweet_Info.json">Download JSON File</a>'
    st.markdown(href,unsafe_allow_html=True)
       
#to upload data in MongoDB here I create a database with collections to store the data       
if st.button('Upload to MongoDB'):
    ScrapedData = Scraping_TwitterData(keyword, start_date, end_date, tweet_count)
    Tweet_Info=create_data(ScrapedData)
    
    client = MongoClient('mongodb://Indhumathi:guvi2022@ac-gu0gx2a-shard-00-00.rdjud8z.mongodb.net:27017,ac-gu0gx2a-shard-00-01.rdjud8z.mongodb.net:27017,ac-gu0gx2a-shard-00-02.rdjud8z.mongodb.net:27017/?ssl=true&replicaSet=atlas-dqzly7-shard-0&authSource=admin&retryWrites=true&w=majority')
    db = client['Twitter_Data']
    coll = db['Tweets']
    Tweet_Info_json = json.loads(Tweet_Info.to_json(orient='records'))
    coll.insert_many(Tweet_Info_json)
    st.success('Uploaded to MongoDB')
       