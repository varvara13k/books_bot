import flask
import pandas as pd
import database
from datetime import datetime

app = flask.Flask(__name__)

@app.route('/download/<book_id>')
def book_info(book_id):
    db = database.dbapi.DatabaseConnector()
    stats = db.get_book_stats(book_id)
    stats_dict = {
    "borrow_id": [s.borrow_id for s in stats],
    "book_id": [s.book_id for s in stats],
    "date_start": [s.date_start for s in stats],
    "date_end": [s.date_end for s in stats],
    "user_id": [s.user_id for s in stats]
    }
    df = pd.DataFrame(stats_dict)
    file_name = "Statistic.xlsx"
    df.to_excel(file_name, index=False)
    return flask.send_file(file_name, as_attachment=True)

app.run('0.0.0.0', port=8080, debug=True)