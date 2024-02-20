from fcfmramos import db


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(
        db.Integer, db.ForeignKey("course.id"), nullable=False
    )
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)


class ReviewDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(
        db.Integer, db.ForeignKey("review.id"), nullable=False
    )
    difficulty = db.Column(db.Integer, nullable=False)
    workload = db.Column(db.Integer, nullable=False)
    enjoyment = db.Column(db.Integer, nullable=False)


class ReviewText(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(
        db.Integer, db.ForeignKey("review.id"), nullable=False
    )
    description = db.Column(db.Text, nullable=False)
    opinion = db.Column(db.Text, nullable=False)


class ReviewLikes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(
        db.Integer, db.ForeignKey("review.id"), nullable=False
    )
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    liked = db.Column(db.Boolean, nullable=False)
