from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return '浩楠你好'

app.run()