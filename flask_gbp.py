from flask import Flask, render_template, send_from_directory, Blueprint, request, json, jsonify
import os
import sqlite3
responses_db_path = "../nosponse/responses.sqlite3"
app = Flask(__name__, static_folder="static-folder")


def j_file2dic(_file):
    with open(_file, "r", encoding="utf-8") as filed:
        dic = json.load(filed)
    return dic


def load_responses(responses_db_path):
    conn = sqlite3.connect(responses_db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('select * from response')
    data = c.fetchall()
    conn.close()
    responses = dict()
    for row in data:
        responses[row['msg']] = responses.get(row['msg'], []) + [row['response']]
    return responses


def dicjdump(dic, _file):
    with open(_file, "w", encoding="utf-8") as filed:
        json.dump(dic, filed, indent=4, ensure_ascii=False)


@app.route("/nosponse/")
def ret_nosponse():
    return send_from_directory("./nosponse", "index.html")


@app.route("/nosponse/responses.json")
def ret_responses():
    data = load_responses(responses_db_path)
    return jsonify(data)


@app.route('/nosponse/<path:path>')
def serve_static(path):
    p = os.path.dirname(path)
    file = os.path.basename(path)
    return send_from_directory('./nosponse/' + p + "/", file)


@app.route('/service-worker.js')
def serve_worker():
    return send_from_directory('./nosponse', 'service-worker.js')


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8000)
