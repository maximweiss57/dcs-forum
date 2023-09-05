from app import create_app

app = create_app(status='development')

if __name__ == "__main__":
    app.run(debug=True)
