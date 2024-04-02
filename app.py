from flask import Flask, render_template, request
from dotenv import load_dotenv
load_dotenv()

from script import generate_vocab
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        subject = request.form['language']
        grade = request.form['grade']
        level = request.form['level']
        topic = request.form['topic']
        amount = request.form['amount']

        try:
            results = generate_vocab(subject, grade, level, topic, amount)
            return render_template('result.html', result_html=results)
        except Exception as e:
            error_message = str(e)
            return render_template('result.html', error_message=error_message)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
