class Book(object):
    def __init__(self, url, book_name, image_url, book_type,  introduction, author, publishing, publishing_time,
                 price, editors_choice, content_validity, about_author, catalog, media_reviews):
        self.url = url  # 网页URL
        self.book_name = book_name  # 书名
        self.image_url = image_url  # 书封面
        self.book_type = book_type  # 类型
        self.introduction = introduction  # 简单介绍
        self.author = author  # 作者
        self.publishing = publishing  # 出版社
        self.publishing_time = publishing_time  # 出版时间
        self.price = price  # 价格
        self.editors_choice = editors_choice  # 编辑推荐
        self.content_validity = content_validity  # 内容简介
        self.about_author = about_author  # 关于作者，作者简介
        self.catalog = catalog  # 目录
        self.media_reviews = media_reviews  # 媒体评论

    @property
    def url(self):
        return self.url

    @url.setter
    def url(self, value):
        self.url = value

    @property
    def book_name(self):
        return self.book_name

    @book_name.setter
    def book_name(self, value):
        self.book_name = value

    @property
    def image_url(self):
        return self.image_url

    @image_url.setter
    def image_url(self, value):
        self.image_url = value

    @property
    def book_type(self):
        return self.book_type

    @book_type.setter
    def book_type(self, value):
        self.book_type = value

    @property
    def introduction(self):
        return self.introduction

    @introduction.setter
    def introduction(self, value):
        self.introduction = value

    @property
    def author(self):
        return self.author

    @author.setter
    def author(self, value):
        self.author = value

    @property
    def publishing(self):
        return self.publishing

    @publishing.setter
    def publishing(self, value):
        self.publishing = value

    @property
    def publishing_time(self):
        return self.publishing_time

    @publishing_time.setter
    def publishing_time(self, value):
        self.publishing_time = value

    @property
    def price(self):
        return self.price

    @price.setter
    def price(self, value):
        self.price = value

    @property
    def editors_choice(self):
        return self.editors_choice

    @editors_choice.setter
    def editors_choice(self, value):
        self.editors_choice = value

    @property
    def content_validity(self):
        return self.content_validity

    @content_validity.setter
    def content_validity(self, value):
        self.content_validity = value

    @property
    def about_author(self):
        return self.about_author

    @about_author.setter
    def about_author(self, value):
        self.about_author = value

    @property
    def catalog(self):
        return self.catalog

    @catalog.setter
    def catalog(self, value):
        self.catalog = value

    @property
    def media_reviews(self):
        return self.media_reviews

    @media_reviews.setter
    def media_reviews(self, value):
        self.media_reviews = value



