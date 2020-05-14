#Python Newsbot v1#

Hello!

This is Dawson Ren’s Python Newsbot. On the most basic level, it scours a news source's XML sitemap for URLs. These articles, which are written in HTML, are then parsed for their title, author, name, and news source, and saved to .txt files within News. The way I've implemented this last step is pretty janky and requires a lot of human input, so that's another problem.

Because each news source stores its past articles in a different way, you’ll notice that each news source has its own folder in here. Whenever you run the .py script with the news source's name (`nbc.py`, `ajz,py`, etc.) , you’ll only be parsing the news for that news source.

The way each news source is stored can be found in the info .txt file.

Here’s the list of news sources:

Reuters -- functional
NBC -- broken from misdirects
Economist -- functional
AJZ -- functional
Foreign Policy -- functional
Forbes -- broken
Brookings Institute -- broken
NYT -- NOT functional, due to downloading xml sitemaps as compressed .gz (gunzip) files. Haven't figured out how to unzip these files within the program. Outside modules haven't worked (I think).

Limitations

Right now, you can only run these python scripts through the shell (such as the native terminal, or a 3rd party IDE such as Eclipse or IDLE).

They must be run through the shell (bash or otherwise) using the command

python3 [.py file]

in order to run many news sites simultaneously.

Additionally, the retrieval and storage of articles is asynchronous, meaning that the program deals with URLs as if you're in a line, serving each URL individually, rather than having multiple lines, serving them in parallel. Pretty inefficient. 

Yusuf, you should probably use the asyncio module from python. It's great! I think it's like javascript notation. Use the "async" keyword.
