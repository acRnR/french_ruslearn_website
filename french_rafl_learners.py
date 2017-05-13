import os
import random
from flask import Flask
from flask import url_for, render_template, request, redirect, flash, session
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.sql import select
import html


app = Flask(__name__)
app.secret_key = os.urandom(24)


def voc_maker(ps, categories):
    #print('vocmaker ON')
    class Words(object):
        pass

    db_path = 'vocabulary.db'
    engine = create_engine('sqlite:///%s' % db_path, echo=False)
    metadata = MetaData(engine)
    rus_words = Table('rus_words', metadata, autoload=True)
    mapper(Words, rus_words)
    sessionmaker(bind=engine)
    conn = engine.connect()
    s = select([rus_words])
    result = conn.execute(s)

    d = sorting(result, ps, categories)
    #print('vocmaker OFF\n', d)
    return d


def sorting(data, ps, categories):
    #print('sorting')
    d = {}
    for row in data:
        if row['part_of_speech'] == ps:
            for category in categories:
                if row['category'] == category or row['extra_info'] == category:
                    if category not in d:
                        d[category] = []
                    d[category].append([row['Rus'], row['Fran']])
    #print('sorted')
    return d


def sorting_back(data, ps, categories):
    #print('sorting')
    d = {}
    for row in data:
        if row['part_of_speech'] == ps:
            for category in categories:
                if row['category'] == category or row['extra_info'] == category:
                    if category not in d:
                        d[category] = []
                    d[category].append([row['Fran'], row['Rus']])
    #print('sorted')
    return d


def quiz_maker(ps, cat, func):
    #print('quizmaker ON')
    class Words(object):
        pass
    db_path = 'vocabulary.db'
    engine = create_engine('sqlite:///%s' % db_path, echo=False)
    metadata = MetaData(engine)
    rus_words = Table('rus_words', metadata, autoload=True)
    mapper(Words, rus_words)
    sessionmaker(bind=engine)
    conn = engine.connect()
    s = select([rus_words])
    result = conn.execute(s)

    d = func(result, ps, cat)
    #i = 1
    newd = {}
    for key in d:#{'1d':[['лол', 'lol'], ['шта', 'wut']]}
        #qs = {}
        quiz_mater = random.sample(d[key], 5)
        quests = {}
        i = 1
        for row in quiz_mater:
            quests[str(i)] = {"question": row[0], "answer": row[1]}

            #qs.append(quests)
            i += 1
            newd[key] = quests
    #{ cat : [ 1 : {"question": row[0], "answer": row[1]}, 2 : {"question": row[0], "answer": row[1]} }]
    #print('quizmaker OFF')
    return newd


@app.route('/')
def profile_page():
    profile_refer = url_for('profile_page')
    quizes_refer = url_for('quizes_page')
    test_refer = url_for('test_1d')
    n_v = url_for('vocab_nouns')
    v_v = url_for('vocab_verbs')
    a_v = url_for('vocab_adverbs')
    # todo: добавить ссылки на тесты
    return render_template('profile_page.html',
                           profile_refer=profile_refer, quizes_refer=quizes_refer, test_refer=test_refer,
                           noun_voc=n_v, verb_voc=v_v, adv_voc=a_v)


@app.route('/quizes_page')
def quizes_page():
    profile_refer = url_for('profile_page')
    return render_template('quizes_page.html', profile_refer=profile_refer)

"""------------------------------------------------------------------------------------------"""

@app.route('/materials/vocab_nouns')
def vocab_nouns():
    ps = 's'
    cat = ['1d', 'm', 'n', '3d', 'sg_tantum', 'pl_tantum']
    session['questions_n'] = quiz_maker(ps,cat, sorting)
    session['quest_b_n'] = quiz_maker(ps, cat, sorting_back)
    voc = voc_maker(ps, cat)
    profile_refer = url_for('profile_page')
    quizes_refer = url_for('quizes_page')
    #a1d = url_for('test_1d')
    return render_template('vocab.html',
                           profile_refer=profile_refer, quizes_refer=quizes_refer,# test_refer=test_refer,
                           mama=cat, voc=voc, vocab_category='Le Substantif')#,
                           #a1d=a1d)


