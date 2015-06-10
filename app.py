from urlparse import urlparse

import github3

from flask import Flask
from flask import redirect, url_for, render_template


app = Flask(__name__)

@app.route("/")
def homepage():
    return "Welcome!"
    
@app.route("/gist/<path:gist_url>")
def gister(gist_url):
    # split off the username from things like: betatim/c4af33d04542f4306d38
    gist_url = gist_url.split("/")
    gist = github3.gist(gist_url[-1])
    
    return render_template("gist_display.html",
                           description=gist.description,
                           files=[f for f in gist.iter_files()])

@app.route("/url/<path:a_url>")
def urler(a_url):
    parsed_url = urlparse("http://" + a_url)

    if parsed_url.netloc == "gist.github.com":
        return redirect(url_for("gister", gisturl=parsed_url.path[1:]))

    else:
        return str(parsed_url)


if __name__ == "__main__":
    app.run(debug=True)
