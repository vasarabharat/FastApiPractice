from fastapi  import FastAPI

app = FastAPI()


BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]


@app.get("/")
async def home_page():
    return {"message":"Hellow worlds!!"}

@app.get("/books")
async def get_all_books():
    return BOOKS


# query parameters
@app.get("/books/")
async def get_books_category(category):
    return {"Message": "User requesed {category} category "}

@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and \
                book.get('category').casefold() == category.casefold():
            books_to_return.append(book)

    return books_to_return


#NOTE: in fast api url mapping will be in chronological order so all dynamic urls must be at bottom and all fixed url are on top otherwise it will execute with dynamic variable 

# if this method will written after dynamic url then it will never trigger because it treat 1 as dynamic value and it will execute that method.
@app.get("/books/1")
async def get_book_one():
    return BOOKS[0]


# dynamic url sample. 
@app.get("/books/{book_title}")
async def get_book_title(book_title: str):
    for book in BOOKS:
        if book_title.lower() == book.get('title').lower():
            return book
        
    return {"Message": f"{book_title} not found in our list"}



# we need to import Body from fastapi to use body of a post method
from fastapi import Body


# here in this example we have to use /docs url to send a body. use exact same dictionary so it will add new book into our books variable
# ex use exact same dict: {"title": "Title Seven", "author": "Author Three", "category": "Science"}
@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)


@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book


@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break