@app.route('/materials/test_1d', methods=['GET', 'POST'])
def test_1d():
    questions_n = session['questions_n']
    try:
        profile_refer = url_for('profile_page')
        quizes_refer = url_for('quizes_page')

        if request.method == "POST":
            entered_answer = request.form.get('answer', '')
            if not entered_answer:
                flash("Please enter an answer", "error")  # Show error if no answer entered
            elif entered_answer != questions_n["1d"][session["current_question"]]["answer"]:
                flash("La bonne réponse:\n" + questions_n["1d"][session["current_question"]]["answer"], "error")
            else:
                session["current_question"] = str(int(session["current_question"]) + 1)
                if session["current_question"] in questions_n:
                    redirect(url_for('test_1d'))
                else:
                    return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=0)
        if "current_question" not in session:
            session["current_question"] = "1"
        elif session["current_question"] not in questions_n["1d"]:
            session.pop("current_question")
            return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=1)
        return render_template("test_page.html",
                               question=questions_n["1d"][session["current_question"]]["question"],
                               question_number=session["current_question"],
                               profile_refer=profile_refer, quizes_refer=quizes_refer, cat='1d')
    except NameError:
        redirect(url_for('vocab_nouns'))


@app.route('/materials/test_m', methods=['GET', 'POST'])
def test_m():
    questions_n = session['questions_n']
    try:
        profile_refer = url_for('profile_page')
        quizes_refer = url_for('quizes_page')
        if request.method == "POST":
            entered_answer = request.form.get('answer', '')
            if not entered_answer:
                flash("Please enter an answer", "error")  # Show error if no answer entered
            elif entered_answer != questions_n["m"][session["current_question"]]["answer"]:
                flash("La bonne réponse:\n" + questions_n["m"][session["current_question"]]["answer"], "error")
            else:
                session["current_question"] = str(int(session["current_question"]) + 1)
                if session["current_question"] in questions_n:
                    redirect(url_for('test_m'))
                else:
                    return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=0)
        if "current_question" not in session:
            session["current_question"] = "1"
        elif session["current_question"] not in questions_n["m"]:
            session.pop("current_question")
            return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=1)
        return render_template("test_page.html",
                               question=questions_n["m"][session["current_question"]]["question"],
                               question_number=session["current_question"],
                               profile_refer=profile_refer, quizes_refer=quizes_refer, cat='m')
    except NameError:
        redirect(url_for('vocab_nouns'))


@app.route('/materials/test_n', methods=['GET', 'POST'])
def test_n():
    questions_n = session['questions_n']
    try:
        profile_refer = url_for('profile_page')
        quizes_refer = url_for('quizes_page')

        if request.method == "POST":
            entered_answer = request.form.get('answer', '')
            print('AAAAAAA', entered_answer)
            if not entered_answer:
                flash("Please enter an answer", "error")  # Show error if no answer entered
            elif entered_answer != questions_n["n"][session["current_question"]]["answer"]:
                flash("La bonne réponse:\n" + questions_n["n"][session["current_question"]]["answer"], "error")
            else:
                session["current_question"] = str(int(session["current_question"]) + 1)
                if session["current_question"] in questions_n:
                    redirect(url_for('test_n'))
                else:
                    print('ahaaaa')
                    return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=0)
        if "current_question" not in session:
            session["current_question"] = "1"
        elif session["current_question"] not in questions_n["n"]:
            session.pop("current_question")
            return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=1)
        return render_template("test_page.html",
                               question=questions_n["n"][session["current_question"]]["question"],
                               question_number=session["current_question"],
                               profile_refer=profile_refer, quizes_refer=quizes_refer, cat='n')
    except NameError:
        redirect(url_for('vocab_nouns'))


