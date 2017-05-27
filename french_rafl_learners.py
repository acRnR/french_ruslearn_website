import conf
import os
import random
from flask import Flask
from flask_mail import Mail
from flask import url_for, render_template, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.sql import select

"""---------------- Настройки конфигураций и создание связи с базой данных пользователей ----------------------------"""
sess_2 = {}
mail = Mail()

app = Flask(__name__)

app.secret_key = os.urandom(24)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userinfo.db'
app.config['SECURITY_REGISTERABLE'] = True
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = conf.MAILUN
app.config['MAIL_PASSWORD'] = conf.PASSWORD
mail.init_app(app)

db = SQLAlchemy(app)

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


"""--------------------------Функции, получающие данные для выведения на страницах сайта-----------------------------"""


def distance(a, b):
    # "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        a, b = b, a
        n, m = m, n
    current_row = range(n+1)
    for i in range(1, m+1):
        previous_row, current_row = current_row, [i]+[0]*n
        for j in range(1,n+1):
            add, delete, change = previous_row[j]+1, current_row[j-1]+1, previous_row[j-1]
            if a[j-1] != b[i-1]:
                change += 1
            current_row[j] = min(add, delete, change)
    return current_row[n]


def call_db(tbl):
    class Words(object):
        pass
    db_path = 'voc.db'
    engine = create_engine('sqlite:///%s' % db_path, echo=False)
    metadata = MetaData(engine)
    need = Table(tbl, metadata, autoload=True)
    mapper(Words, need)
    sessionmaker(bind=engine)
    conn = engine.connect()
    s = select([need])
    result = conn.execute(s)
    return result


def useremailget():
    db_path = 'userinfo.db'
    engine = create_engine('sqlite:///%s' % db_path, echo=False)
    metadata = MetaData(engine)
    need = Table('User', metadata, autoload=True)
    sessionmaker(bind=engine)
    conn = engine.connect()
    s = select([need])
    result = conn.execute(s)
    for row in result:
        if str(row['id']) == str(session['user_id']):
            return row['email']
        else:
            return 'l\'internaute n\'est pas défini'


def voc_maker(ps, categories):
    result = call_db('rus_words')
    d = sorting(result, ps, categories)
    return d


def sorting(data, ps, categories, f=None, n=None):
    d = {}
    if n == 1:
        for row in data:
            if row['category'] in categories:
                d[row['Rus']] = row['Fran']
    else:
        for row in data:
            if row['part_of_speech'] == ps:
                for category in categories:
                    if row['category'] == category or row['extra_info'] == category:
                        if category not in d:
                            d[category] = []
                        d[category].append([row['Rus'], row['Fran']])
    return d


def sorting_back(data, ps, categories, f=None, n=None):
    d = {}
    if n == 1:
        for row in data:
            if row['category'] in categories:
                d[row['Fran']] = row['Rus']
    else:
        for row in data:
            if row['part_of_speech'] == ps:
                for category in categories:
                    if row['category'] == category or row['extra_info'] == category:
                        if category not in d:
                            d[category] = []
                        d[category].append([row['Fran'], row['Rus']])
    return d


def gramm_sorting(data, ps, categories, f, n=None):
    forms = f()
    d = {}
    if n == 1:
        for row in data:
            if row['category'] in categories:
                #d[row['Fran']] = row['Rus']
                if row['Rus'] in forms:
                    d[forms[row['Rus']][0]] = forms[row['Rus']][1]
    for row in data:
        if row['part_of_speech'] == ps:
            for category in categories:
                if row['category'] == category or row['extra_info'] == category:
                    if category not in d:
                        d[category] = []
                    if row['Rus'] in forms:
                        d[category].append([forms[row['Rus']][0], forms[row['Rus']][1]])
    return d


def ex_genpl_maker():
    result = call_db('s_decl')
    d = {}
    context = ['Много ...', 'Мало ...', 'Не осталось ...', 'Не хватает ...']
    for row in result:
        if row['gen_pl'] != '' and row['gen_pl'] is not None:
            d[row['nom_sg']] = [str(random.choice(context)) + ' (' + row['nom_sg'] + ')', row['gen_pl']]
    return d


def prs_conj_maker():
    result = call_db('v_conj')
    d = {}
    arr = {'Я ... (': 'prs1sg', 'Ты ... (': 'prs2sg', 'Он ... (': 'prs3sg', 'Она ... (': 'prs3sg',
               'Мы ... (': 'prs1pl', 'Вы ... (': 'prs2pl', 'Они ... (': 'prs3pl'}
    for row in result:
        if row['prs1sg'] != '' and row['prs1sg'] is not None:
            context = random.choice(list(arr))
            d[row['inf']] = [context + row['inf'] + ')', row[arr[context]]]
    return d


def big_q_maker(ps, cat, sorter, func=None):
    result = call_db('rus_words')
    d = sorter(result, ps, cat, func, 1)
    num = 1
    try:
        quiz_mater = random.sample(list(d), 20)
    except ValueError:
        quiz_mater = list(d)
    quests = {}
    for key in quiz_mater:
        quests[str(num)] = {"question": key, "answer": d[key]}
        num += 1

    return quests


