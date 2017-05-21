import os
import random
from flask import Flask
from flask import url_for, render_template, request, redirect, flash, session
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.sql import select
import html


app = Flask(__name__, static_url_path='')
app.secret_key = os.urandom(24)
# todo: сделать собирание тестов на более раннем этапе


def distance(a, b):
    # "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a, b = b, a
        n, m = m, n

    current_row = range(n+1) # Keep current and previous row, not entire matrix
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
    db_path = 'vocabulary.db'
    engine = create_engine('sqlite:///%s' % db_path, echo=False)
    metadata = MetaData(engine)
    need = Table(tbl, metadata, autoload=True)
    mapper(Words, need)
    sessionmaker(bind=engine)
    conn = engine.connect()
    s = select([need])
    result = conn.execute(s)
    return result


def voc_maker(ps, categories):
    result = call_db('rus_words')
    d = sorting(result, ps, categories)
    #print('vocmaker OFF\n', d)
    return d


def sorting(data, ps, categories, f=None):
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


def sorting_back(data, ps, categories, f=None):
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


def gramm_sorting(data, ps, categories, f):
    forms = f()
    d = {}
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


def quiz_maker(ps, cat, sorter, func=None):
    #print('quizmaker ON')
    result = call_db('rus_words')
    d = sorter(result, ps, cat, func)
    newd = {}
    for key in d:#{'1d':[['лол', 'lol'], ['шта', 'wut']]}
        try:
            quiz_mater = random.sample(d[key], 5)
            quests = {}
            i = 1
            for row in quiz_mater:
                quests[str(i)] = {"question": row[0], "answer": row[1]}
                i += 1
                newd[key] = quests
        except ValueError:
            print(key)
            continue
    #{ cat : [ 1 : {"question": row[0], "answer": row[1]}, 2 : {"question": row[0], "answer": row[1]} }]
    #print('quizmaker OFF')
    #print(newd)
    return newd
"""-------------------------------------------------------------------------"""


@app.route('/')
def profile_page():
    profile_refer = url_for('profile_page')
    quizes_refer = url_for('quizes_page')
    #test_refer = url_for('test_1d')
    n_v = url_for('vocab_nouns')
    v_v = url_for('vocab_verbs')
    a_v = url_for('vocab_adverbs')
    #session['ex_genpl'] = ex_genpl_maker()
    # todo: добавить ссылки на тесты
    return render_template('profile_page.html',
                           profile_refer=profile_refer, quizes_refer=quizes_refer,#test_refer=test_refer,
                           noun_voc=n_v, verb_voc=v_v, adv_voc=a_v)


@app.route('/quizes_page')
def quizes_page():
    profile_refer = url_for('profile_page')
    return render_template('quizes_page.html', profile_refer=profile_refer)
"""-------------------------------------------------------------------------"""


@app.route('/materials/test_<categ>', methods=['GET', 'POST'])
def test(categ):
    cs = {
        '1d': 'n', 'm': 'n', 'n':'n', '3d':'n', 'sg_tantum':'n', 'pl_tantum':'n',
        '1_productif': 'v', '1_sans_diff': 'v', '1_avec_diff': 'v', '1_base_altern': 'v', '2_productif': 'v', '2_improductif': 'v',
        'adv': 'adv'
    }
    questions = session['questions_' + cs[categ]]
    try:
        profile_refer = url_for('profile_page')
        quizes_refer = url_for('quizes_page')
        if request.method == "POST":
            entered_answer = request.form.get('answer', '')
            if not entered_answer:
                flash("Please enter an answer", "error")  # Show error if no answer entered
            elif entered_answer != questions[categ][session["current_question"]]["answer"]:
                flash("La bonne réponse:\n" + questions[categ][session["current_question"]]["answer"],
                      "error")
            else:
                session["current_question"] = str(int(session["current_question"]) + 1)
                if session["current_question"] in questions:
                    redirect(url_for('test', categ=categ))
                else:
                    return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=0)
        if "current_question" not in session:
            session["current_question"] = "1"
        elif session["current_question"] not in questions[categ]:
            session.pop("current_question")
            return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=1)
        return render_template("test_page.html",
                               question=questions[categ][session["current_question"]]["question"],
                               question_number=session["current_question"],# pg=url_for('test', categ=categ),
                               profile_refer=profile_refer, quizes_refer=quizes_refer, cat=categ)
    except NameError:
        redirect(url_for('vocab_verbs'))


@app.route('/materials/testb_<categ>', methods=['GET', 'POST'])
def testb(categ):
    cs = {
        '1d': 'n', 'm': 'n', 'n': 'n', '3d': 'n', 'sg_tantum': 'n', 'pl_tantum': 'n',
        '1_productif': 'v', '1_sans_diff': 'v', '1_avec_diff': 'v', '1_base_altern': 'v', '2_productif': 'v',
        '2_improductif': 'v',
        'adv': 'adv'
    }
    questions = session['quest_b_' + cs[categ]]
    try:
        profile_refer = url_for('profile_page')
        quizes_refer = url_for('quizes_page')
        if request.method == "POST":
            entered_answer = request.form.get('answer', '')
            if not entered_answer:
                flash("Please enter an answer", "error")  # Show error if no answer entered
            elif entered_answer.replace('́', '&#769;') != questions[categ][session["current_question"]]["answer"]:
                flash("La bonne réponse:\n" + questions[categ][session["current_question"]]["answer"], "error")
            else:
                session["current_question"] = str(int(session["current_question"]) + 1)
                if session["current_question"] in questions:
                    redirect(url_for('testb', categ=categ))
                else:
                    return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=0)
        if "current_question" not in session:
            session["current_question"] = "1"
        elif session["current_question"] not in questions[categ]:
            session.pop("current_question")
            return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=1)
        return render_template("test_backw.html",
                               question=questions[categ][session["current_question"]]["question"],
                               question_number=session["current_question"],
                               profile_refer=profile_refer, quizes_refer=quizes_refer, cat=categ)
    except NameError:
        redirect(url_for('vocab_nouns'))