@app.route('/materials/test_3d', methods=['GET', 'POST'])
def test_3d():
    questions_n = session['questions_n']
    try:
        profile_refer = url_for('profile_page')
        quizes_refer = url_for('quizes_page')

        if request.method == "POST":
            entered_answer = request.form.get('answer', '')
            print('AAAAAAA', entered_answer)
            if not entered_answer:
                flash("Please enter an answer", "error")  # Show error if no answer entered
            elif entered_answer != questions_n["3d"][session["current_question"]]["answer"]:
                flash("La bonne réponse:\n" + questions_n["3d"][session["current_question"]]["answer"], "error")
            else:
                session["current_question"] = str(int(session["current_question"]) + 1)
                if session["current_question"] in questions_n:
                    redirect(url_for('test_3d'))
                else:
                    print('ahaaaa')
                    return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=0)
        if "current_question" not in session:
            session["current_question"] = "1"
        elif session["current_question"] not in questions_n["3d"]:
            session.pop("current_question")
            return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=1)
        return render_template("test_page.html",
                               question=questions_n["3d"][session["current_question"]]["question"],
                               question_number=session["current_question"],
                               profile_refer=profile_refer, quizes_refer=quizes_refer, cat='3d')
    except NameError:
        redirect(url_for('vocab_nouns'))


@app.route('/materials/test_sg_tantum', methods=['GET', 'POST'])
def test_sg_tantum():
    questions_n = session['questions_n']
    try:
        profile_refer = url_for('profile_page')
        quizes_refer = url_for('quizes_page')

        if request.method == "POST":
            entered_answer = request.form.get('answer', '')
            if not entered_answer:
                flash("Please enter an answer", "error")  # Show error if no answer entered
            elif entered_answer != questions_n["sg_tantum"][session["current_question"]]["answer"]:
                flash("La bonne réponse:\n" + questions_n["sg_tantum"][session["current_question"]]["answer"], "error")
            else:
                session["current_question"] = str(int(session["current_question"]) + 1)
                if session["current_question"] in questions_n:
                    redirect(url_for('test_sg_tantum'))
                else:
                    return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=0)
        if "current_question" not in session:
            session["current_question"] = "1"
        elif session["current_question"] not in questions_n["sg_tantum"]:
            session.pop("current_question")
            return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=1)
        return render_template("test_page.html",
                               question=questions_n["sg_tantum"][session["current_question"]]["question"],
                               question_number=session["current_question"],
                               profile_refer=profile_refer, quizes_refer=quizes_refer, cat='sg_tantum')
    except NameError:
        redirect(url_for('vocab_nouns'))


@app.route('/materials/test_pl_tantum', methods=['GET', 'POST'])
def test_pl_tantum():
    questions_n = session['questions_n']
    try:
        profile_refer = url_for('profile_page')
        quizes_refer = url_for('quizes_page')

        if request.method == "POST":
            entered_answer = request.form.get('answer', '')
            if not entered_answer:
                flash("Please enter an answer", "error")  # Show error if no answer entered
            elif entered_answer != questions_n["pl_tantum"][session["current_question"]]["answer"]:
                flash("La bonne réponse:\n" + questions_n["pl_tantum"][session["current_question"]]["answer"], "error")
            else:
                session["current_question"] = str(int(session["current_question"]) + 1)
                if session["current_question"] in questions_n:
                    redirect(url_for('test_pl_tantum'))
                else:
                    return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=0)
        if "current_question" not in session:
            session["current_question"] = "1"
        elif session["current_question"] not in questions_n["pl_tantum"]:
            session.pop("current_question")
            return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=1)
        return render_template("test_page.html",
                               question=questions_n["pl_tantum"][session["current_question"]]["question"],
                               question_number=session["current_question"],
                               profile_refer=profile_refer, quizes_refer=quizes_refer, cat='pl_tantum')
    except NameError:
        redirect(url_for('vocab_nouns'))

"""-------------------------------------------------------------------------------------------"""

