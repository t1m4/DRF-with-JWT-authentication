class User():

    def __init__(self, username, email, access, refresh):
        self.username = username
        self.email = email
        self.access = access
        self.refresh = refresh
        self.posts = None

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
        return "%s %s" % (self.title, self.user)


class Like():
    def __init__(self, post, user):
        self.post = post
        self.user = user

    def __str__(self):
        return "%s %s" % (self.post.title, self.user)


if __name__ == '__main__':
    u = User(username="12", email="132", access='123', refresh="123")
    print(u)
