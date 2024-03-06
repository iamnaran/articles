from article import create_app
from article.config import Config

app = create_app(Config)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
