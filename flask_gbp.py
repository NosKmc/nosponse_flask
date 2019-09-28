from flask import Flask, render_template, send_from_directory, Blueprint, request, json
import os
app = Flask(__name__, static_folder="static-folder")


def j_file2dic(_file):
    with open(_file, "r", encoding="utf-8") as filed:
        dic = json.load(filed)
    return dic
    

def dicjdump(dic, _file):
    with open(_file, "w", encoding="utf-8") as filed:
        json.dump(dic, filed, indent=4, ensure_ascii=False)


@app.route("/nosponse/")
def ret_nosponse():
    return send_from_directory("./nosponse", "index.html")


@app.route("/nosponse/responses.json")
def ret_responses():
    return send_from_directory("../", "responses.json")


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
