from flask_login import current_user
from app import db
from app.models import Review, Article, Tag
from app.articles.utils import get_article_html


def process_new_review_form(form):
    # process article
    article_id = process_article(form.url.data)
    # process tags
    tags = process_tags(form.tags.data)
    # add tags to article
    add_tags_to_article(article_id, tags)

    review = Review(
        rating=form.rating.data,
        content=form.content.data,
        author=current_user,
        article_id=article_id,
    )
    db.session.add(review)
    db.session.commit()


def process_article(url):
    article = Article.query.filter_by(url=url).first()
    if article:
        return article.id
    title, image_file = get_article_html(url)
    if title and image_file:
        article = Article(url=url, title=title, image_file=image_file)
    elif title:
        article = Article(url=url, title=title)
    elif image_file:
        article = Article(url=url, image_file=image_file)
    else:
        article = Article(url=url)
    db.session.add(article)
    db.session.commit()
    return article.id


def process_tags(tags_string):
    tags_string = tags_string.split(",")
    tags = []
    for tag in tags_string:
        tag = tag.strip()
        # search if tag exists
        existent_tag = Tag.query.filter_by(name=tag).first()
        if not existent_tag:
            new_tag = Tag(name=tag)
            db.session.add(new_tag)
            db.session.commit()
            tags.append(new_tag.id)
        else:
            tags.append(existent_tag.id)
    return tags


def add_tags_to_article(article_id, tag_list):
    if not tag_list:
        return
    article = Article.query.get(article_id)
    for tag_id in tag_list:
        tag = Tag.query.get(tag_id)
        article.tags.append(tag)
