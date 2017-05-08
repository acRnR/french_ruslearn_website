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


#questions = { "1" : { "question" : "Which city is the capital of India?", "answer" : "New Delhi"},
 #             "2" : { "question" : "Who is the president of the USA?", "answer" : "Barack Obama" },
  #            "3" : { "question" : "Which is the world's highest mountain?", "answer" : "Mount Everest"},
   #           "4" : { "question" : "Which is the largest star of the solar system?", "answer" : "Sun"},
    #          "5" : { "question" : "How many days are there in a leap year?", "answer" : "366" } }


def voc_maker(ps, categories):
    class Words(object):
        pass

    db_path = 'vocabulary.db'
    engine = create_engine('sqlite:///%s' % db_path, echo=False)
    metadata = MetaData(engine)
    rus_words = Table('rus_words', metadata, autoload=True)
    mapper(Words, rus_words)
    sessionmaker(bind=engine)
    #sess = Session()
    conn = engine.connect()
    s = select([rus_words])
    result = conn.execute(s)


    d = {}
    for row in result:
        if row['part_of_speech'] == ps:
            for category in categories:
                #print('AaAAAAaAAA', row['category'])
                if row['category'] == category or row['extra_info'] == category:
                #arr.append(row)
                    if category not in d:
                        d[category] = []
                    d[category].append([row['Rus'], row['Fran']])
                #arr.append([category, [row['Rus'], row['Fran']]])
                #print('RUS:', row[0], 'FRAN:', row[1])
    #if extra is not None:
     #   for row in result:
      #      if row['extra_info'] == extra:

    return d


def quiz_maker():
    questions = {}

    class Words(object):
        pass

    db_path = 'vocabulary.db'
    engine = create_engine('sqlite:///%s' % db_path, echo=False)
    metadata = MetaData(engine)
    rus_words = Table('rus_words', metadata, autoload=True)
    mapper(Words, rus_words)
    sessionmaker(bind=engine)
    # sess = Session()
    conn = engine.connect()
    s = select([rus_words])
    result = conn.execute(s)

    quiz_mater = random.sample(list(result), 5)

    i = 1
    for row in quiz_mater:
        questions[str(i)] = {"question": row['Rus'], "answer": row['Fran']}
        i += 1
    print('WAAAAT', questions)
    return questions


@app.route('/')
def profile_page():
    profile_refer = url_for('profile_page')
    quizes_refer = url_for('quizes_page')
    test_refer = url_for('test_page')
    n_v = url_for('vocab_nouns')
    v_v = url_for('vocab_verbs')
    a_v = url_for('vocab_adverbs')
    # todo: добавить ссылки на тесты
    return render_template('profile_page.html',
                           profile_refer=profile_refer, quizes_refer=quizes_refer, test_refer=test_refer,
                           noun_voc=n_v, verb_voc=v_v, adv_voc=a_v)


#@app.route('/profile_page')
#def profile_page():
 #   materials_refer = url_for('material_page')
  #  quizes_refer = url_for('quizes_page')
   # return render_template('profile_page.html',
    #                       materials_refer=materials_refer, quizes_refer=quizes_refer)


@app.route('/quizes_page')
def quizes_page():
    profile_refer = url_for('profile_page')
    return render_template('quizes_page.html', profile_refer=profile_refer)


@app.route('/test_page', methods=['GET', 'POST'])
def test_page():
    #questions = quiz_maker()
    try:
        profile_refer = url_for('profile_page')
        quizes_refer = url_for('quizes_page')

        if request.method == "POST":
            entered_answer = request.form.get('answer', '')
            print('AAAAAAA', entered_answer)
            if not entered_answer:
                flash("Please enter an answer", "error")  # Show error if no answer entered
            elif entered_answer != questions[session["current_question"]]["answer"]:
                flash("La bonne réponse:\n" + questions[session["current_question"]]["answer"], "error")
            else:
                session["current_question"] = str(int(session["current_question"]) + 1)
                if session["current_question"] in questions:
                    redirect(url_for('test_page'))
                else:
                    return render_template("success.html")
        if "current_question" not in session:
            session["current_question"] = "1"
        elif session["current_question"] not in questions:
            return render_template("success.html")
        return render_template("test_page.html",
                               question=questions[session["current_question"]]["question"],
                               question_number=session["current_question"],
                               profile_refer=profile_refer, quizes_refer=quizes_refer)
    except NameError:
        redirect(url_for('vocab_nouns'))


@app.route('/materials/vocab_nouns')
def vocab_nouns():
    ps = 's'
    cat = ['1d', 'm', 'n', '3d', 'sg_tantum', 'pl_tantum']
    print(ps, cat)
    global questions
    questions = quiz_maker()
    voc = voc_maker(ps, cat)
    #print('NOOO', voc)
    profile_refer = url_for('profile_page')
    quizes_refer = url_for('quizes_page')
    test_refer = url_for('test_page')
    return render_template('vocab.html',
                           profile_refer=profile_refer, quizes_refer=quizes_refer, test_refer=test_refer,
                           mama=cat, voc=voc, vocab_category='Le Substantif')


@app.route('/materials/vocab_verbs')
def vocab_verbs():
    voc = voc_maker('v')
    profile_refer = url_for('profile_page')
    quizes_refer = url_for('quizes_page')
    test_refer = url_for('test_page')
    return render_template('vocab.html',
                           profile_refer=profile_refer, quizes_refer=quizes_refer, test_refer=test_refer,
                           voc=voc, vocab_category='Le Verbe')


@app.route('/materials/vocab_adverbs')
def vocab_adverbs():
    voc = voc_maker('adv')
    profile_refer = url_for('profile_page')
    quizes_refer = url_for('quizes_page')
    test_refer = url_for('test_page')
    return render_template('vocab.html',
                           profile_refer=profile_refer, quizes_refer=quizes_refer, test_refer=test_refer,
                           voc=voc, vocab_category="L'Adverbe")


if __name__ == '__main__':
    app.run(debug=True)
