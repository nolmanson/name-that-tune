from flask import Flask, render_template
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template("image.html")

if __name__ == "__main__":
    app.run(debug=True)