def quiz_maker(ps, cat, sorter, func=None):
    result = call_db('rus_words')
    d = sorter(result, ps, cat, func)
    newd = {}
    for key in d:
        try:
            quiz_mater = random.sample(d[key], 5)
            quests = {}
            num = 1
            for row in quiz_mater:
                quests[str(num)] = {"question": row[0], "answer": row[1]}
                num += 1
                newd[key] = quests
        except ValueError:
            continue
    return newd
"""--------------------------------Заглавная страница и страница клавиатуры------------------------------------------"""


@app.route('/')
@login_required
def profile_page():
    uemail = useremailget()
    profile_refer = url_for('profile_page')
    n_v = url_for('vocab_nouns')
    v_v = url_for('vocab_verbs')
    a_v = url_for('vocab_adverbs')
    return render_template('profile_page.html',
                           profile_refer=profile_refer,
                           noun_voc=n_v, verb_voc=v_v, adv_voc=a_v, uemail=uemail)


@app.route('/keyboard', methods=['GET'])
@login_required
def keyboard():
    return render_template('reqvkb.html')
"""-------------------------Страницы с маленькими квизами (тестами на оценку)----------------------------------------"""


@app.route('/materials/quiz_<categ>', methods=['GET', 'POST'])
@login_required
def quizes_page(categ):
    cs = {
        '1d': 'n', 'm': 'n', 'n': 'n', '3d': 'n', 'sg_tantum': 'n', 'pl_tantum': 'n',
        '1_productif': 'v', '1_sans_diff': 'v', '1_avec_diff': 'v', '1_base_altern': 'v', '2_productif': 'v',
        '2_improductif': 'v',
        'adv': 'adv'
    }
    questions = sess_2['quiz_' + cs[categ]]

    try:
        profile_refer = url_for('profile_page')
        if request.method == "POST":
            entered_answer = request.form.get('answer', '')
            if not entered_answer:
                flash("Entrez votre réponse, s'il vous plaît", "error")
            else:
                dist = distance(entered_answer, questions[categ][sess_2["current_question"]]["answer"])
                if dist == 0:
                    sess_2['mark'] += 1
                elif dist == 1:
                    sess_2['mark'] += (1/2)
                else:
                    sess_2['mistake_q_'+cs[categ]].append(questions[categ][sess_2["current_question"]]["question"]+' - '+questions[categ][sess_2["current_question"]]["answer"])
                sess_2["current_question"] = str(int(sess_2["current_question"]) + 1)
                if sess_2["current_question"] in questions:
                    redirect(url_for('quizes_page', categ=categ))
                else:
                    return render_template("q_success.html", profile_refer=profile_refer, a=0)
        if "current_question" not in sess_2:
            sess_2["current_question"] = "1"
        elif sess_2["current_question"] not in questions[categ]:
            mark = sess_2['mark']
            sess_2['mark'] = 0
            sess_2.pop("current_question")
            return render_template("q_success.html", profile_refer=profile_refer, a=1, markk=mark, mistakes=sess_2['mistake_q_'+cs[categ]])
        return render_template("quizes_page.html",
                               question=questions[categ][sess_2["current_question"]]["question"],
                               question_number=sess_2["current_question"],
                               profile_refer=profile_refer, cat=categ)
    except NameError:
        redirect(url_for('vocab_verbs'))


@app.route('/materials/quizb_<categ>', methods=['GET', 'POST'])
@login_required
def quizb_page(categ):
    cs = {
        '1d': 'n', 'm': 'n', 'n': 'n', '3d': 'n', 'sg_tantum': 'n', 'pl_tantum': 'n',
        '1_productif': 'v', '1_sans_diff': 'v', '1_avec_diff': 'v', '1_base_altern': 'v', '2_productif': 'v',
        '2_improductif': 'v',
        'adv': 'adv'
    }
    questions = sess_2['quizb_' + cs[categ]]
    try:
        profile_refer = url_for('profile_page')
        if request.method == "POST":
            entered_answer = request.form.get('answer', '')
            if not entered_answer:
                flash("Entrez votre réponse, s'il vous plaît", "error")
            else:
                dist = distance(entered_answer, questions[categ][sess_2["current_question"]]["answer"])
                if dist == 0:
                    sess_2['mark'] += 1
                elif dist == 1:
                    sess_2['mark'] += (1/2)
                else:
                    sess_2['mistake_bq_'+cs[categ]].append(questions[categ][sess_2["current_question"]]["question"]+' - '+questions[categ][sess_2["current_question"]]["answer"])
                sess_2["current_question"] = str(int(sess_2["current_question"]) + 1)
                if sess_2["current_question"] in questions:
                    redirect(url_for('quizb_page', categ=categ))
                else:
                    return render_template("q_success.html", profile_refer=profile_refer, a=0)
        if "current_question" not in sess_2:
            sess_2["current_question"] = "1"
        elif sess_2["current_question"] not in questions[categ]:
            mark = sess_2['mark']
            sess_2['mark'] = 0
            sess_2.pop("current_question")
            return render_template("q_success.html", profile_refer=profile_refer, a=1, markk=mark, mistakes=sess_2['mistake_bq_'+cs[categ]])
        return render_template("quizes_backw.html",
                               question=questions[categ][sess_2["current_question"]]["question"],
                               question_number=sess_2["current_question"],
                               profile_refer=profile_refer, cat=categ)
    except NameError:
        redirect(url_for('vocab_verbs'))