@app.route('/materials/vocab_verbs')
def vocab_verbs():
    ps = 'v'
    cat = ['1_productif', '1_sans_diff', '1_avec_diff', '1_base_altern', '2_productif', '2_improductif']
    session['questions_v'] = quiz_maker(ps, cat, sorting)
    session['quest_b_v'] = quiz_maker(ps, cat, sorting_back)
    voc = voc_maker(ps, cat)
    profile_refer = url_for('profile_page')
    quizes_refer = url_for('quizes_page')
    #test_refer = url_for('test_page')
    return render_template('vocab.html',
                           profile_refer=profile_refer, quizes_refer=quizes_refer,# test_refer=test_refer,
                           mama=cat, voc=voc, vocab_category='Le Verbe')


@app.route('/materials/test_1_productif', methods=['GET', 'POST'])
def test_1_productif():
    questions_v = session['questions_v']
    try:
        profile_refer = url_for('profile_page')
        quizes_refer = url_for('quizes_page')
        if request.method == "POST":
            entered_answer = request.form.get('answer', '')
            if not entered_answer:
                flash("Please enter an answer", "error")  # Show error if no answer entered
            elif entered_answer != questions_v["1_productif"][session["current_question"]]["answer"]:
                flash("La bonne réponse:\n" + questions_v["1_productif"][session["current_question"]]["answer"], "error")
            else:
                session["current_question"] = str(int(session["current_question"]) + 1)
                if session["current_question"] in questions_v:
                    redirect(url_for('test_1_productif'))
                else:
                    return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=0)
        if "current_question" not in session:
            session["current_question"] = "1"
        elif session["current_question"] not in questions_v["1_productif"]:
            session.pop("current_question")
            return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=1)
        return render_template("test_page.html",
                               question=questions_v["1_productif"][session["current_question"]]["question"],
                               question_number=session["current_question"],
                               profile_refer=profile_refer, quizes_refer=quizes_refer, cat='1_productif')
    except NameError:
        redirect(url_for('vocab_verbs'))


@app.route('/materials/test_1_base_altern', methods=['GET', 'POST'])
def test_1_base_altern():
    questions_v = session['questions_v']
    try:
        profile_refer = url_for('profile_page')
        quizes_refer = url_for('quizes_page')
        if request.method == "POST":
            entered_answer = request.form.get('answer', '')
            if not entered_answer:
                flash("Please enter an answer", "error")  # Show error if no answer entered
            elif entered_answer != questions_v["1_base_altern"][session["current_question"]]["answer"]:
                flash("La bonne réponse:\n" + questions_v["1_base_altern"][session["current_question"]]["answer"], "error")
            else:
                session["current_question"] = str(int(session["current_question"]) + 1)
                if session["current_question"] in questions_v:
                    redirect(url_for('test_1_base_altern'))
                else:
                    return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=0)
        if "current_question" not in session:
            session["current_question"] = "1"
        elif session["current_question"] not in questions_v["1_base_altern"]:
            session.pop("current_question")
            return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=1)
        return render_template("test_page.html",
                               question=questions_v["1_base_altern"][session["current_question"]]["question"],
                               question_number=session["current_question"],
                               profile_refer=profile_refer, quizes_refer=quizes_refer, cat='1_base_altern')
    except NameError:
        redirect(url_for('vocab_verbs'))


@app.route('/materials/test_1_avec_diff', methods=['GET', 'POST'])
def test_1_avec_diff():
    questions_v = session['questions_v']
    try:
        profile_refer = url_for('profile_page')
        quizes_refer = url_for('quizes_page')
        if request.method == "POST":
            entered_answer = request.form.get('answer', '')
            if not entered_answer:
                flash("Please enter an answer", "error")  # Show error if no answer entered
            elif entered_answer != questions_v["1_avec_diff"][session["current_question"]]["answer"]:
                flash("La bonne réponse:\n" + questions_v["1_avec_diff"][session["current_question"]]["answer"], "error")
            else:
                session["current_question"] = str(int(session["current_question"]) + 1)
                if session["current_question"] in questions_v:
                    redirect(url_for('test_1_avec_diff'))
                else:
                    return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=0)
        if "current_question" not in session:
            session["current_question"] = "1"
        elif session["current_question"] not in questions_v["1_avec_diff"]:
            session.pop("current_question")
            return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=1)
        return render_template("test_page.html",
                               question=questions_v["1_avec_diff"][session["current_question"]]["question"],
                               question_number=session["current_question"],
                               profile_refer=profile_refer, quizes_refer=quizes_refer, cat='1_avec_diff')
    except NameError:
        redirect(url_for('vocab_verbs'))


