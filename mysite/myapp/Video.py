from googleapiclient.discovery import build
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json
api_key="AIzaSyBUFNjfHbxq-N4jdgCAGIE0aIb1RV6iTrI"

class Video:
    sentiment = SentimentIntensityAnalyzer()
    video_url = "placeholder"
    def pull_comments(self):
        video_id = self.video_url.split("v=")
        youtube = build(
            'youtube',
            'v3',
        developerKey=api_key
        )
        request = youtube.commentThreads().list(
            part='snippet',
            videoId= video_id[-1],
            textFormat = 'plainText',
            maxResults=100
        ).execute()
        return request
    def video_data(self):
        video_id = self.video_url.split("v=")
        youtube = build(
            'youtube',
            'v3',
        developerKey=api_key
        )
        request = youtube.videos().list(part='snippet,statistics', id=video_id).execute()
        return request
    def get_title(self):
        video_title = self.video_data()['items'][0]['snippet']['title']
        return video_title
    def get_publish(self):
        publish_date = self.video_data()['items'][0]['snippet']['publishedAt']
        final_date = publish_date.split("T")
        return final_date[0]
    def get_description(self):
        description = self.video_data()['items'][0]['snippet']['description']
        return description
    def get_channel(self):
        channel = self.video_data()['items'][0]['snippet']['channelTitle']
        return channel
    def get_likes(self):
        like_count = self.video_data()['items'][0]['statistics']['likeCount']
        return like_count
    def get_views(self):
        like_count = self.video_data()['items'][0]['statistics']['viewCount']
        return like_count
    def get_thumbnail(self):
        thumbnail = self.video_data()['items'][0]['snippet']['thumbnails']['high']['url']
        return thumbnail
    def create_comments_list(self):
        video_comments = self.pull_comments()
        full_list =[]
        for items in video_comments['items']:
            comment = items['snippet']['topLevelComment']['snippet']['textDisplay']
            full_list.append(comment)
        context = {
            "data": full_list
        }
        return context
    def comment_sentiment_list(self):
        sentiment_list = []
        video_comments = self.pull_comments()
        for items in video_comments['items']:
            comment = items['snippet']['topLevelComment']['snippet']['textDisplay']
            sentiment_score = round(self.sentiment.polarity_scores(comment)['compound'] * 100, 1)
            pos_score = round(self.sentiment.polarity_scores(comment)['pos'] * 100, 1)
            negative_score = round(self.sentiment.polarity_scores(comment)['neg'] * 100, 1)
            neutral_score = round(self.sentiment.polarity_scores(comment)['neu'] * 100, 1)
            comment_data = (comment, sentiment_score, pos_score, negative_score, neutral_score)
            sentiment_list.append(comment_data)
        return sentiment_list
    def average_sentiment(self):
        sentiment_data = self.comment_sentiment_list()
        sentiment_counter = 0
        comment_counter = 0
        for comment in sentiment_data:
            sentiment_counter += comment[1]
            comment_counter += 1
        average_sentiment = round(sentiment_counter / comment_counter, 1)
        return average_sentiment
    def view_positive_comments(self):
        video_comments = self.comment_sentiment_list()
        positive_counter = 0
        pos_com_list = []
        for comment in video_comments:
            if comment[1]>0.05:
                pos_com_list.append(comment)
                positive_counter += 1
        pos_comments = {
            'positiveComments': pos_com_list,
            'positiveCounter': positive_counter
        }
        return pos_comments
    def view_neutral_comments(self):
        video_comments = self.comment_sentiment_list()
        neu_counter = 0
        neu_com_list = []
        for comment in video_comments:
            if comment[1]>-0.05 and comment[1]<.05:
                neu_com_list.append(comment)
                neu_counter += 1
        neu_comments = {
            'neutralComments': neu_com_list,
            'neutralCounter': neu_counter
        }
        return neu_comments
    def view_negative_comments(self):
        video_comments = self.comment_sentiment_list()
        negative_counter = 0
        neg_com_list = []
        for comment in video_comments:
            if comment[1]<-0.05:
                neg_com_list.append(comment)
                negative_counter+=1
        neg_comments = {
            'negativeComments': neg_com_list,
            'negativeCounter': negative_counter
        }
        return neg_comments
    def highest_positive_comment(self):
        pos_comment_list = self.view_positive_comments()
        highest_comment = ""
        highest_score = 0
        for comment in pos_comment_list['positiveComments']:
            if comment[1] > highest_score:
                highest_score, highest_comment= comment[1], comment 
        return highest_comment
    def lowest_negative_comment(self):
        neg_comment_list = self.view_negative_comments()
        lowest_score = 0
        lowest_comment = ""
        for comment in neg_comment_list['negativeComments']:
            if comment[1] < lowest_score:
                lowest_score, lowest_comment= comment[1], comment 
        return lowest_comment
    def video_statistics(self):
        statistics = {
            'likeCount': self.get_likes(),
            'viewCount': self.get_views,
            'title': self.get_title(),
            'publishDate': self.get_publish(),
            'description': self.get_description(),
            'averageSentiment': self.average_sentiment(),
            'channel': self.get_channel(),
            'thumbnail': self.get_thumbnail(),
            'lowestComment': self.lowest_negative_comment(),
            'highestComment': self.highest_positive_comment()
        }
        return statistics
    def googlecharts_json(self):
        video_comments = self.comment_sentiment_list()
        pos_num = self.view_positive_comments()['positiveCounter']
        neg_num = self.view_negative_comments()['negativeCounter']
        neu_num = self.view_neutral_comments()['neutralCounter']
        comment_num = pos_num + neg_num + neu_num
        scatter_array = []
        scatter_counter = 1
        for comment in video_comments:
            scatter_array.append([scatter_counter, comment[1]])
            scatter_counter += 1
        percentage_dict = {
            "percentPos": round(pos_num / comment_num, 2),
            "percentNeg": round(neg_num / comment_num, 2),
            "percentNeu": round(neu_num / comment_num, 2),
            'scatterChart': scatter_array
        }
        json_dict = json.dumps(percentage_dict)
        print(pos_num)
        print(neg_num)
        print(neu_num)
        print(comment_num)
        return json_dict