@app.route('/materials/qgenpl_<categ>', methods=['GET', 'POST'])
@login_required
def qgenpl(categ):
    questions = sess_2['qgenpl']
    try:
        profile_refer = url_for('profile_page')
        if request.method == "POST":
            entered_answer = request.form.get('answer', '')
            if not entered_answer:
                flash("Entrez votre réponse, s'il vous plaît", "error")
            else:
                dist = distance(entered_answer, questions[categ][sess_2["current_question"]]["answer"])
                if dist == 0:
                    sess_2['mark'] += 1
                elif dist == 1:
                    sess_2['mark'] += (1/2)
                else:
                    sess_2['mistake_gq_n'].append(questions[categ][sess_2["current_question"]]["question"].replace('...', questions[categ][sess_2["current_question"]]["answer"]))
                sess_2["current_question"] = str(int(sess_2["current_question"]) + 1)
                if sess_2["current_question"] in questions:
                    redirect(url_for('qgenpl', categ=categ))
                else:
                    return render_template("q_success.html", profile_refer=profile_refer, a=0)
        if "current_question" not in sess_2:
            sess_2["current_question"] = "1"
        elif sess_2["current_question"] not in questions[categ]:
            mark = sess_2['mark']
            sess_2['mark'] = 0
            sess_2.pop("current_question")
            return render_template("q_success.html", profile_refer=profile_refer, a=1, markk=mark, mistakes=sess_2['mistake_gq_n'])
        return render_template("quiz_genpl.html",
                               question=questions[categ][sess_2["current_question"]]["question"],
                               question_number=sess_2["current_question"],
                               profile_refer=profile_refer, cat=categ)
    except NameError:
        redirect(url_for('vocab_verbs'))


@app.route('/materials/qconj_<categ>', methods=['GET', 'POST'])
@login_required
def qconj(categ):
    questions = sess_2['qconj']
    try:
        profile_refer = url_for('profile_page')
        if request.method == "POST":
            entered_answer = request.form.get('answer', '')
            if not entered_answer:
                flash("Entrez votre réponse, s'il vous plaît", "error")
            else:
                dist = distance(entered_answer, questions[categ][sess_2["current_question"]]["answer"])
                if dist == 0:
                    sess_2['mark'] += 1
                elif dist == 1:
                    sess_2['mark'] += (1/2)
                else:
                    sess_2['mistake_cq_v'].append(questions[categ][sess_2["current_question"]]["question"].replace('...', questions[categ][sess_2["current_question"]]["answer"]))
                sess_2["current_question"] = str(int(sess_2["current_question"]) + 1)
                if sess_2["current_question"] in questions:
                    redirect(url_for('qconj', categ=categ))
                else:
                    return render_template("q_success.html", profile_refer=profile_refer, a=0)
        if "current_question" not in sess_2:
            sess_2["current_question"] = "1"
        elif sess_2["current_question"] not in questions[categ]:
            mark = sess_2['mark']
            sess_2['mark'] = 0
            sess_2.pop("current_question")
            return render_template("q_success.html", profile_refer=profile_refer, a=1,
                                   markk=mark, mistakes=sess_2['mistake_cq_v'])
        return render_template("quiz_conj.html",
                               question=questions[categ][sess_2["current_question"]]["question"],
                               question_number=sess_2["current_question"],
                               profile_refer=profile_refer, cat=categ)
    except NameError:
        redirect(url_for('vocab_verbs'))
"""---------------------------------------Страницы с большими квизами------------------------------------------------"""


@app.route('/materials/bigquiz_<categ>', methods=['GET', 'POST'])
@login_required
def bigquiz(categ):
    questions = sess_2['bigq_'+categ]
    try:
        profile_refer = url_for('profile_page')
        if request.method == "POST":
            entered_answer = request.form.get('answer', '')
            if not entered_answer:
                flash("Entrez votre réponse, s'il vous plaît", "error")
            else:
                dist = distance(entered_answer, questions[sess_2["current_question"]]["answer"])
                if dist == 0:
                    sess_2['mark'] += 1
                elif dist == 1:
                    sess_2['mark'] += (1/2)
                else:
                    sess_2['mistake_q_'+categ].append(questions[sess_2["current_question"]]["question"]+' - '+questions[sess_2["current_question"]]["answer"])
                sess_2["current_question"] = str(int(sess_2["current_question"]) + 1)
                if sess_2["current_question"] in questions:
                    redirect(url_for('bigquiz', categ=categ))
                else:
                    return render_template("q_success.html", profile_refer=profile_refer, a=0)
        if "current_question" not in sess_2:
            sess_2["current_question"] = "1"
        elif sess_2["current_question"] not in questions:
            mark = sess_2['mark']
            sess_2['mark'] = 0
            sess_2.pop("current_question")
            return render_template("q_success.html", profile_refer=profile_refer, a=1, markk=mark, mistakes=sess_2['mistake_q_'+categ])
        return render_template("bigquiz.html",
                               question=questions[sess_2["current_question"]]["question"],
                               question_number=sess_2["current_question"],
                               profile_refer=profile_refer, cat=categ, sumup=len(questions))
    except NameError:
        redirect(url_for('vocab_verbs'))