@app.route('/materials/test_1_sans_diff', methods=['GET', 'POST'])
def test_1_sans_diff():
    questions_v = session['questions_v']
    try:
        profile_refer = url_for('profile_page')
        quizes_refer = url_for('quizes_page')
        if request.method == "POST":
            entered_answer = request.form.get('answer', '')
            if not entered_answer:
                flash("Please enter an answer", "error")  # Show error if no answer entered
            elif entered_answer != questions_v["1_sans_diff"][session["current_question"]]["answer"]:
                flash("La bonne réponse:\n" + questions_v["1_sans_diff"][session["current_question"]]["answer"], "error")
            else:
                session["current_question"] = str(int(session["current_question"]) + 1)
                if session["current_question"] in questions_v:
                    redirect(url_for('test_1_sans_diff'))
                else:
                    return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=0)
        if "current_question" not in session:
            session["current_question"] = "1"
        elif session["current_question"] not in questions_v["1_sans_diff"]:
            session.pop("current_question")
            return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=1)
        return render_template("test_page.html",
                               question=questions_v["1_sans_diff"][session["current_question"]]["question"],
                               question_number=session["current_question"],
                               profile_refer=profile_refer, quizes_refer=quizes_refer, cat='1_sans_diff')
    except NameError:
        redirect(url_for('vocab_verbs'))


@app.route('/materials/test_2_productif', methods=['GET', 'POST'])
def test_2_productif():
    questions_v = session['questions_v']
    try:
        profile_refer = url_for('profile_page')
        quizes_refer = url_for('quizes_page')
        if request.method == "POST":
            entered_answer = request.form.get('answer', '')
            if not entered_answer:
                flash("Please enter an answer", "error")  # Show error if no answer entered
            elif entered_answer != questions_v["2_productif"][session["current_question"]]["answer"]:
                flash("La bonne réponse:\n" + questions_v["2_productif"][session["current_question"]]["answer"], "error")
            else:
                session["current_question"] = str(int(session["current_question"]) + 1)
                if session["current_question"] in questions_v:
                    redirect(url_for('test_2_productif'))
                else:
                    return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=0)
        if "current_question" not in session:
            session["current_question"] = "1"
        elif session["current_question"] not in questions_v["2_productif"]:
            session.pop("current_question")
            return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=1)
        return render_template("test_page.html",
                               question=questions_v["2_productif"][session["current_question"]]["question"],
                               question_number=session["current_question"],
                               profile_refer=profile_refer, quizes_refer=quizes_refer, cat='2_productif')
    except NameError:
        redirect(url_for('vocab_verbs'))


@app.route('/materials/test_2_improductif', methods=['GET', 'POST'])
def test_2_improductif():
    questions_v = session['questions_v']
    try:
        profile_refer = url_for('profile_page')
        quizes_refer = url_for('quizes_page')
        if request.method == "POST":
            entered_answer = request.form.get('answer', '')
            if not entered_answer:
                flash("Please enter an answer", "error")  # Show error if no answer entered
            elif entered_answer != questions_v["2_improductif"][session["current_question"]]["answer"]:
                flash("La bonne réponse:\n" + questions_v["2_improductif"][session["current_question"]]["answer"], "error")
            else:
                session["current_question"] = str(int(session["current_question"]) + 1)
                if session["current_question"] in questions_v:
                    redirect(url_for('test_2_improductif'))
                else:
                    return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=0)
        if "current_question" not in session:
            session["current_question"] = "1"
        elif session["current_question"] not in questions_v["2_improductif"]:
            session.pop("current_question")
            return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=1)

        return render_template("test_page.html",
                               question=questions_v["2_improductif"][session["current_question"]]["question"],
                               question_number=session["current_question"],
                               profile_refer=profile_refer, quizes_refer=quizes_refer, cat='2_improductif')
    except NameError:
        redirect(url_for('vocab_verbs'))


