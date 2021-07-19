import asyncio
import random
from datetime import datetime

import aiohttp

from automated_bot import config
from automated_bot.models import User, Post


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
        response['user'] = user
        post = Post(**response)
        result.append(post)

    return result


async def create_users():
    print(datetime.now())
    users = []
    for i in range(config.number_of_users):
        data = config.register_data.copy()
        data['username'] = data['username'].replace("0", str(i + 1))
        data['email'] = data['email'].replace('0', str(i + 1))
        result = await post_request(config.url_register, data)
        if result:
            user = User(**result)
            posts = await create_posts_for_user(user)
            user.posts = posts
            users.append(user)

    print(users)
    print(datetime.now())

    # import pdb
    # pdb.set_trace()


if __name__ == '__main__':
    asyncio.run(create_users())
    # asyncio.run(register_user(register_data))