@app.route('/materials/bigquizb_<categ>', methods=['GET', 'POST'])
@login_required
def bigquizb(categ):
    questions = sess_2['big_qb_' + categ]
    try:
        profile_refer = url_for('profile_page')
        if request.method == "POST":
            entered_answer = request.form.get('answer', '')
            if not entered_answer:
                flash("Entrez votre réponse, s'il vous plaît", "error")
            else:
                dist = distance(entered_answer, questions[sess_2["current_question"]]["answer"])
                if dist == 0:
                    sess_2['mark'] += 1
                elif dist == 1:
                    sess_2['mark'] += (1/2)
                else:
                    sess_2['mistake_bq_' + categ].append(questions[sess_2["current_question"]]["question"]+' - '+questions[sess_2["current_question"]]["answer"])
                sess_2["current_question"] = str(int(sess_2["current_question"]) + 1)
                if sess_2["current_question"] in questions:
                    redirect(url_for('bigquizb', categ=categ))
                else:
                    return render_template("q_success.html", profile_refer=profile_refer, a=0)
        if "current_question" not in sess_2:
            sess_2["current_question"] = "1"
        elif sess_2["current_question"] not in questions:
            mark = sess_2['mark']
            sess_2['mark'] = 0
            sess_2.pop("current_question")
            return render_template("q_success.html", profile_refer=profile_refer, a=1, markk=mark, mistakes=sess_2['mistake_bq_'+categ])
        return render_template("bigquizb.html",
                               question=questions[sess_2["current_question"]]["question"],
                               question_number=sess_2["current_question"],
                               profile_refer=profile_refer, cat=categ, sumup=len(questions))
    except NameError:
        redirect(url_for('vocab_verbs'))


@app.route('/materials/bigqgenpl', methods=['GET', 'POST'])
@login_required
def bigqgenpl():
    questions = sess_2['bigqgenpl']
    try:
        profile_refer = url_for('profile_page')
        if request.method == "POST":
            entered_answer = request.form.get('answer', '')
            if not entered_answer:
                flash("Entrez votre réponse, s'il vous plaît", "error")
            else:
                dist = distance(entered_answer, questions[sess_2["current_question"]]["answer"])
                if dist == 0:
                    sess_2['mark'] += 1
                elif dist == 1:
                    sess_2['mark'] += (1/2)
                else:
                    sess_2['mistake_gq_n'].append(questions[sess_2["current_question"]]["question"].replace('...', questions[sess_2["current_question"]]["answer"]))
                sess_2["current_question"] = str(int(sess_2["current_question"]) + 1)
                if sess_2["current_question"] in questions:
                    redirect(url_for('bigqgenpl'))
                else:
                    return render_template("q_success.html", profile_refer=profile_refer, a=0)
        if "current_question" not in sess_2:
            sess_2["current_question"] = "1"
        elif sess_2["current_question"] not in questions:
            mark = sess_2['mark']
            sess_2['mark'] = 0
            sess_2.pop("current_question")
            return render_template("q_success.html", profile_refer=profile_refer, a=1, markk=mark, mistakes=sess_2['mistake_gq_n'])
        return render_template("bigq_gen.html",
                               question=questions[sess_2["current_question"]]["question"],
                               question_number=sess_2["current_question"],
                               profile_refer=profile_refer, sumup=len(questions))
    except NameError:
        redirect(url_for('vocab_verbs'))


@app.route('/materials/bigqconj_<categ>', methods=['GET', 'POST'])
@login_required
def bigqconj(categ):
    questions = sess_2['bigqconj'+categ]
    try:
        profile_refer = url_for('profile_page')
        if request.method == "POST":
            entered_answer = request.form.get('answer', '')
            if not entered_answer:
                flash("Entrez votre réponse, s'il vous plaît", "error")
            else:
                dist = distance(entered_answer, questions[sess_2["current_question"]]["answer"])
                if dist == 0:
                    sess_2['mark'] += 1
                elif dist == 1:
                    sess_2['mark'] += (1/2)
                else:
                    sess_2['mistake_cq_v'].append(questions[sess_2["current_question"]]["question"].replace('...', questions[sess_2["current_question"]]["answer"]))
                    sess_2["current_question"] = str(int(sess_2["current_question"]) + 1)
                if sess_2["current_question"] in questions:
                    redirect(url_for('bigqconj', categ=categ))
                else:
                    return render_template("q_success.html", profile_refer=profile_refer, a=0)
        if "current_question" not in sess_2:
            sess_2["current_question"] = "1"
        elif sess_2["current_question"] not in questions:
            mark = sess_2['mark']
            sess_2['mark'] = 0
            sess_2.pop("current_question")
            return render_template("q_success.html", profile_refer=profile_refer, a=1,
                                   markk=mark, mistakes=sess_2['mistake_cq_v'])
        return render_template("bigq_conj.html",
                               question=questions[sess_2["current_question"]]["question"],
                               question_number=sess_2["current_question"],
                               profile_refer=profile_refer, cat=categ, sumup=len(questions))
    except NameError:
        redirect(url_for('vocab_verbs'))

"""---------------------------Страницы с маленькими упражнениями (тестами не на оценку)------------------------------"""