@app.route('/materials/testb_1_productif', methods=['GET', 'POST'])
def testb_1_productif():
    questions_v = session['quest_b_v']
    try:
        profile_refer = url_for('profile_page')
        quizes_refer = url_for('quizes_page')
        if request.method == "POST":
            entered_answer = request.form.get('answer', '')
            if not entered_answer:
                flash("Please enter an answer", "error")  # Show error if no answer entered
            elif entered_answer.replace('́', '&#769;') != questions_v["1_productif"][session["current_question"]]["answer"]:
                flash("La bonne réponse:\n" + questions_v["1_productif"][session["current_question"]]["answer"], "error")
            else:
                session["current_question"] = str(int(session["current_question"]) + 1)
                if session["current_question"] in questions_v:
                    redirect(url_for('testb_1_productif'))
                else:
                    return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=0)
        if "current_question" not in session:
            session["current_question"] = "1"
        elif session["current_question"] not in questions_v["1_productif"]:
            session.pop("current_question")
            return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=1)
        return render_template("test_backw.html",
                               question=questions_v["1_productif"][session["current_question"]]["question"],
                               question_number=session["current_question"],
                               profile_refer=profile_refer, quizes_refer=quizes_refer, cat='1_productif')
    except NameError:
        redirect(url_for('vocab_verbs'))


@app.route('/materials/testb_1_base_altern', methods=['GET', 'POST'])
def testb_1_base_altern():
    questions_v = session['quest_b_v']
    try:
        profile_refer = url_for('profile_page')
        quizes_refer = url_for('quizes_page')
        if request.method == "POST":
            entered_answer = request.form.get('answer', '')
            if not entered_answer:
                flash("Please enter an answer", "error")  # Show error if no answer entered
            elif entered_answer.replace('́', '&#769;') != questions_v["1_base_altern"][session["current_question"]]["answer"]:
                flash("La bonne réponse:\n" + questions_v["1_base_altern"][session["current_question"]]["answer"], "error")
            else:
                session["current_question"] = str(int(session["current_question"]) + 1)
                if session["current_question"] in questions_v:
                    redirect(url_for('testb_1_base_altern'))
                else:
                    return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=0)
        if "current_question" not in session:
            session["current_question"] = "1"
        elif session["current_question"] not in questions_v["1_base_altern"]:
            session.pop("current_question")
            return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=1)
        return render_template("test_backw.html",
                               question=questions_v["1_base_altern"][session["current_question"]]["question"],
                               question_number=session["current_question"],
                               profile_refer=profile_refer, quizes_refer=quizes_refer, cat='1_base_altern')
    except NameError:
        redirect(url_for('vocab_verbs'))


@app.route('/materials/testb_1_avec_diff', methods=['GET', 'POST'])
def testb_1_avec_diff():
    questions_v = session['quest_b_v']
    try:
        profile_refer = url_for('profile_page')
        quizes_refer = url_for('quizes_page')
        if request.method == "POST":
            entered_answer = request.form.get('answer', '')
            if not entered_answer:
                flash("Please enter an answer", "error")  # Show error if no answer entered
            elif entered_answer.replace('́', '&#769;') != questions_v["1_avec_diff"][session["current_question"]]["answer"]:
                flash("La bonne réponse:\n" + questions_v["1_avec_diff"][session["current_question"]]["answer"], "error")
            else:
                session["current_question"] = str(int(session["current_question"]) + 1)
                if session["current_question"] in questions_v:
                    redirect(url_for('testb_1_avec_diff'))
                else:
                    return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=0)
        if "current_question" not in session:
            session["current_question"] = "1"
        elif session["current_question"] not in questions_v["1_avec_diff"]:
            session.pop("current_question")
            return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=1)
        return render_template("test_backw.html",
                               question=questions_v["1_avec_diff"][session["current_question"]]["question"],
                               question_number=session["current_question"],
                               profile_refer=profile_refer, quizes_refer=quizes_refer, cat='1_avec_diff')
    except NameError:
        redirect(url_for('vocab_verbs'))


