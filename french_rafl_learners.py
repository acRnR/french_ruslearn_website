from flask import Flask
from flask import url_for, render_template, request, redirect

app = Flask(__name__)


@app.route('/')
def material_page():
    profile_refer = url_for('profile_page')
    quizes_refer = url_for('quizes_page')
    return render_template('vocab.html', profile_refer=profile_refer, quizes_refer=quizes_refer)


@app.route('/profile_page')
def profile_page():
    materials_refer = url_for('material_page')
    quizes_refer = url_for('quizes_page')
    return render_template('profile_page.html', materials_refer=materials_refer, quizes_refer=quizes_refer)

@app.route('/quizes_page')
def quizes_page():
    materials_refer = url_for('material_page')
    profile_refer = url_for('profile_page')
    return render_template('quizes_page.html', materials_refer=materials_refer, profile_refer=profile_refer)

if __name__ == '__main__':
    app.run(debug=True)
