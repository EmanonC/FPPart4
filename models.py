from exts import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class UserSkills(db.Model):
    __tablename__ = 'user_skills'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)\

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    skill_user = db.relationship('User', backref=db.backref('skills'))

    skill_id=db.Column(db.Integer, db.ForeignKey('skill.id'))

class Skill(db.Model):
    __tablename__ = 'skill'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    skill_context = db.Column(db.String(200))
    skill_score=db.Column(db.Integer)

class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200))
    type=db.Column(db.String(200))

class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200))
    type=db.Column(db.String(200))

class CourseSkill(db.Model):
    __tablename__ = 'course_skill'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    course= db.relationship('Course', backref=db.backref('course_skill'))

    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'))

class UserCourse(db.Model):
    __tablename__ = 'user_course'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(200))
    status = db.Column(db.String(200))

    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    taked_course = db.relationship('User', backref=db.backref('taked_course'))

class JobPost(db.Model):
    __tablename__ = 'job_post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(200))
    href = db.Column(db.Text)
    requirement_num=db.Column(db.Integer)
    skill_num=db.Column(db.Integer)


    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    job_posts= db.relationship('Company', backref=db.backref('job_posts'))

class JobSkill(db.Model):
    __tablename__ = 'job_skill'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)


    job_post_id = db.Column(db.Integer, db.ForeignKey('job_post.id'))
    job_post= db.relationship('JobPost', backref=db.backref('job_skill'))

    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'))

class JobRequirement(db.Model):
    __tablename__ = 'job_requirement'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    context = db.Column(db.Text)

    job_post_id = db.Column(db.Integer, db.ForeignKey('job_post.id'))
    job_post= db.relationship('JobPost', backref=db.backref('job_requirement'))








class StorePlace(db.Model):
    __tablename__ = 'store_place'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200))
    type=db.Column(db.String(200))
    score=db.Column(db.Integer)
    status=db.Column(db.Integer)


class CollectedCards(db.Model):
    __tablename__ = 'collected_cards'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pull_from = db.Column(db.String(200))

    number_of_cards = db.Column(db.Integer, nullable=False)

    card_id = db.Column(db.Integer, db.ForeignKey('card.id'))
    stored_card= db.relationship('Card', backref=db.backref('owned_cards'))

    store_at  = db.Column(db.Integer, db.ForeignKey('store_place.id'))
    store_palce = db.relationship('StorePlace', backref=db.backref('storedcards'))

    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship('User', backref=db.backref('cards'))




class Set(db.Model):
    __tablename__ = 'set'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    set_name = db.Column(db.String(200), nullable=False)
    set_code = db.Column(db.String(200), nullable=False)
    set_ind=db.Column(db.String(20), nullable=False)
    series = db.Column(db.String(200), nullable=False)
    release_data = db.Column(db.DATE)


class Card(db.Model):
    __tablename__ = 'card'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    card_number = db.Column(db.String(200), nullable=False)

    card_name = db.Column(db.String(200), nullable=True)
    card_type = db.Column(db.String(200), nullable=True)
    card_subtype = db.Column(db.String(200), nullable=True)
    card_rarity = db.Column(db.String(200), nullable=True)

    is_standard = db.Column(db.Integer)

    set_id = db.Column(db.Integer, db.ForeignKey('set.id'))
    fromset = db.relationship('Set', backref=db.backref('cards'))


class CardText(db.Model):
    __tablename__ = 'card_text'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text, nullable=False)

    card_id = db.Column(db.Integer, db.ForeignKey('card.id'))
    fromcard = db.relationship('Card', backref=db.backref('TrEnTexts'))

class MoveText(db.Model):
    __tablename__ = 'move_text'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    energy_cost = db.Column(db.String(200), nullable=False)
    move_name = db.Column(db.String(200), nullable=False)
    move_damage = db.Column(db.String(20), nullable=True)
    move_text = db.Column(db.Text, nullable=True)


    card_id = db.Column(db.Integer, db.ForeignKey('card.id'))
    fromcard = db.relationship('Card', backref=db.backref('moves'))

class PokemonStats(db.Model):
    __tablename__ = 'pokemon_stats'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    pokemon_type = db.Column(db.String(200), nullable=True)
    weakness = db.Column(db.String(200), nullable=True)
    resistance = db.Column(db.String(200), nullable=True)
    retreat = db.Column(db.String(200), nullable=True)
    hp = db.Column(db.Integer, nullable=True)

    ability_name = db.Column(db.String(200), nullable=True)
    ability_text = db.Column(db.Text, nullable=True)

    card_id = db.Column(db.Integer, db.ForeignKey('card.id'))
    fromcard = db.relationship('Card', backref=db.backref('stats'))
