
from rest_framework import serializers

from .models import Author, Book, Page


class PageSerializer(serializers.ModelSerializer):
    page_number = serializers.SerializerMethodField('pagenum')

    #
    def pagenum(self, page):
        # Get the author object that is associated with the book
        pagenum = page.number
        return pagenum

    class Meta:
        model = Page
        fields = ['author', 'book', 'page_number', 'content']


class BookSerializer(serializers.ModelSerializer):
    # authorname = serializers.SerializerMethodField('nameauthor')
    #
    # def nameauthor(self, book):
    #     # Get the author object that is associated with the book
    #     authorname = book.author.name
    #     return authorname


    class Meta:
        model = Book
        fields = ['author', 'name', 'title']


class AuthorSerializer(serializers.ModelSerializer):
    # books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


"""
{
"id": 1,
"name": "ahmed",
"email": "ahmed@gmail.com",
"password": "ahmed@2001"
}
{
"id": 2
"name": "ahmed2001",
"email": "ahmed2001@gmail.com",
"password": "ahmed@2001"
}
"""