from flask import render_template, request, Blueprint
from app.models import Review

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get("page", 1, type=int)
    reviews = Review.query.order_by(Review.date_posted.desc()).paginate(
        page=page, per_page=6
    )
    return render_template("home.html", reviews=reviews, title="Home")
