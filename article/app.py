from article import create_app
from article.config import Config

app = create_app(Config)


if __name__ == '__main__':
    app.run(debug=True)
