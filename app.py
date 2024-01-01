from flask import Flask, render_template, request, flash
from file_handler import upload_files, convert_to_docx
from indexer import tokenize_and_index
from search_engine import boolean_search, extended_boolean_search, vector_search

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'supersecretkey'  # Secret key for flash messages


@app.route('/')
def home():
    return render_template('indexing_settings.html')


@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            language = request.form.get('language')
            tokenization_algorithm = request.form.get('tokenization_algorithm')

            file_paths = upload_files(request)
            if not file_paths:
                flash('No files uploaded. Please select valid DOC files.', 'error')
                return render_template('indexing_settings.html')

            converted_paths = convert_to_docx(file_paths)
            if not converted_paths:
                flash('No valid DOC files to convert. Please upload valid DOC files.', 'error')
                return render_template('indexing_settings.html')

            tokenize_and_index(converted_paths, language, tokenization_algorithm)
            flash('Files indexed successfully!', 'success')
            return render_template('search_page.html')

        except Exception as e:
            flash(f"Error during indexing: {e}", 'error')

    return render_template('indexing_settings.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    try:
        query = request.args.get('query')
        algorithm = request.args.get('algorithm')

        if not query or not algorithm:
            flash('Invalid search query or algorithm selected.', 'error')
            return render_template('search_page.html')

        results = []
        if algorithm == 'boolean':
            results = boolean_search(query)
        elif algorithm == 'extended_boolean':
            results = extended_boolean_search(query)
        elif algorithm == 'vector':
            results = vector_search(query)

        if not results:
            flash('No matching results found.', 'info')
        return render_template('search_page.html', query=query, results=results)

    except Exception as e:
        flash(f"Error during search: {e}", 'error')
        return render_template('search_page.html')


if __name__ == '__main__':
    app.run(threaded=False)
