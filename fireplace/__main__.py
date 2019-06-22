from .server import create_server

if __name__ == "__main__":
    app = create_server()
    app.run(host="::", port=8080)