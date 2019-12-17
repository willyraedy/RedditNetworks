import praw
from dotenv import load_dotenv
load_dotenv()
import os

CLIENT_SECRET = os.getenv("REDDIT_API_SECRET")
PASSWORD = os.getenv("REDDIT_PASSWORD")

reddit_api_wrapper = praw.Reddit(client_id='f_wJd_CV9WBtxg',
                                 client_secret=CLIENT_SECRET,
                                 password=PASSWORD, user_agent='script:melis-thesis:v0.0.1 (by /u/wilburRay)',
                                 username='wilburRay')