@app.route('/materials/test_<categ>', methods=['GET', 'POST'])
@login_required
def test(categ):
    cs = {
        '1d': 'n', 'm': 'n', 'n':'n', '3d':'n', 'sg_tantum':'n', 'pl_tantum':'n',
        '1_productif': 'v', '1_sans_diff': 'v', '1_avec_diff': 'v', '1_base_altern': 'v', '2_productif': 'v', '2_improductif': 'v',
        'adv': 'adv'
    }
    questions = sess_2['questions_' + cs[categ]]
    try:
        profile_refer = url_for('profile_page')
        if request.method == "POST":
            entered_answer = request.form.get('answer', '')
            if not entered_answer:
                flash("Entrez votre réponse, s'il vous plaît", "error")
            elif entered_answer != questions[categ][sess_2["current_question"]]["answer"]:
                flash("La bonne réponse:\n" + questions[categ][sess_2["current_question"]]["answer"],
                      "error")
            else:
                sess_2["current_question"] = str(int(sess_2["current_question"]) + 1)
                if sess_2["current_question"] in questions:
                    redirect(url_for('test', categ=categ))
                else:
                    return render_template("success.html", profile_refer=profile_refer, a=0)
        if "current_question" not in sess_2:
            sess_2["current_question"] = "1"
        elif sess_2["current_question"] not in questions[categ]:
            sess_2.pop('current_question')
            return render_template("success.html", profile_refer=profile_refer, a=1)
        return render_template("test_page.html",
                               question=questions[categ][sess_2["current_question"]]["question"],
                               question_number=sess_2["current_question"],
                               profile_refer=profile_refer, cat=categ)
    except NameError:
        redirect(url_for('vocab_verbs'))


@app.route('/materials/testb_<categ>', methods=['GET', 'POST'])
@login_required
def testb(categ):
    cs = {
        '1d': 'n', 'm': 'n', 'n': 'n', '3d': 'n', 'sg_tantum': 'n', 'pl_tantum': 'n',
        '1_productif': 'v', '1_sans_diff': 'v', '1_avec_diff': 'v', '1_base_altern': 'v', '2_productif': 'v',
        '2_improductif': 'v',
        'adv': 'adv'
    }
    questions = sess_2['quest_b_' + cs[categ]]
    try:
        profile_refer = url_for('profile_page')
        if request.method == "POST":
            entered_answer = request.form.get('answer', '')
            if not entered_answer:
                flash("Entrez votre réponse, s'il vous plaît", "error")
            elif entered_answer != questions[categ][sess_2["current_question"]]["answer"]:
                flash("La bonne réponse:\n" + questions[categ][sess_2["current_question"]]["answer"], "error")
            else:
                sess_2["current_question"] = str(int(sess_2["current_question"]) + 1)
                if sess_2["current_question"] in questions:
                    redirect(url_for('testb', categ=categ))
                else:
                    return render_template("success.html", profile_refer=profile_refer, a=0)
        if "current_question" not in sess_2:
            sess_2["current_question"] = "1"
        elif sess_2["current_question"] not in questions[categ]:
            sess_2.pop('current_question')
            return render_template("success.html", profile_refer=profile_refer, a=1)
        return render_template("test_backw.html",
                               question=questions[categ][sess_2["current_question"]]["question"],
                               question_number=sess_2["current_question"],
                               profile_refer=profile_refer, cat=categ)
    except NameError:
        redirect(url_for('vocab_verbs'))

sess_2['i'] = 0


@app.route('/materials/genpl_<categ>', methods=['GET', 'POST'])
@login_required
def test_gen(categ):
    hints = {
        '1d': u'l’apparition de la voyelle mobile pour tous les mots présentant une accumulation de consonnes avec la désinence Ø<br>les mots à accent non final, tels que гóстья «l’invitée», ont une forme de Génitif pl. en -ий<br>les mots à accent final, tels que судья́ «le juge», ont une forme de Génitif pl. en -eй<br>dans une séquence «voyelle + й + consonne + a», le mécanisme de la voyelle mobile fait que le -й- est remplacé par un -e-<br>!Exceptions! Il y a trois mots en -ня où le <br>\'/ reste mou au Gen. pl., si l’accent est final, -ня́, on a une désinence -éй',
        'm': u'Le Génitif pluriel, outre les désinences de base dans les Types I et II, peut avoir une désinence Ø. La désinence Ø apparaît dans les mots dont le thème change au pluriel (mots en -анин / -янин, en -ёнок / -онок et en -ин)<br>Un certain nombre de mots ont une désinence Ø au Génitif pl. Le Génitif pl. sera donc semblable au Nominatif sg., mis à part les quelques cas où l’accent différencie les deux formes',
        'n': u'Une série de neutre en -o avec élargissement du thème par /j/, comme les substantifs masculins du type брат, le Génitif pl. de ces mots est -ьев<br>Le Génitif pl. a une désinence en -ев / -ов (outre les mots de cette série) dans deux mots en -ко mentionnés ci-dessus et dans quelques mots en -ье<br>La désinence type pour cette déclinaison, la désinence Ø, peut entraîner l’apparition d’une voyelle mobile<br>Il faut prêter attention aux mots en -ье, ceux-ci ont une forme de Génitif pl. en -ий'
    }
    questions = sess_2['ex_genpl']
    try:
        profile_refer = url_for('profile_page')
        if request.method == "POST":
            entered_answer = request.form.get('answer', '')
            if not entered_answer:
                flash("Entrez votre réponse, s'il vous plaît", "error")
            elif entered_answer != questions[categ][sess_2["current_question"]]["answer"]:
                if categ in hints and sess_2['i'] == 0:
                    flash(hints[categ], 'error')
                    sess_2['i'] += 1
                else:
                    flash("La bonne réponse:\n" + questions[categ][sess_2["current_question"]]["answer"],
                          "error")
            else:
                sess_2["current_question"] = str(int(sess_2["current_question"]) + 1)
                if sess_2["current_question"] in questions:
                    redirect(url_for('genpl_', categ=categ))
                else:
                    sess_2['i'] = 0
                    return render_template("success.html", profile_refer=profile_refer, a=0)
        if "current_question" not in sess_2:
            sess_2["current_question"] = "1"
        if sess_2["current_question"] not in questions[categ]:
            sess_2.pop('current_question')
            return render_template("success.html", profile_refer=profile_refer, a=1)
        return render_template("test_gen.html",
                               question=questions[categ][sess_2["current_question"]]["question"],
                               question_number=sess_2["current_question"],
                               profile_refer=profile_refer, cat=categ)
    except NameError:
        redirect(url_for('vocab_nouns'))


