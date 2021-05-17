from selenium import webdriver
import time
import pandas as pd
from googleapiclient.discovery import build
import re


api_key = 'AIzaSyBQWXnuUyHN7aJliDTw8DavfcS3aTr2Qx4'
video_ids = ['http://www.youtube.com/watch?v=FLt7bCtsvNk',
 'http://www.youtube.com/watch?v=DpaAf7KRaZM',
 'http://www.youtube.com/watch?v=YOketbttgfg',
 'http://www.youtube.com/watch?v=10QkOikYI68',
 'http://www.youtube.com/watch?v=7XIfVxBNTXw',
 'http://www.youtube.com/watch?v=dszhmazAtSk',
 'http://www.youtube.com/watch?v=S5WN7gTYnfA',
 'http://www.youtube.com/watch?v=6Ef6ZNJmDLE',
 'http://www.youtube.com/watch?v=k3BqlalhjN4',
 'http://www.youtube.com/watch?v=h6M7Et0a2fY'] #이 부분에 아이디 넣으면 됨.


for i in range(len(video_ids)):
    video_ids[i] = video_ids[i][-11:]





comment_ = []
for i in range(len(video_ids)):
    video_id = video_ids[i]
    comments = list()
    api_obj = build('youtube', 'v3', developerKey=api_key)
    response = api_obj.commentThreads().list(part='snippet,replies', videoId=video_id, maxResults=100).execute()

    while response:
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append([comment['textDisplay'], comment['authorDisplayName'], comment['publishedAt'], comment['likeCount']])
     
            if item['snippet']['totalReplyCount'] > 0:
                for reply_item in item['replies']['comments']:
                    reply = reply_item['snippet']
                    comments.append([reply['textDisplay'], reply['authorDisplayName'], reply['publishedAt'], reply['likeCount']])
     
        if 'nextPageToken' in response:
            response = api_obj.commentThreads().list(part='snippet,replies', videoId=video_id, pageToken=response['nextPageToken'], maxResults=100).execute()
        else:
            break

    df = pd.DataFrame(comments)
    df = df.sort_values(by=3, ascending = False,)
    df_sample = df[0].head(5)
    df_val = df_sample.values
    df_list = df_val.tolist()

    sentence = ''
    for i in df_list:
        pattern=re.compile(r'\s\s+')
        i=re.sub(pattern,' ',i)
        i=re.sub('[^ 가-힣]','',i)
        i=re.sub(' +', ' ', i)
        i=i.strip()
        sentence += i
        sentence += ' '

    comment_.append(sentence)
orig_df = pd.read_csv('뜨뜨뜨뜨_#2.csv',encoding='cp949')
orig_df['comment_text'] = comment_
orig_df.drop('Unnamed: 0',axis = 1, inplace = True)
print(orig_df)  
orig_df.to_csv('뜨뜨뜨뜨_fin.csv',index=False, encoding='cp949')
    
'''
    print(df)
    df.to_csv(filename, header=['comment', 'author', 'date', 'num_likes'],encoding = 'utf-8-sig', index=None)

    df = pd.read_csv(filename) # for구문으로 csv파일들을 읽어 들인다
    df_sample = df.loc[:,['comment','num_likes']]
'''
    
