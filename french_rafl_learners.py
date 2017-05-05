from flask import Flask
from flask import url_for, render_template, request, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.sql import select
import html


app = Flask(__name__)

def voc_maker(partofsp):
    class Words(object):
        pass

    db_path = 'vocabulary.db'
    engine = create_engine('sqlite:///%s' % db_path, echo=True)
    metadata = MetaData(engine)
    rus_words = Table('rus_words', metadata, autoload=True)
    mapper(Words, rus_words)
    Session = sessionmaker(bind=engine)
    session = Session()
    conn = engine.connect()
    s = select([rus_words])
    result = conn.execute(s)

    arr = []
    # todo: по категориям
    for row in result:
        if row[2] == partofsp:
            arr.append([row[0], row[1]])
            #print('RUS:', row[0], 'FRAN:', row[1])
    return arr


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


@app.route('/test_page')
def test_page():
    profile_refer = url_for('profile_page')
    quizes_refer = url_for('quizes_page')
    return render_template('test_page.html',
                           profile_refer=profile_refer, quizes_refer=quizes_refer)


@app.route('/materials/vocab_nouns')
def vocab_nouns():
    voc = voc_maker('s')
    profile_refer = url_for('profile_page')
    quizes_refer = url_for('quizes_page')
    test_refer = url_for('test_page')
    return render_template('vocab.html',
                           profile_refer=profile_refer, quizes_refer=quizes_refer, test_refer=test_refer,
                           voc = voc, vocab_category='Le Substantif')


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
