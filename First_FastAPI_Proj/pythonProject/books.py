from fastapi import FastAPI, Body

app = FastAPI()


BOOKS = [

    {'title':"Title 1", 'author':"author 1", 'category':"science"},
    {'title': "Title 2", 'author': "author 2", 'category': "history"},
    {'title': "Title 3", 'author': "author 3", 'category': "history"},
    {'title': "Title 4", 'author': "author 4", 'category': "maths"},
    {'title': "Title 5", 'author': "author 5", 'category': "science"},
    {'title': "Title 6", 'author': "author 2", 'category': "history"}
]

@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get('/books/')
async def query_category(category:str):
    arr = []
    for book in BOOKS:

        if category.casefold() == book.get("category").casefold():
            arr.append(book)
    return arr

'''
@app.get("/books/{dynamic_param}")
async def read_book(dynamic_param: str):
    return{'dynamic_param':dynamic_param}
'''

@app.get("/books/{dynamic_param}")
async def read_book(title: str):

    for book in BOOKS:

        if title.casefold() == book.get("title").casefold():
            return book

@app.get("/books/{dynamic_param}/")
async def read_book(author: str, category: str):
    arr = []
    for book in BOOKS:

        if author.casefold() == book.get("author").casefold() and category.casefold() == book.get("category").casefold():
            arr.append(book)
    return arr

@app.post('/books/create_books')
async def create_book(new=Body()):
    BOOKS.append(new)


@app.put('/books/update_book')
async  def update_book(update = Body()):

    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == update.get("title").casefold:
            BOOKS[i]=update



@app.delete('/books/del_book/{book_title}')
async  def delete_book(book_title:str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break