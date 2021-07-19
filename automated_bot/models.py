from automated_bot import config


class User():

    def __init__(self, username, email, access, refresh):
        self.username = username
        self.email = email
        self.access = access
        self.refresh = refresh
        self.posts = None
        self.like_count = config.max_likes_per_user

    def __str__(self):
        return self.username


class Post():
    def __init__(self, id, user, title, description):
        self.id = id
        self.user = user
        self.title = title
        self.description = description
        self.likes = None

    def __str__(self):
        return "%s-%s" % (self.title, self.user)


class Like():
    def __init__(self, post, user):
        self.post = post
        self.user = user

    def __str__(self):
        return "%s-%s" % (self.post.title, self.user)
