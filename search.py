# -*- coding: utf-8 -*-
# !/usr/bin/python

# This sample executes a search request for the specified search term.
# Sample usage:
#   python search.py --q=surfing --max-results=10
# NOTE: To use the sample, you must provide a developer key obtained
#       in the Google APIs Console. Search for "REPLACE_ME" in this code
#       to find the correct place to provide that key..

import argparse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import crawlData
from skimage import io
import Protocol
import time


def showImg(img_src):
    image = io.imread(img_src)
    io.imshow(image)
    io.show()


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = 'AIzaSyDWX7321N79YcXyFbulSEdU1zh1RIFM2Gg'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                developerKey=DEVELOPER_KEY)


def mv_download():
    try:
        start = float(time.time())
        for item in Protocol.Group_list:
            channelId = crawlData.search(Protocol.channelId, Protocol.channelName, item['Name'],
                                         Protocol.searchAll_True, Protocol.order_ByRelevance, None, None)
            item['channel'] = crawlData.channel_detail(channelId)
            item['video_list'] = crawlData.search(Protocol.video, Protocol.channelName, item['channel'],
                                                  Protocol.searchAll_True, Protocol.order_ByDate, Protocol.stock_True,
                                                  item['Filter'])
        end = float(time.time())
        print("執行時間 : " + str(end - start) + " s")
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))


def favorite():
    try:
        start = float(time.time())
        for index, item in enumerate(Protocol.Type_list):
            if  item['TYPE'] == 'K-POP channel':
                channeList = crawlData.search(Protocol.channelName, Protocol.favroiteType, item['TYPE'],
                                              Protocol.searchAll_True, Protocol.order_ByViewCount, Protocol.stock_False,
                                              None)
            else:
                channeList = crawlData.search(Protocol.channelName, Protocol.favroiteType, item['TYPE'],
                                          Protocol.searchAll_True, Protocol.order_ByRelevance, Protocol.stock_False,
                                          None)

            Protocol.Type_list[index]['ChannelList'] = channeList
            for index, channel in enumerate(channeList):
                vedioList = crawlData.search(Protocol.video, Protocol.channelName, channel, Protocol.searchAll_False,
                                 Protocol.order_ByRelevance,
                                 Protocol.stock_False, None)
                channel["vedioList"] = vedioList
        end = float(time.time())
        print("執行時間 : " + str(end - start) + " s")
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
