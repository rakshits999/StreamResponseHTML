from flask import Flask, render_template, request, Response
import openai
import json

app = Flask(__name__)

openai.api_key = "API_KEY"

def generate_chunks(prompt):
    result = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        stream=True
    )

    for chunk in result:
        response = chunk.choices[0].delta.get("content", "")
        words = response.split()
        for word in words:
            yield word

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response')
def get_response():
    prompt = request.args.get('prompt', '')

    def stream_response():
        chunks_generator = generate_chunks(prompt)
        for word in chunks_generator:
            yield 'data: ' + json.dumps(word) + '\n\n'

    return Response(stream_response(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)
