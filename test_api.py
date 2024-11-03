import pytest
import requests
from requests.auth import HTTPBasicAuth
import json
import time

from config_provider import ConfigProvider


def test_getBooks_gToken_whenNoApiAccessToken_shouldReturn403(context):
    # Given G-Token is not provided
    headers = { }

    # When all books are requested
    url = ConfigProvider.get_host() + "/books"
    response = requests.request("GET", url, headers=headers, data="")  

    # Then 403 is returned
    assert response.status_code == 403

def test_getBooks_gToken_whenValidApiAccessToken_shouldReturn200(context):
    # Given G-Token is provided
    headers = { 'g-token': ConfigProvider.get_g_token() }

    # When all books are requested
    url = ConfigProvider.get_host() + "/books"
    response = requests.request("GET", url, headers=headers, data="")  

    # Then 200 is returned
    assert response.status_code == 200

def test_getBooks_searchById_whenValidId_shouldReturnBook(context):
    # Given G-Token is provided
    headers = { 'g-token': ConfigProvider.get_g_token() }

    # When a book is requested by ID
    url = ConfigProvider.get_host() + "/books/1"
    response = requests.request("GET", url, headers=headers, data="")  

    # Then 200 is returned
    assert response.status_code == 200

    # And the ISBN of the returned book is 1593281056
    assert response.json()["isbn"] == '1593281056'

def test_getBooks_searchById_whenInvalidId_shouldReturn404(context):
    # Given G-Token is provided
    headers = { 'g-token': ConfigProvider.get_g_token() }

    # When a book is requested by an invalid ID
    url = ConfigProvider.get_host() + "/books/9999999999999999999999999999"
    response = requests.request("GET", url, headers=headers, data="")  

    # Then 404 is returned
    assert response.status_code == 404

def test_getBooks_searchByTitle_whenValidTitle_shouldReturnBook(context):
    # Given G-Token is provided
    headers = { 'g-token': ConfigProvider.get_g_token() }

    # When a book is requested by title
    params = "?title=The Screwtape Letters"
    url = ConfigProvider.get_host() + "/books" + params
    response = requests.request("GET", url, headers=headers, data="")  

    # Then 200 is returned
    assert response.status_code == 200

    # And the ISBN of the returned book is 0060652934
    assert response.json()[0]["isbn"] == '0060652934'

def test_getBooks_searchByTitle_whenInvalidTitle_shouldReturnNoBooks(context):
    # Given G-Token is provided
    headers = { 'g-token': ConfigProvider.get_g_token() }

    # When a book is requested by a title that does not exist
    params = "?title=This is not an existing book title"
    url = ConfigProvider.get_host() + "/books" + params
    response = requests.request("GET", url, headers=headers, data="")  

    # Then 200 is returned
    assert response.status_code == 200

    # And the response contains no books
    assert len(response.json()) == 0

def test_getBooks_searchByAuthor_whenValidAuthor_shouldReturnBook(context):
    # Given G-Token is provided
    headers = { 'g-token': ConfigProvider.get_g_token() }

    # When a book is requested by an author 
    params = "?author=Greg Bahnsen"
    url = ConfigProvider.get_host() + "/books" + params
    response = requests.request("GET", url, headers=headers, data="")  

    # Then 200 is returned
    assert response.status_code == 200

    # And the ISBN of the returned book is 0875520987
    assert response.json()[0]["isbn"] == '0875520987'

def test_getBooks_whenInvalidAuthor_shouldReturnNoBooks(context):
    # Given G-Token is provided
    headers = { 'g-token': ConfigProvider.get_g_token() }

    # When a book is requested by an author that does not exist
    params = "?author=This is not an existing author name"
    url = ConfigProvider.get_host() + "/books" + params
    response = requests.request("GET", url, headers=headers, data="")  

    # Then 200 is returned
    assert response.status_code == 200

    # And the response contains no books
    assert len(response.json()) == 0

