import asyncio
import random
from datetime import datetime

import aiohttp

from automated_bot import config
from automated_bot.models import User, Post, Like


async def post_request(url, data, headers=None):
    """
    Send post request and return Json or None
    :param headers: not required, because we can register without Authorization
    """
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url, data=data) as r:
            if r.status == 201:
                return await r.json()
            else:
                config.logger.info("Couldn't create with %s'", data)


async def create_posts_for_user(user):
    """
    Create random number of posts for given user
    """
    headers = {"Authorization": "Bearer %s" % user.access}
    number_of_posts = random.randint(1, config.max_posts_per_user)
    result = []
    for i in range(number_of_posts):
        data = config.post_data.copy()
        data['title'] = data['title'].replace("0", str(i + 1))
        response = await post_request(config.url_create_post, data, headers)
        if response:
            response['user'] = user
            post = Post(**response)
            result.append(post)
    user.posts = result

async def create_users():
    """
    Create users and posts for them
    """
    users = []
    aws_for_posts = []
    for i in range(config.number_of_users):
        data = config.register_data.copy()
        data['username'] = data['username'].replace("0", str(i + 1))
        data['email'] = data['email'].replace('0', str(i + 1))
        response = await post_request(config.url_register, data)
        if response:
            user = User(**response)
            aws_for_posts.append(create_posts_for_user(user))
            # posts = await create_posts_for_user(user)
            # user.posts = posts
            users.append(user)
    r = await asyncio.gather(*aws_for_posts)

    return users


async def create_random_likes(users):
    result = []

    for user in users:
        for i in range(config.max_likes_per_user):
            whose_user_post = random.choice(users)
            post = random.choice(whose_user_post.posts)
            like = await create_like_for_user_and_post(user, post)
            if like:
                result.append(like)

            # may be when we like second time one post, we need to unlike it.

    return result


async def create_like_for_user_and_post(user, post):
    data = config.like_data.copy()
    data['post_id'] = post.id
    headers = {"Authorization": "Bearer %s" % user.access}
    response = await post_request(config.url_like_post, data, headers)
    if response:
        like = Like(post=post, user=user)
        return like
    else:
        print("Can't like", user, post)
        # User already like this post or another error
        return None


async def main():
    print(datetime.now())
    users = await create_users()
    print(datetime.now())
    likes = await create_random_likes(users)
    print(len(likes))
    print(datetime.now())


if __name__ == '__main__':
    asyncio.run(main())
    # asyncio.run(register_user(register_data))