#todo: добавить подсказки правил
@app.route('/materials/genpl_<categ>', methods=['GET', 'POST'])
def test_gen(categ):
    # questions_adv = session['quest_b_adv']
    questions = session['ex_genpl']
    try:
        profile_refer = url_for('profile_page')
        quizes_refer = url_for('quizes_page')
        if request.method == "POST":
            entered_answer = request.form.get('answer', '')
            if not entered_answer:
                flash("Please enter an answer", "error")  # Show error if no answer entered
            elif entered_answer.replace('́', '&#769;') != questions[categ][session["current_question"]]["answer"]:
                flash("La bonne réponse:\n" + questions[categ][session["current_question"]]["answer"],
                      "error")
            else:
                session["current_question"] = str(int(session["current_question"]) + 1)
                if session["current_question"] in questions:
                    redirect(url_for('genpl_', categ=categ))
                else:
                    return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=0)
        if "current_question" not in session:
            session["current_question"] = "1"
        elif session["current_question"] not in questions[categ]:
            session.pop("current_question")
            return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=1)

        return render_template("test_gen.html",
                               question=questions[categ][session["current_question"]]["question"],
                               question_number=session["current_question"],
                               profile_refer=profile_refer, quizes_refer=quizes_refer, cat=categ)
    except NameError:
        redirect(url_for('vocab_adverbs'))

#todo: добавить подсказки правил
@app.route('/materials/conj_<categ>', methods=['GET', 'POST'])
def test_conj(categ):
    # questions_adv = session['quest_b_adv']
    questions = session['ex_conj']
    try:
        profile_refer = url_for('profile_page')
        quizes_refer = url_for('quizes_page')
        if request.method == "POST":
            entered_answer = request.form.get('answer', '')
            if not entered_answer:
                flash("Please enter an answer", "error")  # Show error if no answer entered
            elif entered_answer.replace('́', '&#769;') != questions[categ][session["current_question"]]["answer"]:
                flash("La bonne réponse:\n" + questions[categ][session["current_question"]]["answer"],
                      "error")
            else:
                session["current_question"] = str(int(session["current_question"]) + 1)
                if session["current_question"] in questions:
                    redirect(url_for('conj_', categ=categ))
                else:
                    return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=0)
        if "current_question" not in session:
            session["current_question"] = "1"
        elif session["current_question"] not in questions[categ]:
            session.pop("current_question")
            return render_template("success.html", profile_refer=profile_refer, quizes_refer=quizes_refer, a=1)
        return render_template("test_conj.html",
                               question=questions[categ][session["current_question"]]["question"],
                               question_number=session["current_question"],
                               profile_refer=profile_refer, quizes_refer=quizes_refer, cat=categ)
    except NameError:
        redirect(url_for('vocab_adverbs'))
"""------------------------------------------------------------------------"""


@app.route('/materials/vocab_nouns')
def vocab_nouns():
    ps = 's'
    cat = ['1d', 'm', 'n', '3d', 'sg_tantum', 'pl_tantum']
    session['questions_n'] = quiz_maker(ps, cat, sorting)
    session['quest_b_n'] = quiz_maker(ps, cat, sorting_back)
    session['ex_genpl'] = quiz_maker(ps, cat, gramm_sorting, ex_genpl_maker)
    voc = voc_maker(ps, cat)
    profile_refer = url_for('profile_page')
    quizes_refer = url_for('quizes_page')
    #a1d = url_for('test_1d')
    return render_template('vocab.html',
                           profile_refer=profile_refer, quizes_refer=quizes_refer,# test_refer=test_refer,
                           mama=cat, voc=voc, vocab_category='Le Substantif')#,
                           #a1d=a1d)


@app.route('/materials/vocab_verbs')
def vocab_verbs():
    ps = 'v'
    cat = ['1_productif', '1_sans_diff', '1_avec_diff', '1_base_altern', '2_productif', '2_improductif']
    session['questions_v'] = quiz_maker(ps, cat, sorting)
    session['quest_b_v'] = quiz_maker(ps, cat, sorting_back)
    session['ex_conj'] = quiz_maker(ps, cat, gramm_sorting, prs_conj_maker)
    voc = voc_maker(ps, cat)
    profile_refer = url_for('profile_page')
    quizes_refer = url_for('quizes_page')
    #test_refer = url_for('test_page')
    return render_template('vocab.html',
                           profile_refer=profile_refer, quizes_refer=quizes_refer,# test_refer=test_refer,
                           mama=cat, voc=voc, vocab_category='Le Verbe')


@app.route('/materials/vocab_adverbs')
def vocab_adverbs():
    ps = 'adv'
    cat = ['adv']
    session['questions_adv'] = quiz_maker(ps, cat, sorting)
    session['quest_b_adv'] = quiz_maker(ps, cat, sorting_back)
    voc = voc_maker(ps, cat)
    profile_refer = url_for('profile_page')
    quizes_refer = url_for('quizes_page')
    #test_refer = url_for('test_1d')
    return render_template('vocab.html',
                           profile_refer=profile_refer, quizes_refer=quizes_refer,# test_refer=test_refer,
                           mama=cat, voc=voc, vocab_category="L'Adverbe")


#@app.route('/keyboard')
#def keyboard():
 #   return render_template('keyb.html')


if __name__ == '__main__':
    app.run(debug=True)
