import sqlite3
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

nltk.download('punkt')
nltk.download('stopwords')


def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS indexed_documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT,
                indexed_content TEXT,
                language TEXT,
                tokenization_algorithm TEXT
            )
        ''')
        connection.commit()
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")


def connect_to_database():
    return sqlite3.connect('database.db')


def insert_indexed_data(connection, file_path, indexed_content, language, tokenization_algorithm):
    try:
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO indexed_documents (file_path, indexed_content, language, tokenization_algorithm)
            VALUES (?, ?, ?, ?)
        ''', (file_path, ' '.join(indexed_content), language, tokenization_algorithm))
        connection.commit()
    except sqlite3.Error as e:
        print(f"Error inserting indexed data: {e}")


def search_in_database(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute('''
            SELECT file_path FROM indexed_documents
            WHERE lower(indexed_content) LIKE ?
        ''', ('%' + query.lower() + '%',))
        results = cursor.fetchall()
        return [result[0] for result in results]
    except sqlite3.Error as e:
        print(f"Error searching in database: {e}")
        return []


def tokenize(content, language, tokenization_algorithm):
    tokens = []
    if tokenization_algorithm == 'Whitespace':
        tokens = content.split()
    elif tokenization_algorithm == 'Word Tokenization':
        tokens = word_tokenize(content)

    if language == 'english':
        stop_words = set(stopwords.words('english'))
        tokens = [token for token in tokens if token.lower() not in stop_words]
    elif language == 'arabic':
        tokenizer = RegexpTokenizer(r'\b\w+\b')
        tokens = tokenizer.tokenize(content)

    return tokens


def read_file_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content


def tokenize_and_index(file_paths, language, tokenization_algorithm):
    try:
        conn = connect_to_database()
        create_table(conn)
        for file_path in file_paths:
            content = read_file_content(file_path)
            indexed_content = tokenize(content, language, tokenization_algorithm)
            insert_indexed_data(conn, file_path, indexed_content, language, tokenization_algorithm)
        conn.close()
    except Exception as e:
        print(f"Error tokenizing and indexing: {e}")
        # Handle error as needed
