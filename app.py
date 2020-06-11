from flask import Flask, render_template

from controller import get_graphic

app = Flask(__name__)


@app.route('/')
def plot_test():
    '''
    to be deleted
    proof of concept
    :return:
    '''
    [filename, data] = get_graphic('bar plot', [], [], [])
    return render_template(filename, plot=data)


if __name__ == '__main__':
    app.run()
