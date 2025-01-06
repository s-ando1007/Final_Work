import random
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

TRIVIA_API_URL = "https://opentdb.com/api.php?amount=1&difficulty=easy&type=multiple"
TRANSLATE_API_URL = "https://api.mymemory.translated.net/get"

# 緊急時の問題
STATIC_QUESTIONS = [
    {"scenario": "秒速5mで走る自転車がいます。10秒間走ったときの距離は何mですか？", "choices": ["50", "100"], "correct": "50"},
    {"scenario": "1週間は何日ですか？", "choices": ["6", "7"], "correct": "7"},
    {"scenario": "1mは何cmですか？", "choices": ["100", "1000"], "correct": "100"},
    {"scenario": "三角形の角度の合計は何度ですか？", "choices": ["180度", "360度"], "correct": "180度"},
    {"scenario": "桃太郎は誰を倒した？", "choices": ["鬼", "魔人"], "correct": "鬼"}
]

# 問題取得
def translate_to_japanese(text):
    try:
        response = requests.get(TRANSLATE_API_URL, params={"q": text, "langpair": "en|ja"})
        data = response.json()
        return data["responseData"]["translatedText"]
    except:
        return text

def fetch_question():
    try:
        response = requests.get(TRIVIA_API_URL)
        trivia_data = response.json()
        if trivia_data["response_code"] == 0:
            result = trivia_data["results"][0]
            question = translate_to_japanese(result["question"])
            correct = translate_to_japanese(result["correct_answer"])
            incorrect = translate_to_japanese(result["incorrect_answers"][0])
            choices = [correct, incorrect]
            random.shuffle(choices)
            return {"scenario": question, "choices": choices, "correct": correct}
    except:
        return random.choice(STATIC_QUESTIONS)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/game')
def game():
    return render_template('index.html')

@app.route('/get_question/<int:question_num>', methods=['GET'])
def get_question(question_num):
    question = fetch_question()
    return jsonify(question)

@app.route('/check_answer', methods=['POST'])
def check_answer():
    data = request.json
    user_choice = data.get('choice')
    correct = data.get('correct')

    if user_choice == correct:
        return jsonify({"result": "correct"})
    else:
        return jsonify({"result": "incorrect"})

if __name__ == '__main__':
    app.run(debug=True)