@app.route('/materials/conj_<categ>', methods=['GET', 'POST'])
@login_required
def test_conj(categ):
    questions = sess_2['ex_conj']
    try:
        profile_refer = url_for('profile_page')
        if request.method == "POST":
            entered_answer = request.form.get('answer', '')
            if not entered_answer:
                flash("Entrez votre réponse, s'il vous plaît", "error")
            elif entered_answer != questions[categ][sess_2["current_question"]]["answer"]:
                flash("La bonne réponse:\n" + questions[categ][sess_2["current_question"]]["answer"],
                      "error")
            else:
                sess_2["current_question"] = str(int(sess_2["current_question"]) + 1)
                if sess_2["current_question"] in questions:
                    redirect(url_for('conj_', categ=categ))
                else:
                    return render_template("success.html", profile_refer=profile_refer, a=0)
        if "current_question" not in sess_2:
            sess_2["current_question"] = "1"
        if sess_2["current_question"] not in questions[categ]:
            sess_2.pop('current_question')
            return render_template("success.html", profile_refer=profile_refer, a=1)
        return render_template("test_conj.html",
                               question=questions[categ][sess_2["current_question"]]["question"],
                               question_number=sess_2["current_question"],
                               profile_refer=profile_refer, cat=categ)
    except NameError:
        redirect(url_for('vocab_adverbs'))
"""-----------------------------------Страницы с большими упражнениями-----------------------------------------------"""


@app.route('/materials/bigtest_<categ>', methods=['GET', 'POST'])
@login_required
def bigtest(categ):
    questions = sess_2['big_t_' + categ]
    try:
        profile_refer = url_for('profile_page')
        if request.method == "POST":
            entered_answer = request.form.get('answer', '')
            if not entered_answer:
                flash("Entrez votre réponse, s'il vous plaît", "error")
            elif entered_answer != questions[sess_2["current_question"]]["answer"]:
                flash("La bonne réponse:\n" + questions[sess_2["current_question"]]["answer"],
                      "error")
            else:
                sess_2["current_question"] = str(int(sess_2["current_question"]) + 1)
                if sess_2["current_question"] in questions:
                    redirect(url_for('bigtest', categ=categ))
                else:
                    return render_template("success.html", profile_refer=profile_refer, a=0)
        if "current_question" not in sess_2:
            sess_2["current_question"] = "1"
        elif sess_2["current_question"] not in questions:
            sess_2.pop('current_question')
            return render_template("success.html", profile_refer=profile_refer, a=1)
        return render_template("bigtest.html",
                               question=questions[sess_2["current_question"]]["question"],
                               question_number=sess_2["current_question"], sumup=len(questions),
                               profile_refer=profile_refer, cat=categ)
    except NameError:
        redirect(url_for('vocab_verbs'))


@app.route('/materials/bigtestb_<categ>', methods=['GET', 'POST'])
@login_required
def bigtestb(categ):
    questions = sess_2['big_tb_' + categ]
    try:
        profile_refer = url_for('profile_page')
        if request.method == "POST":
            entered_answer = request.form.get('answer', '')
            if not entered_answer:
                flash("Entrez votre réponse, s'il vous plaît", "error")
            elif entered_answer != questions[sess_2["current_question"]]["answer"]:
                flash("La bonne réponse:\n" + questions[sess_2["current_question"]]["answer"], "error")
            else:
                sess_2["current_question"] = str(int(sess_2["current_question"]) + 1)
                if sess_2["current_question"] in questions:
                    redirect(url_for('bigtestb', categ=categ))
                else:
                    return render_template("success.html", profile_refer=profile_refer, a=0)
        if "current_question" not in sess_2:
            sess_2["current_question"] = "1"
        elif sess_2["current_question"] not in questions:
            sess_2.pop('current_question')
            return render_template("success.html", profile_refer=profile_refer, a=1)
        return render_template("bigtestb.html",
                               question=questions[sess_2["current_question"]]["question"],
                               question_number=sess_2["current_question"],
                               profile_refer=profile_refer, cat=categ, sumup = len(questions))
    except NameError:
        redirect(url_for('vocab_verbs'))


