import pytest
from allnc.middleware import Middleware


def test_basic_route_adding(app):
    @app.route("/home")
    def home(req, resp):
        resp.text = "Hello World"


def test_duplicat_routes_throws_exception(app):
    @app.route("/home")
    def home(req, resp):
        resp.text = "Hello World home2"

    with pytest.raises(AssertionError):
        @app.route("/home")
        def home2(req, resp):
            resp.text = "Hello World home2"


def test_request_can_be_sent_by_test_client(app, test_client):
    @app.route("/home")
    def home(req, resp):
        resp.text = "Hello from home"

    response = test_client.get("http://testserver/home")
    assert response.text == "Hello from home"


def test_parameterized_routing(app, test_client):
    @app.route("/hello/{name}")
    def greeting(request, response, name):
        response.text = f"Hello {name}"

    assert test_client.get("http://testserver/hello/John").text == "Hello John"
    assert test_client.get("http://testserver/hello/Musharraf").text == "Hello Musharraf"


def test_default_response(test_client):
    response = test_client.get("http://testserver/nonexistent")
    assert response.text == "Not Found."
    assert response.status_code == 404


def test_class_based_get(app, test_client):
    @app.route("/books")
    class Books:
        def get(self, req, resp):
            resp.text = "Books page"

    assert test_client.get("http://testserver/books").text == "Books page"


def test_class_based_post(app, test_client):
    @app.route("/books")
    class Books:
        def post(self, req, resp):
            resp.text = "Endpoint to create a  book"

    assert test_client.post("http://testserver/books").text == "Endpoint to create a  book"


def test_class_based_method_not_Allowed(app, test_client):
    @app.route("/books")
    class Books:
        def post(self, req, resp):
            resp.text = "Endpoint to create a  book"

    response = test_client.get("http://testserver/books")
    assert response.text == "Method Not Allowed"

    assert response.status_code == 405


def test_alternative_route_adding(app, test_client):
    def new_handler(req, resp):
        resp.text = "From new Handler"

    app.add_route("/new-handler", new_handler)
    assert test_client.get("http://testserver/new-handler").text == "From new Handler"


def test_template_handler(app, test_client):
    @app.route("/new-template")
    def template(req, resp):
        resp.body = app.template(
            "test.html",
            context={"new_title": "Best title", "new_body": "Best body"},
        )

    response = test_client.get("http://testserver/new-template")
    assert "Best title" in response.text
    assert "Best body" in response.text
    assert "text/html" in response.headers["Content-Type"]


def test_custom_exception_handler(app, test_client):
    def on_exception(req, resp, exc):
        resp.text = "Something bad happened"

    app.add_exception_handler(on_exception)

    @app.route("/exception")
    def exception_throwing_handler(req, resp):
        raise AttributeError("some exception")

    response = test_client.get("http://testserver/exception")
    assert response.text == "Something bad happened"


def test_non_existent_static_file(test_client):
    assert test_client.get("http://testserver/static/nonexistent.css").status_code == 404


def test_serving_static_file(test_client):
    response = test_client.get("http://testserver/static/test.css")
    assert response.text == "body { background-color: chocolate;}"


def test_middleware_method_are_called(app, test_client):
    process_request_called = False
    process_response_called = False

    class SimpleMiddleware(Middleware):

        def __init__(self, app):
            super().__init__(app)

        def process_request(self, req):
            nonlocal process_request_called
            process_request_called = True

        def process_response(self, req, resp):
            nonlocal process_response_called
            process_response_called = True

    app.add_middleware(SimpleMiddleware)

    @app.route("/home")
    def index(req, resp):
        resp.text = "from handler"

    resp = test_client.get("http://testserver/home")

    assert process_request_called is True
    assert process_response_called is True


def test_allowed_methods_for_function_based_handlers(app, test_client):
    @app.route("/home", allowed_methods=["post"])
    def home(req, resp):
        resp.text = "Hello from home"

    resp = test_client.get("http://testserver/home")

    assert resp.status_code == 405
    assert resp.text == "Method Not Allowed"


def test_json_response_helper(app, test_client):
    @app.route("/json")
    def json_handler(req, resp):
        resp.json = {"name": "allnc"}

    resp = test_client.get("http://testserver/json")
    resp_data = resp.json()

    assert resp.headers["Content-Type"] == "application/json"
    assert resp_data["name"] == "allnc"


def test_text_response_helper(app, test_client):
    @app.route("/text")
    def text_handler(req, resp):
        resp.text = "plain text"

    resp = test_client.get("http://testserver/text")

    assert "text/plain" in resp.headers["Content-Type"]
    assert resp.text == "plain text"


def test_html_response_helper(app, test_client):
    @app.route("/html")
    def html_handler(req, resp):
        resp.html = app.template(
            "test.html",
            context={"new_title": "Best title", "new_body": "Best body"},
        )

    response = test_client.get("http://testserver/html")

    assert "text/html" in response.headers["Content-Type"]
    assert "Best title" in response.text
    assert "Best body" in response.text
