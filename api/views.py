from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Author, Book, Page
from .serializers import AuthorSerializer, BookSerializer, PageSerializer

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime


# Create your views here.
# It is used to list the books for the reader
class BookList(APIView):
    def get(self, request):
        book = Book.objects.all()
        serializer = BookSerializer(book, many=True)
        return Response(serializer.data)


class BookAuthorName(APIView):
    def get(self, request, name):
        book = Book.objects.filter(name=name)
        serializer = BookSerializer(book, many=True)
        return Response(serializer.data)


class Pages(APIView):
    def get(self, request):
        pages = Page.objects.all()
        serializer = PageSerializer(pages, many=True)
        return Response(serializer.data)

class PageId(APIView):
    def get(self, request, book_id, page_number):

        if not book_id or not page_number:
            return Response({'error': 'Invalid data. Both book_id and the page are required.'}, status=400)

        try:
            page = Page.objects.get(number=page_number, book_id=book_id)
        except Page.DoesNotExist:
            return Response({'error': 'Page does not exist.'}, status=404)

        serializer = PageSerializer(page)
        return Response(serializer.data)


#######################################

class RegisterAuthor(APIView):
    def post(self, request):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAuthor(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = Author.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        # token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        decoded_token = jwt.decode(token, 'secret', algorithms=['HS256'])

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': decoded_token
        }
        return response

###########
class AuthorView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = Book.objects.filter(id=payload['id']).first()
        serializer = BookSerializer(user)
        return Response(serializer.data)

    ###################
    # add post method to edit the book with pages
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = Author.objects.filter(id=payload['id']).first()

        book_id = request.data.get('book_id')
        pages = request.data.get('pages')

        if not book_id or not pages:
            return Response({'error': 'Invalid data. Both book_id and pages are required.'}, status=400)

        book = Book.objects.filter(id=book_id, author=user).first()

        if not book:
            return Response({'error': 'Book not found.'}, status=404)

        page_ids = [page.get('id') for page in pages]

        # Delete existing pages not present in the updated list
        Page.objects.filter(book=book).exclude(id__in=page_ids).delete()

        for page_data in pages:
            page_id = page_data.get('id')
            page_number = page_data.get('number')

            if not page_number:
                return Response({'error': 'Invalid page data. Page number is required.'}, status=400)

            if page_id:
                # Update existing page
                page = Page.objects.filter(id=page_id, book=book).first()
                if not page:
                    return Response({'error': 'Page not found.'}, status=404)
                page.number = page_number
                page.save()
            else:
                # Create new page
                page = Page(book=book, number=page_number)
                page.save()

        serializer = BookSerializer(book)
        return Response(serializer.data)

#############
class AuthorAddBook(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = Book.objects.filter(id=payload['id']).first()

        print(user.id)
        print(user.name)
        print(user.author)
        print(user.title)
        print(user)

        print(request.data)

        temp_data = {
            'author': user.id,  # Assign the ID of the user as the author_id
            'name': user.name,
            'title': request.data['title']
        }

        print(temp_data)
        serializer = BookSerializer(data=temp_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    """
        {
        "id": 2,
        "name": "Mark2",
        "title": "Book Mark2"
        }
    """

"""
Add the pages of the book with its content.
"""
class AuthorAddPages(APIView):

    pages = Page.objects.all()
    serializer = PageSerializer(pages, many=True)

    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = Book.objects.filter(id=payload['id']).first()
        book_id = Page.objects.filter(id=request.data['book_id']).first()

        # print(Page)
        # number = Page.objects.filter(id=Page.number)
        # user = Page.objects.all()
        print(user)

        temp_data = {
            'author': user.id,
            'book': book_id.id,
            # 'page_number': 1,
            'content': request.data['content']
        }

        serializer = PageSerializer(data=temp_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = Author.objects.filter(id=payload['id']).first()
        book_id=request.data["book_id"]
        page_number = request.data["page_number"]

        print("User", user.id)
        print("book_id", book_id)
        print("page_number", page_number)

        if not book_id or not page_number:
            return Response({'error': 'Invalid data. Both book_id and the page are required.'}, status=400)
        try:
            page = Page.objects.get(number=page_number, book_id=book_id)
        except Page.DoesNotExist:
            return Response({'error': 'Page does not exist.'}, status=404)
        page.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# class AuthorEidtPage(APIView):
#     def get(self, request, book_id, page_id):
#         token = request.COOKIES.get('jwt')
#
#         if not token:
#             raise AuthenticationFailed('Unauthenticated!')
#         try:
#             payload = jwt.decode(token, 'secret', algorithms=['HS256'])
#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed('Unauthenticated!')
#
#         pages = Page.objects.all()
#         serializer = PageSerializer(pages, many=True)
#         print("Serializer", serializer)
#
#         author = Author.objects.filter(id=payload['id']).first()
#         book = Book.objects.filter(id=book_id)
#         page = Page.objects.filter(book__page=page_id)
#         # print("Author id", author.id)
#         # print("Book id", book.query)
#         # print("Page id", page)
#
#         serializer = PageSerializer(page)
#         print("serializer", serializer.data)
#         return Response("Get from Author edit page")
#
#
#     def get_queryset(self):
#         queryset = Page.objects.all()  # Replace YourModel with your actual model
#         return queryset
#
#     def get_object(self, pk):
#         try:
#             return Page.objects.get(pk=pk)
#         except Page.DoesNotExists:
#             raise Http404
#
#     def put(self, request, pk):
#         token = request.COOKIES.get('jwt')
#
#         if not token:
#             raise AuthenticationFailed('Unauthenticated!')
#         try:
#             payload = jwt.decode(token, 'secret', algorithms=['HS256'])
#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed('Unauthenticated!')
#
#         user = Book.objects.filter(id=payload['id']).first()
#         book_id = Page.objects.filter(id=request.data['book_id']).first()
#         print(pk)
#
#         temp_data = {
#             'author': user.id,
#             'book': book_id.id,
#             # 'page_number': 1,
#             'content': request.data['content']
#         }
#
#         page = self.get_object(pk)
#         serializer = PageSerializer(page, data=temp_data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""
{
"number": 1,
"content": "Introduction from author author 3 "
}
"""

class AuthorEidtPage(APIView):
    def put(self, request, book_id, page_number):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = Author.objects.filter(id=payload['id']).first()
        print("User", user.id)

        if not book_id or not page_number:
            return Response({'error': 'Invalid data. Both book_id and the page are required.'}, status=400)

        page_num=Page.objects.get(number=page_number, book_id=book_id, author=payload['id'])
        print(page_num)
        temp_data = {
            'author': user.id,
            'book': book_id,
            'page_number': page_number,
            'content': request.data['content']
        }

        serializer = PageSerializer(page_num, data=temp_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



##########


class LogoutAuthor(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response

