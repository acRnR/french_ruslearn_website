from flask import Flask
from flask import url_for, render_template, request, redirect
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)


@app.route('/')
def material_page():
    profile_refer = url_for('profile_page')
    quizes_refer = url_for('quizes_page')
    test_refer = url_for('test_page')
    # todo: чтобы возвращал страницу со ссылками на все материалы и тесты, а не vocab.html
    return render_template('vocab.html',
                           profile_refer=profile_refer, quizes_refer=quizes_refer, test_refer=test_refer)


@app.route('/profile_page')
def profile_page():
    materials_refer = url_for('material_page')
    quizes_refer = url_for('quizes_page')
    return render_template('profile_page.html',
                           materials_refer=materials_refer, quizes_refer=quizes_refer)


@app.route('/quizes_page')
def quizes_page():
    materials_refer = url_for('material_page')
    profile_refer = url_for('profile_page')
    return render_template('quizes_page.html',
                           materials_refer=materials_refer, profile_refer=profile_refer)


@app.route('/test_page')
def test_page():
    profile_refer = url_for('profile_page')
    materials_refer = url_for('material_page')
    quizes_refer = url_for('quizes_page')
    return render_template('test_page.html',
                           profile_refer=profile_refer, materials_refer=materials_refer, quizes_refer=quizes_refer)


@app.route('/materials/vocab_nouns')
def vocab_nouns():

    voc =
    profile_refer = url_for('profile_page')
    quizes_refer = url_for('quizes_page')
    test_refer = url_for('test_page')
    return render_template('vocab.html',
                           profile_refer=profile_refer, quizes_refer=quizes_refer, test_refer=test_refer,
                           voc = voc, vocab_category='Substantif')


if __name__ == '__main__':
    app.run(debug=True)