@app.route('/materials/biggenpl', methods=['GET', 'POST'])
@login_required
def biggenpl():
    questions = sess_2['biggenpl']
    try:
        profile_refer = url_for('profile_page')
        if request.method == "POST":
            entered_answer = request.form.get('answer', '')
            if not entered_answer:
                flash("Entrez votre réponse, s'il vous plaît", "error")
            elif entered_answer != questions[sess_2["current_question"]]["answer"]:
                flash("La bonne réponse:\n" + questions[sess_2["current_question"]]["answer"],
                      "error")
            else:
                sess_2["current_question"] = str(int(sess_2["current_question"]) + 1)
                if sess_2["current_question"] in questions:
                    redirect(url_for('biggenpl'))
                else:
                    sess_2['i'] = 0
                    return render_template("success.html", profile_refer=profile_refer, a=0)
        if "current_question" not in sess_2:
            sess_2["current_question"] = "1"
        if sess_2["current_question"] not in questions:
            sess_2.pop('current_question')
            return render_template("success.html", profile_refer=profile_refer, a=1)
        return render_template("bigt_gen.html",
                               question=questions[sess_2["current_question"]]["question"],
                               question_number=sess_2["current_question"],
                               profile_refer=profile_refer, sumup=len(questions))
    except NameError:
        redirect(url_for('vocab_nouns'))


@app.route('/materials/bigconj_<categ>', methods=['GET', 'POST'])
@login_required
def bigconj(categ):
    questions = sess_2['bigconj'+categ]
    try:
        profile_refer = url_for('profile_page')
        if request.method == "POST":
            entered_answer = request.form.get('answer', '')
            if not entered_answer:
                flash("Entrez votre réponse, s'il vous plaît", "error")
            elif entered_answer != questions[sess_2["current_question"]]["answer"]:
                flash("La bonne réponse:\n" + questions[sess_2["current_question"]]["answer"],
                      "error")
            else:
                sess_2["current_question"] = str(int(sess_2["current_question"]) + 1)
                if sess_2["current_question"] in questions:
                    redirect(url_for('bigconj', categ=categ))
                else:
                    return render_template("success.html", profile_refer=profile_refer, a=0)
        if "current_question" not in sess_2:
            sess_2["current_question"] = "1"
        if sess_2["current_question"] not in questions:
            sess_2.pop('current_question')
            return render_template("success.html", profile_refer=profile_refer, a=1)
        return render_template("bigconj.html",
                               question=questions[sess_2["current_question"]]["question"],
                               question_number=sess_2["current_question"],
                               profile_refer=profile_refer, cat=categ, sumup=len(questions))
    except NameError:
        redirect(url_for('vocab_adverbs'))

"""-------------------------------Страницы с материалами по каждой теме/части речи-----------------------------------"""


@app.route('/materials/vocab_nouns')
@login_required
def vocab_nouns():
    ps = 's'
    cats = {'1d': 'Premier declinasion', 'm': 'Les masculins', 'n': 'Les neutres', '3d': 'Troiseme declinasion',
           'sg_tantum': 'Singularia Tantum', 'pl_tantum': 'Pluralia tantum'}
    cat = ['1d', 'm', 'n', '3d', 'sg_tantum', 'pl_tantum']
    sess_2['mark'] = 0
    sess_2['quiz_n'] = quiz_maker(ps, cat, sorting)
    sess_2['questions_n'] = quiz_maker(ps, cat, sorting)
    sess_2['big_t_n'] = big_q_maker(ps, cat, sorting)
    sess_2['bigq_n'] = big_q_maker(ps, cat, sorting)
    sess_2['quizb_n'] = quiz_maker(ps, cat, sorting_back)
    sess_2['quest_b_n'] = quiz_maker(ps, cat, sorting_back)
    sess_2['big_tb_n'] = big_q_maker(ps, cat, sorting_back)
    sess_2['big_qb_n'] = big_q_maker(ps, cat, sorting_back)
    sess_2['qgenpl'] = quiz_maker(ps, cat, gramm_sorting, ex_genpl_maker)
    sess_2['ex_genpl'] = quiz_maker(ps, cat, gramm_sorting, ex_genpl_maker)
    sess_2['biggenpl'] = big_q_maker(ps, cat, gramm_sorting, ex_genpl_maker)
    sess_2['bigqgenpl'] = big_q_maker(ps, cat, gramm_sorting, ex_genpl_maker)
    sess_2['mistake_q_n'] = []
    sess_2['mistake_bq_n'] = []
    sess_2['mistake_gq_n'] = []
    voc = voc_maker(ps, cat)
    profile_refer = url_for('profile_page')
    return render_template('vocab.html',
                           profile_refer=profile_refer, cats=cats,
                           mama=cat, voc=voc, vocab_category='Le Substantif', ps='n', uemail=useremailget(),
                           noun_voc=url_for('vocab_nouns'), verb_voc='vocab_verbs', adv_voc=url_for('vocab_adverbs'))


