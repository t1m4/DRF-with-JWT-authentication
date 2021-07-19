import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent / '.env'
load_dotenv(env_path)

# define logger
log_format = logging.Formatter('[%(asctime)s] [%(filename)s.%(funcName)s.%(lineno)d] [%(levelname)s] - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# writing to stdout
# handler = logging.StreamHandler(sys.stdout)
handler = logging.FileHandler(filename='info.log')
handler.setLevel(logging.INFO)
handler.setFormatter(log_format)
logger.addHandler(handler)

# define urls
host = "http://127.0.0.1:8000"
url_register = host + "/auth/api/register/"
url_create_post = host + "/facebook/api/create_post/"
url_like_post = host + "facebook/api/like/"

# get env variables
number_of_users = int(os.environ.get('number_of_users', 10))
max_posts_per_user = int(os.environ.get('max_posts_per_user', 10))
max_likes_per_user = int(os.environ.get('max_likes_per_user', 10))

# define data
register_data = {
    'email': 'test_0@example.com',
    'username': 'test_0',
    'password': 'very_strong_password',
    'double_password': 'very_strong_password',
}

post_data = {
    'title': 'post_title_0',
    'description': 'description',
}