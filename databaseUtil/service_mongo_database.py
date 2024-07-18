import os
from os import listdir, walk


def addBook(collection):
    array = listdir('D:/py_proj/books')
    for author in array:
        for (dir_path, dir_names, file_names) in walk(f'D:/py_proj/books/{author}'):
            for file_name in file_names:
                print(file_name)
                book_item = {
                    'author': author,
                    'title': file_name,
                    'path': dir_path + "/" + file_name,
                    "language": 'russian',  # TODO detect language
                    'date': None
                }
                collection.insert_one(book_item)
    collection.create_index(name='index1', keys=[('title', "text"), ('author', 'text')], default_language='russian')


def deleteFiles():
    array = listdir('D:/py_proj/books')
    for author in array:
        for (dir_path, dir_names, file_names) in walk(f'D:/py_proj/books/{author}'):
            for file_name in file_names:
                size = os.path.getsize(f'D:/py_proj/books/{author}/{file_name}')
                if size < 60:
                    print(file_name, size)
                    os.remove(f'D:/py_proj/books/{author}/{file_name}')
                    if os.listdir('.'):
                        print('Have file here')
                    else:
                        pass
