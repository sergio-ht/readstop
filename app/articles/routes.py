from flask import render_template, Blueprint

from app.models import Article, Tag

articles = Blueprint("articles", __name__)


@articles.route("/article/<int:article_id>")
def article(article_id):
    article = Article.query.get_or_404(article_id)
    tags = article.tags
    tags = [tag.name for tag in tags]
    avg_rating = article_average_rating(article)

    return render_template(
        "article.html", article=article, tags=tags, avg_rating=avg_rating
    )


@articles.route("/tag/<string:tag_name>")
def tag(tag_name):
    tag = Tag.query.filter_by(name=tag_name).first()
    if not tag:
        return "not an existing tag"
    articles = tag.articles
    c = len(articles)
    print(f"total articles: {c}")

    return render_template("tag.html", articles=articles, tag=tag)


def article_average_rating(article):
    ratings = article.reviews
    ratings = [review.rating for review in ratings]
    total = sum(ratings)
    return total / len(ratings)
