from flask import Flask, redirect, url_for, render_template
# from flask_bootstrap import Bootstrap

app = Flask(__name__)
# Bootstrap(app)
@app.route("/") 
def home():
    return render_template("index.html", title = "HOME", id = "home")

@app.route("/consult") 
def consult():
    return render_template("consult.html", title = "CONSULT", id = "consult")

@app.route("/respect") 
def respect():
    return render_template("respect.html", title = "RESPECT", id = "respect")

@app.route("/apples") 
def apples():
    return render_template("apples.html", title = "APPLES", id = "apples")

@app.route("/misa") 
def misa():
    return render_template("misa.html", title = "MISA", id = "misa")

if __name__ == "__main__":
    app.run(debug=True)