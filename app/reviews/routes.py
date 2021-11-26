from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from app import db
from app.models import Review
from app.reviews.forms import ReviewForm
from app.reviews.utils import process_new_review_form

reviews = Blueprint("reviews", __name__)


@reviews.route("/reviews/new", methods=["GET", "POST"])
@login_required
def new_review():
    form = ReviewForm()
    if form.validate_on_submit():
        process_new_review_form(form)
        flash("The review has been posted", "success")
        return redirect(url_for("main.home"))
    return render_template(
        "create_review.html", title="Review an Article", legend="New Review", form=form
    )


@reviews.route("/reviews/<int:review_id>")
def review(review_id):
    review = Review.query.get_or_404(review_id)
    return render_template("review.html", review=review)


@reviews.route("/reviews/<int:review_id>/update", methods=["GET", "POST"])
@login_required
def update_review(review_id):
    review = Review.query.get_or_404(review_id)
    if review.author != current_user:
        abort(403)
    form = ReviewForm()
    if form.validate_on_submit():
        review.rating = form.rating.data
        review.content = form.content.data
        db.session.commit()
        flash("The review has been updated", "success")
        return redirect(url_for("reviews.review", review_id=review.id))
    elif request.method == "GET":
        form.url.data = review.article.url
        form.rating.data = review.rating
        form.content.data = review.content
    return render_template(
        "create_review.html", title="Update Review", legend="Update Review", form=form
    )


@reviews.route("/reviews/<int:review_id>/delete", methods=["POST"])
@login_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    if review.author != current_user:
        abort(403)
    db.session.delete(review)
    db.session.commit()
    flash("The review has been deleted", "success")
    return redirect(url_for("main.home"))