def test_postBooks_addBook_whenValidRequest_shouldSuccessfullyAddBook(context):
    # Given a book to add
    unique = str(time.time()*1000000).replace('.','')
    title = "Automation Book " + unique
    author = "Automation Author " + unique
    isbn = "1234" + unique
    releaseDate = "2019-02-01"
    payload = json.dumps({
        "title": title,
        "author": author,
        "isbn": isbn,
        "releaseDate": releaseDate
        })

    # When a book is added
    url = ConfigProvider.get_host() + "/books"
    headers = {
        'g-token': 'ROM831ESV',
        'Content-Type': 'application/json',
        'Authorization': 'Basic Og=='
        }
    response = requests.request("POST", url, headers=headers, data=payload)
    context["book_ids"].append(response.json()["id"])

    # Then 201 is returned
    assert response.status_code == 201

    # And the response contains the added book
    assert response.json()["title"] == title
    assert response.json()["author"] == author
    assert response.json()["isbn"] == isbn
    assert response.json()["releaseDate"] == releaseDate

def test_deleteBooks_deleteBook_whenValidBasicAuth_shouldDeleteBook(context):
    # Given a book has been added
    unique = str(time.time()*1000000).replace('.','')
    title = "Automation Book " + unique
    author = "Automation Author " + unique
    isbn = "1234" + unique
    releaseDate = "2019-02-01"
    response = requests.request("POST", ConfigProvider.get_host() + "/books", headers={'g-token': 'ROM831ESV','Content-Type': 'application/json','Authorization': 'Basic Og=='}, data=json.dumps({"title": title,"author": author,"isbn": isbn,"releaseDate": releaseDate}))
    book_id = response.json()["id"]
    context["book_ids"].append(response.json()["id"])

    # And Basic Auth credentials are provided (the user has authorization to delete)
    auth = HTTPBasicAuth(ConfigProvider.get_username(), ConfigProvider.get_password())

    # When the book is deleted
    url = ConfigProvider.get_host() + "/books/" + str(book_id)
    headers = {
        'g-token': 'ROM831ESV',
        'Content-Type': 'application/json'
        }
    response = requests.request("DELETE", url, headers=headers, auth=auth)

    # Then 204 is returned
    assert response.status_code == 204

    # And the book is not found when requested
    url = ConfigProvider.get_host() + "/books/" + str(book_id)
    headers = { 'g-token': ConfigProvider.get_g_token() }
    response = requests.request("GET", url, headers=headers, data="")
    assert response.status_code == 404


def test_deleteBooks_deleteBook_whenInvalidBasicAuth_shouldNotDeleteBook(context):
    # Given a book has been added
    unique = str(time.time()*1000000).replace('.','')
    title = "Automation Book " + unique
    author = "Automation Author " + unique
    isbn = "1234" + unique
    releaseDate = "2019-02-01"
    response = requests.request("POST", ConfigProvider.get_host() + "/books", headers={'g-token': 'ROM831ESV','Content-Type': 'application/json','Authorization': 'Basic Og=='}, data=json.dumps({"title": title,"author": author,"isbn": isbn,"releaseDate": releaseDate}))
    book_id = response.json()["id"]
    context["book_ids"].append(response.json()["id"])

    # And Basic Auth credentials is not provided
    auth = None

    # When the book is deleted
    url = ConfigProvider.get_host() + "/books/" + str(book_id)
    headers = {
        'g-token': 'ROM831ESV',
        'Content-Type': 'application/json'
        }
    response = requests.request("DELETE", url, headers=headers)

    # Then 401 is returned
    assert response.status_code == 401

    # And the book is found when requested
    url = ConfigProvider.get_host() + "/books/" + str(book_id)
    headers = { 'g-token': ConfigProvider.get_g_token() }
    response = requests.request("GET", url, headers=headers, data="")
    assert response.status_code == 200
    