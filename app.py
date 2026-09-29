from flask import Flask

app = Flask(
    __name__,
    template_folder="estudos/templates",
    static_folder="estudos/static"
)

from estudos.routes import routes

app.register_blueprint(routes)

print(app.url_map)

if __name__ == "__main__":
    app.run(debug=True)