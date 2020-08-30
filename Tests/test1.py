from flask import Flask, render_template

app = Flask(__name__)

posts = [
    {
        'author' : 'Smyk',
        'title' : 'Post 1',
        'content' : 'The post below me is stupid.',
        'date' : 'August 30, 2020'
    },
    {
        'author' : 'Bhgt',
        'title' : 'Post 2',
        'content' : 'The post above me is stupid.',
        'date' : 'August 29, 2020'
    },
    {
        'author' : 'Bhgt',
        'title' : 'Post 3',
        'content' : 'I dunno why I posted this.',
        'date' : 'August 29, 2020'
    },
    {
        'author' : 'Smyk',
        'title' : 'Post 4',
        'content' : 'This website sucks.',
        'date' : 'August 29, 2020'
    },
    {
        'author' : 'Meseeks',
        'title' : 'Oweee!',
        'content' : 'EXISTENCE IS PAIN!!',
        'date' : 'August 1, 2020'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts= posts)


@app.route("/about")
def about():
    return render_template('about.html', title= 'About')


if __name__=="__main__":
    app.run(debug=True)