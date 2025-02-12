from db import Database
from flask import Flask, render_template, abort

app = Flask(__name__)

# The homepage.
@app.route('/', methods = ['GET','POST'])
def home():
    meets_db = Database("meets.db")
    meets = meets_db.get_future_meets()
    groups = meets_db.get_groups()
    return render_template("home.html", meets=meets, groups=groups)

# Group info page.
@app.route("/group/<path:url>", methods = ['GET','POST'])
def group_info(url):
    meets_db = Database("meets.db")
    groups = meets_db.get_groups()

    for page_group in meets_db.get_groups():
        if (url == page_group[0].replace(" ","")):
            meets = meets_db.get_group_meets(page_group[0])
            return render_template("group-info.html", page_group=page_group, meets=meets, groups=groups)
    abort(404)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)