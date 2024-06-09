![Screenshot from 2024-05-27 15-02-59](https://github.com/themusharraf/allnc/assets/122869450/859d4911-8e2b-45d3-af78-ff64cd51ff4a)
       
   
 
![purpose](https://img.shields.io/badge/purpose-learning-green.svg) ![coverage](https://img.shields.io/badge/coverage-100-green)   ![PyPI - Version](https://img.shields.io/pypi/v/allnc)   
  
# AllNc         
 
AllNc is a Python Web Framework built for learning purposes. The plan is to learn how frameworks
are built by implementing their features, writing blog posts about them and keeping the codebase  
as simple as possible.

It is a WSGI framework and can be used with any WSGI application server such as Gunicorn.

    
## Installation

```shell
pip install allnc
```
   
  
## How to use it
asic Usage:

```python
# app.py
from allnc.app import AllNc
from allnc.middleware import Middleware

app = AllNc()


@app.route("/home")
def home(request, response):
    response.text = "Hello from the Home Page"


@app.route("/about")
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

```

Start:

```bash
gunicorn app:app
```

## Handlers

If you use class based handlers, only the methods that you implement will be allowed:

```python
@app.route("/hello/{name}")
def greeting(request, response, name):
    response.text = f"Hello {name}"
```

This handler will only allow `GET` requests. That is, `POST` and others will be rejected. The same thing can be done with
function based handlers in the following way:

```python
@app.route("/", methods=["get"])
def home(req, resp):
    resp.text = "Hello, this is a home page."
```

Note that if you specify `methods` for class based handlers, they will be ignored.

## Unit Tests

The recommended way of writing unit tests is with [pytest](https://docs.pytest.org/en/latest/). There are two built in fixtures
that you may want to use when writing unit tests with AllNc. The first one is `app` which is an instance of the main `AllNc` class:

```python
def test_route_overlap_throws_exception(app):
    @app.route("/")
    def home(req, resp):
        resp.text = "Welcome Home."

    with pytest.raises(AssertionError):
        @app.route("/")
        def home2(req, resp):
            resp.text = "Welcome Home2."
```

The other one is `client` that you can use to send HTTP requests to your handlers. It is based on the famous [requests](http://docs.python-requests.org/en/master/) and it should feel very familiar:

```python
def test_parameterized_routing(app, test_client):
    @app.route("/hello/{name}")
    def greeting(request, response, name):
        response.text = f"Hello {name}"

    assert test_client.get("http://testserver/hello/John").text == "Hello John"
    assert test_client.get("http://testserver/hello/Musharraf").text == "Hello Musharraf"
```



## Templates

The default folder for templates is `templates`. You can change it when initializing the main `AllNc()` class:

```python
app = AllNc(templates_dir="templates_dir_name")
```

Then you can use HTML files in that folder like so in a handler:

```python
@app.route("/show/template")
def handler_with_template(req, resp):
    resp.html = app.template("example.html", context={"title": "Awesome Framework", "body": "welcome to the future!"})
```

## Static Files

Just like templates, the default folder for static files is `static` and you can override it:

```python
app = AllNc(static_dir="static_dir_name")
```

Then you can use the files inside this folder in HTML files:

```html
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <title>{{title}}</title>

  <link href="/static/main.css" rel="stylesheet" type="text/css">
</head>

<body>
    <h1>{{body}}</h1>
    <p>This is a paragraph</p>
</body>
</html>
```

## Custom Exception Handler

Sometimes, depending on the exception raised, you may want to do a certain action. For such cases, you can register an exception handler:

```python
def on_exception(req, resp, exception):
    if isinstance(exception, HTTPError):
        if exception.status == 404:
            resp.text = "Unfortunately the thing you were looking for was not found"
        else:
            resp.text = str(exception)
    else:
        # unexpected exceptions
        if app.debug:
            debug_exception_handler(req, resp, exception)
        else:
            print("These unexpected exceptions should be logged.")

app = AllNc(debug=False)
app.add_exception_handler(on_exception)
```

This exception handler will catch 404 HTTPErrors and change the text to `"Unfortunately the thing you were looking for was not found"`. For other HTTPErrors, it will simply
show the exception message. If the raised exception is not an HTTPError and if `debug` is set to True, it will show the exception and its traceback. Otherwise, it will log it.

## Middleware

You can create custom middleware classes by inheriting from the `allnc.middleware.Middleware` class and override its two methods
that are called before and after each request:

```python
from allnc.app import AllNc
from allnc.middleware import Middleware

app = AllNc()


class SimpleCustomMiddleware(Middleware):
    def process_request(self, req):
        print("Before dispatch", req.url)

    def process_response(self, req, res):
        print("After dispatch", req.url)


app.add_middleware(SimpleCustomMiddleware)
```


## Features

- WSGI compatible
- Built-in ORM
- Parameterized and basic routing
- Class based handlers
- Test Client
- Support for templates
- Support for static files
- Custom exception handler
- Middleware

## Note

It is extremely raw and will hopefully keep improving. If you are interested in knowing how a particular feature is implemented in other
frameworks, please open an issue and we will hopefully implement and explain it in a blog post
