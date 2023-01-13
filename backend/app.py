import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request

CREATE_AUTHORS_TABLE = (
    "CREATE TABLE IF NOT EXISTS authors (id SERIAL PRIMARY KEY, name TEXT);"
) #will only create if it doesnt already exist
CREATE_NOVELS_TABLE = """CREATE TABLE IF NOT EXISTS novels (author_id INTEGER, title TEXT, chapters INTEGER, FOREIGN KEY(author_id) REFERENCES authors(id) ON DELETE CASCADE);""" #delete when parent is deleted



load_dotenv()

app = Flask(__name__)
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


@app.post("/api/novel")
def add_novel():
    data = request.get_json(force=True)
    print(data)
    title = data["title"]
    chapters = data["chapters"]
    author_id = data["author"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_NOVELS_TABLE)
            cursor.execute("INSERT INTO novels (author_id, title, chapters) VALUES (%s, %s, %s)", (author_id, title, chapters))

    return {"message": "Novel added."}, 201


@app.get("/api/novel")
def get_novels():
    with connection: 
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM authors JOIN novels ON authors.id = novels.author_id")
            table = cursor.fetchall()
            print(table)
    return {"message": table}, 200
