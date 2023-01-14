import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS, cross_origin
import json

CREATE_AUTHORS_TABLE = (
    "CREATE TABLE IF NOT EXISTS authors (id SERIAL PRIMARY KEY, name TEXT);"
) #will only create if it doesnt already exist
CREATE_NOVELS_TABLE = """CREATE TABLE IF NOT EXISTS novels (author_id INTEGER, title TEXT, image_url TEXT, FOREIGN KEY(author_id) REFERENCES authors(id) ON DELETE CASCADE);""" #delete when parent is deleted



load_dotenv()

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

@app.post("/api/author")
def create_author():
    data = request.get_json(force=True)
    # print(data)
    name = data["name"]
    
    with connection:
        with connection.cursor() as cursor: # cursor is an object that allows us to insert data or iterate over rows
            cursor.execute(CREATE_AUTHORS_TABLE)
            cursor.execute("INSERT INTO authors (name) VALUES (%s) RETURNING id;", (name,))
            author_id = cursor.fetchone()[0]
    return {"id": author_id, "message": f"Author {name} created."}, 201


# @app.post("/api/novel")
# def add_novel():
#     data = request.get_json(force=True)
#     print(data)
#     title = data["title"]
#     image_url = data["image_url"]
#     author_name = data["author"]
#     with connection:
#         with connection.cursor() as cursor:
            # cursor.execute(f"SELECT id FROM authors WHERE authors.name='{author_name}'") #sql injection, fix later
            # author_id = cursor.fetchone()[0]
            # cursor.execute(CREATE_NOVELS_TABLE)
            # cursor.execute("INSERT INTO novels (author_id, title, image_url) VALUES (%s, %s, %s);", (author_id, title, image_url))
    
#     return [author_name, title, image_url], 201

@app.post("/api/novel")
def add_novel():
    data = request.get_json(force=True)
    title = data["title"]
    image_url = data["image_url"]
    author_name = data["author"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_AUTHORS_TABLE)
            cursor.execute("INSERT INTO authors (name) VALUES (%s) RETURNING id;", (author_name,))
            author_id = cursor.fetchone()[0]
            cursor.execute(CREATE_NOVELS_TABLE)
            cursor.execute("INSERT INTO novels (author_id, title, image_url) VALUES (%s, %s, %s);", (author_id, title, image_url))

    return [author_name, title, image_url], 201

@app.get("/api/novel")
def get_novels():
    with connection: 
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM authors JOIN novels ON authors.id = novels.author_id;")
            table = cursor.fetchall()
            print(table)
    # response = []
    # for arr in table:
    #     response.append(json.dumps({"author": arr[1], "title": arr[3], "image_url": arr[4]}))
    return table, 200



#for development:
@app.delete("/api/novel")
def delete_novel():
    # data = request.get_json(force=True)
    # print(data)
    # author_id = data["author_id"]
    # title = data["title"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM novels WHERE author_id=1;")
    return {"message": "Deleted 1"}, 202


@app.delete("/api/table")
def delete_table():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("DROP TABLE novels;")

    return {"message": "dropped table"}, 202