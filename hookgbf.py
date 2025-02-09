import feedparser
from discord_webhook import DiscordWebhook,DiscordEmbed
import os
from time import sleep
import datetime

sentlogs="./logs/content.log"
errlogs="./logs/err.log"
if not os.path.exists(sentlogs):
  with open(sentlogs,"w") as ff:
    pass
if not os.path.exists(errlogs):
    with open(errlogs,"w") as ff:
        pass
try:
  url = os.environ['USER']
  hooklink=os.environ['HOOKSECRET']

except Exception as ee:
  with open(errlogs,"a+") as ff:
    err=f"{datetime.datetime.today()}||Err: {ee}\n"
    ff.write(err)
    exit()
try:
  feed = feedparser.parse(url)
  if feed.status == 200:
    with open(sentlogs,"+r") as ff:
      sentt=ff.readlines()
      entryno=len(sentt)
    try:
      for entry in reversed(feed.entries):
        text=entry.link        
        if f"{text.split('/')[-1]}\n" in sentt:
          continue
        text=entry.link
        webhook=DiscordWebhook(url=hooklink,content=text)
        webhook.execute()
        if entryno>60:
          with open(sentlogs,"w") as ff:
            newlog=''.join(sentt[50:])
            ff.write(newlog)
          with open(errlogs,"w") as ff:
            pass
        with open(sentlogs,"a+") as ff:
          ff.write(f"{text.split('/')[-1]}\n") 
    except Exception as e:
      with open(errlogs,"a+") as ff:
        err=f"{datetime.datetime.today()}||WebhookErr: {e}\n"
        ff.write(err)
  else:
    with open(errlogs,"a+") as ff:
      err=f"{datetime.datetime.today()}||Failed to get RSS feed. Status code: {feed.status}"
      ff.write(err)

except Exception as e:
  with open(errlogs,"a+") as ff:
    err=f"{datetime.datetime.today()}||FeedErr: {e}\n"
    ff.write(err)