@app.route('/materials/vocab_verbs')
@login_required
def vocab_verbs():
    ps = 'v'
    cats = {'1_productif': 'Premiere conjugasion. Types productifs', '1_sans_diff': 'Premiere conjugasion. Types Improductifs. Bases sans différentiel',
            '1_avec_diff': 'Premiere conjugasion. Types improductifs. Bases avec différentiel',
            '1_base_altern': 'Premiere conjugasion. Types Improductifs. Bases alternantes',
            '2_productif': 'Premiere conjugasion. Types productifs','2_improductif': 'Premiere conjugasion. Types improductifs'}
    cat = ['1_productif', '1_sans_diff', '1_avec_diff', '1_base_altern', '2_productif', '2_improductif']
    bigcat1 = ['1_productif', '1_sans_diff', '1_avec_diff', '1_base_altern']
    bigcat2 = ['2_productif', '2_improductif']
    sess_2['mark'] = 0
    sess_2['quiz_v'] = quiz_maker(ps, cat, sorting)
    sess_2['questions_v'] = quiz_maker(ps, cat, sorting)
    sess_2['big_t_v'] = big_q_maker(ps, cat, sorting)
    sess_2['big_t_v1'] = big_q_maker(ps, bigcat1, sorting)
    sess_2['big_t_v2'] = big_q_maker(ps, bigcat2, sorting)
    sess_2['bigq_v1'] = big_q_maker(ps, bigcat1, sorting)
    sess_2['bigq_v2'] = big_q_maker(ps, bigcat2, sorting)
    sess_2['bigq_v'] = big_q_maker(ps, cat, sorting)
    sess_2['quizb_v'] = quiz_maker(ps, cat, sorting_back)
    sess_2['quest_b_v'] = quiz_maker(ps, cat, sorting_back)
    sess_2['big_tb_v1'] = big_q_maker(ps, bigcat1, sorting_back)
    sess_2['big_tb_v2'] = big_q_maker(ps, bigcat2, sorting_back)
    sess_2['big_tb_v'] = big_q_maker(ps, cat, sorting_back)
    sess_2['big_qb_v1'] = big_q_maker(ps, bigcat1, sorting_back)
    sess_2['big_qb_v2'] = big_q_maker(ps, bigcat2, sorting_back)
    sess_2['big_qb_v'] = big_q_maker(ps, cat, sorting_back)
    sess_2['qconj'] = quiz_maker(ps, cat, gramm_sorting, prs_conj_maker)
    sess_2['ex_conj'] = quiz_maker(ps, cat, gramm_sorting, prs_conj_maker)
    sess_2['bigconjv'] = big_q_maker(ps, cat, gramm_sorting, prs_conj_maker)
    sess_2['bigconjv1'] = big_q_maker(ps, bigcat1, gramm_sorting, prs_conj_maker)
    sess_2['bigconjv2'] = big_q_maker(ps, bigcat2, gramm_sorting, prs_conj_maker)
    sess_2['mistake_q_v'] = []
    sess_2['mistake_bq_v'] = []
    sess_2['mistake_cq_v'] = []

    sess_2['bigqconjv'] = big_q_maker(ps, cat, gramm_sorting, prs_conj_maker)
    sess_2['bigqconjv1'] = big_q_maker(ps, bigcat1, gramm_sorting, prs_conj_maker)
    sess_2['bigqconjv2'] = big_q_maker(ps, bigcat2, gramm_sorting, prs_conj_maker)
    voc = voc_maker(ps, cat)
    profile_refer = url_for('profile_page')
    return render_template('vocab.html', uemail=useremailget(), cats = cats,
                           profile_refer=profile_refer, mama=cat, voc=voc, vocab_category='Le Verbe', ps='v',
                           noun_voc=url_for('vocab_nouns'), verb_voc='vocab_verbs', adv_voc=url_for('vocab_adverbs'))


@app.route('/materials/vocab_adverbs')
@login_required
def vocab_adverbs():
    ps = 'adv'
    cats = {'adv': ''}
    cat = ['adv']
    sess_2['mark'] = 0
    sess_2['quiz_adv'] = quiz_maker(ps, cat, sorting)
    sess_2['questions_adv'] = quiz_maker(ps, cat, sorting)
    sess_2['big_t_adv'] = big_q_maker(ps, cat, sorting)
    sess_2['bigq_adv'] = big_q_maker(ps, cat, sorting)
    sess_2['quizb_adv'] = quiz_maker(ps, cat, sorting_back)
    sess_2['quest_b_adv'] = quiz_maker(ps, cat, sorting_back)
    sess_2['big_tb_adv'] = big_q_maker(ps, cat, sorting_back)
    sess_2['big_qb_adv'] = big_q_maker(ps, cat, sorting_back)
    sess_2['mistake_q_adv'] = []
    sess_2['mistake_bq_adv'] = []
    voc = voc_maker(ps, cat)
    profile_refer = url_for('profile_page')
    return render_template('vocab.html',
                           profile_refer=profile_refer, uemail=useremailget(), cats=cats,
                           mama=cat, voc=voc, vocab_category="L'Adverbe", ps='adv',
                           noun_voc=url_for('vocab_nouns'), verb_voc='vocab_verbs', adv_voc=url_for('vocab_adverbs'))


if __name__ == '__main__':
    app.run()
