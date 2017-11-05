from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html", navbar_elements=navbar_elements, title="gndi: The Best Place to Waste Your Money!")

@app.route("/about")
def about():
    return render_template("about.html", navbar_elements=navbar_elements)


if __name__ == "__main__":
    app.run(debug=True)