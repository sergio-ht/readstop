from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, URLField
from wtforms.validators import DataRequired, NumberRange, URL


class ReviewForm(FlaskForm):
    url = StringField("Article's URL", validators=[DataRequired(), URL()])
    tags = StringField("Tags (comma separated)")
    rating = IntegerField(
        "Rating", validators=[DataRequired(), NumberRange(min=1, max=10)]
    )
    content = TextAreaField("Review", validators=[DataRequired()])
    submit = SubmitField("Post Review")
