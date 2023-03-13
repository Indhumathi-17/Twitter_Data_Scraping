# Twitter_Data_Scraping
Its an easy solution to scrape the twitter data and download it as different data forms or store it in a database. 

## Tech-world Issues and Solutions

In today's digital world, Data, the rich source of information is increasingly distributed across various platforms like Facebook, Instagram, Youtube, and Twitter host vast amount of data, including photos videos, and text-based content. 
To gain insights and understand trends, the data plays vital role and unevitable resources, so, here I built a solution to scrape data from Twitter extracting data such as the date and time of the tweet, tweet content, user handle, URL, reply count, retweet count, language, source, like count, and other relevant metadata associated with each tweet.
This data can be analyzed and useful to make informed decisions in various domains such as marketing, politics, and social sciences, etc.

## Scraping the tweet

In order to scrape the data from Twitter, I used some modules and python library. 

- pandas
- streamlit
- streamlit_lottie
- pymongo
- snscrape
- base64
- json

## The process:
The data has been scraped using Snscrape library. With TweetSearchScrape() module I was able to scrape the data from Twitter without any Twitter API.

Query is passed to get details to search specific data using hashtag, start date and end date also the number of tweets to be scraped.

## Function to create dataframe
with scraped details like date, id, url, tweet content, reply count, retweet count, source, user, language, like count. 

## Creating GUI
Streamlit app plays role in creating the GUI to scrape the Tweets. I connect the jupyter notebook to Streamlit with help of Anaconda Navigator. In Streamlit, I can use some visually appealing animation and easy buttons to download the data, with help of streamlit_lottie and st.radio() funtion. 

## Download as Json and CSV file
I use the module base64 to download files as csv and json,by encoding the data in order to transmit them from internet safely. With help of B64decode() function, its convienent to decode the data for our use. with base64 its much helpful to transmit the data.

## Upload to MongoDB
Create a database and connect to MongoDB using pymongo, to save the data in MongoDB, I stored the collected data in dictionaries and upload them into the MongoDB from the Streamlit app.

## Finally
Now, you can scrape the data from Twitte and download them in different data forms with this simple solution in form of a web app I built using Python and Streamlit.
