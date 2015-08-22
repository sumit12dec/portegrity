from flask import Flask
app = Flask(__name__)


from flask import Flask, session, jsonify, render_template,request
from flask.sessions import SessionInterface
from beaker.middleware import SessionMiddleware

session_opts = {
    'session.type': 'ext:memcached',
    'session.url': '127.0.0.1:11211',
    'session.data_dir': './cache',
}

class BeakerSessionInterface(SessionInterface):
    def open_session(self, app, request):
        session = request.environ['beaker.session']
        return session

    def save_session(self, app, session, response):
        session.save()


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("pro.html")


@app.route('/cpu')
def cpu():
    import psutil
    a = psutil.virtual_memory()
    b = psutil.disk_usage('/')
    print a.total

    res = {
    'Total Virtual Memory': int(a.total)/(1024*1024),
    'Available Virtual Memory': int(a.available)/(1024*1024),
    'Percent Virtual Memory': int(a.percent),
    'CPU Count': int(psutil.cpu_count()),
    'Total Disk Memory': int(b.total)/(1024*1024),
    'Available Disk Memory': int(b.free)/(1024*1024),
    'Percent Disk Memory': int(b.percent),
    }

    return jsonify(**res)

@app.route('/addbook')
def add_book():
    book_name = request.args.get('book_name')
    if not session.has_key(book_name):
        session[book_name] = book_name    
        return "Book added to Session value"

@app.route('/deletebook')
def delete_book():
    book_name = request.args.get('book_name')
    if session.has_key(book_name):
        print session
        del session[book_name]    
        return "Book deleted from Session value"

@app.route('/list_book')
def list_book():
    return jsonify(**session)



if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True)
    app.wsgi_app = SessionMiddleware(app.wsgi_app, session_opts)
    app.session_interface = BeakerSessionInterface()
