from flask import Flask, render_template

app = Flask(
    __name__,
    template_folder="estudos/templates",
    static_folder="estudos/static"
)


@app.route("/")
def inicio():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)