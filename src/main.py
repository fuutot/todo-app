from app import create_app # __init__さきに走る

app = create_app()

if __name__ == '__main__':
    app.run()
