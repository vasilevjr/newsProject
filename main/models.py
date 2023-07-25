from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class News(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    title = models.CharField(max_length=100)
    text = models.TextField(null=True, blank=True)
    view_amount = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def category_str(self):
        if self.category:
            return self.category.name
        return None


class Comment(models.Model):
    author = models.CharField(max_length=100)
    text = models.TextField()
    news = models.ForeignKey(News, on_delete=models.CASCADE,
                             related_name='news_comments')

    def __str__(self):
        return self.author
