from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search_news():
    query = request.form.get("news_query")
    # Yaha aap backend logic likh sakte ho (API call, DB check etc.)
    result = f"'{query}' ka verification result yaha show hoga."
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
