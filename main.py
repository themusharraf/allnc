from allnc.app import AllNc
from allnc.middleware import Middleware

app = AllNc()


@app.route("/home", allowed_methods=["get"])
def home(request, response):
    response.text = "Hello from the Home Page"


@app.route("/about", allowed_methods=["put"])
def about(request, response):
    response.text = "Hello from the About Page"


@app.route("/hello/{name}")
def greeting(request, response, name):
    response.text = f"Hello {name}"


@app.route("/books")
class Books:
    def get(self, request, response):
        response.text = "Hello from the Books Page"

    def post(self, request, response):
        response.text = "Endpoint to create a  book"


def new_handler(req, resp):
    resp.text = "From new Handler"


app.add_route("/new-handler", new_handler)


@app.route("/template")
def template_handler(req, resp):
    resp.html = app.template(
        "home.html",
        context={"new_title": "Best title", "new_body": "Best body"},
    )


@app.route("/json")
def json_handler(req, resp):
    response_data = {"name": "some name", "type": "json"}
    resp.json = response_data


def on_exception(req, resp, exc):
    resp.text = str(exc)


app.add_exception_handler(on_exception)


@app.route("/exception")
def exception_throwing_handler(req, resp):
    raise AttributeError("some exception")


class LoggingMiddleware(Middleware):
    def __init__(self, app):
        super().__init__(app)

    def process_request(self, req):
        print("request is been called")

    def process_response(self, req, resp):
        print("response has been generated")


app.add_middleware(LoggingMiddleware)
