import os

from flask import Flask, render_template, redirect, request
from jinja2 import environment

import create_filesystem

app = Flask(__name__)
app.jinja_env.filters['style'] = lambda u: style(u)

data, topics = create_filesystem.get_data_for_html()
topics = topics[::-1]


# APP = 'start "D:\\!t\\PyCharm 2020.2\\bin\\pycharm64.exe" "{}"'
APP = '"C:\\Users\\Nishan Paudel\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe" "{}"'


def style(field):
    if field.endswith("*"): # IMP, orange
        return 'color:orangered'
    elif field.endswith(':'): # Change in topic, dark green
        return 'color:darkolivegreen;text-decoration: underline;'
    return 'adfs'
#
# environment.tests['is_java'] = is_link_field
@app.template_filter()
def is_java_file(file_name):
    print(file_name)
    return file_name.endswith('java')


global_topic = topics[0]
@app.route('/config')
def open_config_file():
    print(global_topic)
    os.popen(APP.format('D:\Projects\DSA\data.txt'))

    return redirect('/')


@app.route('/<topic>/<id>')
def open_path(topic, id):
    global global_topic 
    global_topic = topic
    # print('Got here', topic, id)
    id_path = {}
    for question_name, question in data[topic].items():
        for subquestions in question['sub_questions']:
            id_path[subquestions['id']] = subquestions['path']
    print(id in id_path.keys())
    print(id_path[id])
    os.popen(APP.format(id_path[id]))
    return redirect('/'+topic)
    # return render_template('main.html', data={'questions': data[topic], 'current_topic': topic, 'topics': topics})
    # pprint(id_path)
    # print(data[topic])


@app.route('/<topic>')
def change_topic(topic):
    global global_topic 
    global_topic = topic
    print(topic)
    return render_template('main.html', data={'questions': data[topic], 'current_topic': topic, 'topics': topics})


@app.route('/')
def hello_world():
    return render_template('main.html',
                           data={'questions': data[topics[0]], 'current_topic': topics[0], 'topics': topics})


if __name__ == '__main__':
    app.run()
