from app import app

if __name__ == "__main__":
    print("👉 Space Data Analyzer starting (🚀)")
    app.run(host="0.0.0.0", port=8000, debug=True)