@app.route('/materials/testb_1_sans_diff', methods=['GET', 'POST'])
def testb_1_sans_diff():
    questions_v = session['quest_b_v']
    try:
        profile_refer = url_for('profile_page')
        quizes_refer = url_for('quizes_page')
        if request.method == "POST":
            entered_answer = request.form.get('answer', '')
            if not entered_answer:
                flash("Please enter an answer", "error")  # Show error if no answer entered
            elif entered_answer.replace('́', '&#769;') != questions_v["1_sans_diff"][session["current_question"]]["answer"]:
                flash("La bonne réponse:\n" + questions_v["1_sans_diff"][session["current_question"]]["answer"], "error")
            else:
                session["current_question"] = str(int(session["current_question"]) + 1)
                if session["current_question"] in questions_v:
                    redirect(url_for('testb_1_sans_diff'))
                else:
                    return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=0)
        if "current_question" not in session:
            session["current_question"] = "1"
        elif session["current_question"] not in questions_v["1_sans_diff"]:
            session.pop("current_question")
            return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=1)
        return render_template("test_backw.html",
                               question=questions_v["1_sans_diff"][session["current_question"]]["question"],
                               question_number=session["current_question"],
                               profile_refer=profile_refer, quizes_refer=quizes_refer, cat='1_sans_diff')
    except NameError:
        redirect(url_for('vocab_verbs'))


@app.route('/materials/testb_2_productif', methods=['GET', 'POST'])
def testb_2_productif():
    questions_v = session['quest_b_v']
    try:
        profile_refer = url_for('profile_page')
        quizes_refer = url_for('quizes_page')
        if request.method == "POST":
            entered_answer = request.form.get('answer', '')
            if not entered_answer:
                flash("Please enter an answer", "error")  # Show error if no answer entered
            elif entered_answer.replace('́', '&#769;') != questions_v["2_productif"][session["current_question"]]["answer"]:
                flash("La bonne réponse:\n" + questions_v["2_productif"][session["current_question"]]["answer"], "error")
            else:
                session["current_question"] = str(int(session["current_question"]) + 1)
                if session["current_question"] in questions_v:
                    redirect(url_for('testb_2_productif'))
                else:
                    return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=0)
        if "current_question" not in session:
            session["current_question"] = "1"
        elif session["current_question"] not in questions_v["2_productif"]:
            session.pop("current_question")
            return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=1)
        return render_template("test_backw.html",
                               question=questions_v["2_productif"][session["current_question"]]["question"],
                               question_number=session["current_question"],
                               profile_refer=profile_refer, quizes_refer=quizes_refer, cat='2_productif')
    except NameError:
        redirect(url_for('vocab_verbs'))


@app.route('/materials/testb_2_improductif', methods=['GET', 'POST'])
def testb_2_improductif():
    questions_v = session['quest_b_v']
    try:
        profile_refer = url_for('profile_page')
        quizes_refer = url_for('quizes_page')
        if request.method == "POST":
            entered_answer = request.form.get('answer', '')
            if not entered_answer:
                flash("Please enter an answer", "error")  # Show error if no answer entered
            elif entered_answer.replace('́', '&#769;') != questions_v["2_improductif"][session["current_question"]]["answer"]:
                flash("La bonne réponse:\n" + questions_v["2_improductif"][session["current_question"]]["answer"], "error")
            else:
                session["current_question"] = str(int(session["current_question"]) + 1)
                if session["current_question"] in questions_v:
                    redirect(url_for('testb_2_improductif'))
                else:
                    return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=0)
        if "current_question" not in session:
            session["current_question"] = "1"
        elif session["current_question"] not in questions_v["2_improductif"]:
            session.pop("current_question")
            return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=1)

        return render_template("test_backw.html",
                               question=questions_v["2_improductif"][session["current_question"]]["question"],
                               question_number=session["current_question"],
                               profile_refer=profile_refer, quizes_refer=quizes_refer, cat='2_improductif')
    except NameError:
        redirect(url_for('vocab_verbs'))



