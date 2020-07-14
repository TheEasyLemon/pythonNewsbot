# Newsbot

Hello!

This is Dawson Ren’s Python Newsbot. On the most basic level, it scours a news source's XML sitemap for URLs. These articles, which are written in HTML, are then parsed for their title, author, name, and news source, and saved to .txt files within News. The way I've implemented this last step is pretty janky and requires a lot of human input, so that's another problem.
Because each news source stores its past articles in a different way, you’ll notice that each news source has its own folder in here. Whenever you run the .py script with the news source's name (`nbc.py`, `ajz,py`, etc.) , you’ll only be parsing the news for that news source.
The way each news source is stored can be found in the info .txt file.

Here’s the list of news sources:
- Reuters
- Economist
- AJZ (Al Jazeera)
- Foreign Policy

Works in progress:
- NYT - sitemap comes from a gunzip file

Limitations
- requests.get() is used synchronously, so slow