"""---------------------------------------------------------------------------------------------------"""

@app.route('/materials/vocab_adverbs')
def vocab_adverbs():
    ps = 'adv'
    cat = ['adv']
    session['questions_adv'] = quiz_maker(ps, cat, sorting)
    session['quest_b_adv'] = quiz_maker(ps, cat, sorting_back)
    voc = voc_maker(ps, cat)
    profile_refer = url_for('profile_page')
    quizes_refer = url_for('quizes_page')
    test_refer = url_for('test_1d')
    return render_template('vocab.html',
                           profile_refer=profile_refer, quizes_refer=quizes_refer, test_refer=test_refer,
                           mama=cat, voc=voc, vocab_category="L'Adverbe")


@app.route('/materials/test_adv', methods=['GET', 'POST'])
def test_adv():
    questions_adv = session['questions_adv']
    try:
        profile_refer = url_for('profile_page')
        quizes_refer = url_for('quizes_page')
        if request.method == "POST":
            entered_answer = request.form.get('answer', '')
            if not entered_answer:
                flash("Please enter an answer", "error")  # Show error if no answer entered
            elif entered_answer != questions_adv["adv"][session["current_question"]]["answer"]:
                flash("La bonne réponse:\n" + questions_adv["adv"][session["current_question"]]["answer"],
                      "error")
            else:
                session["current_question"] = str(int(session["current_question"]) + 1)
                if session["current_question"] in questions_adv:
                    redirect(url_for('test_adv'))
                else:
                    return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=0)
        if "current_question" not in session:
            session["current_question"] = "1"
        elif session["current_question"] not in questions_adv["adv"]:
            session.pop("current_question")
            return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=1)

        return render_template("test_page.html",
                               question=questions_adv["adv"][session["current_question"]]["question"],
                               question_number=session["current_question"],
                               profile_refer=profile_refer, quizes_refer=quizes_refer, cat='adv')
    except NameError:
        redirect(url_for('vocab_adverbs'))


@app.route('/materials/testb_adv', methods=['GET', 'POST'])
def testb_adv():
    questions_adv = session['quest_b_adv']
    try:
        profile_refer = url_for('profile_page')
        quizes_refer = url_for('quizes_page')
        if request.method == "POST":
            entered_answer = request.form.get('answer', '')
            if not entered_answer:
                flash("Please enter an answer", "error")  # Show error if no answer entered
            elif entered_answer.replace('́', '&#769;') != questions_adv["adv"][session["current_question"]]["answer"]:
                flash("La bonne réponse:\n" + questions_adv["adv"][session["current_question"]]["answer"],
                      "error")
            else:
                session["current_question"] = str(int(session["current_question"]) + 1)
                if session["current_question"] in questions_adv:
                    redirect(url_for('test_adv'))
                else:
                    return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=0)
        if "current_question" not in session:
            session["current_question"] = "1"
        elif session["current_question"] not in questions_adv["adv"]:
            session.pop("current_question")
            return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=1)

        return render_template("test_backw.html",
                               question=questions_adv["adv"][session["current_question"]]["question"],
                               question_number=session["current_question"],
                               profile_refer=profile_refer, quizes_refer=quizes_refer, cat='adv')
    except NameError:
        redirect(url_for('vocab_adverbs'))


if __name__ == '__main__':
    app.run(debug=True)