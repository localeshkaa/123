import psycopg2 as p
from flask import Flask
from flask import redirect, render_template, abort, request
from random import randint

def set_username(id, username):
    con = p.connect(dbname='testdb', user='postgres',
                    password='JLhP1CgJ225603', host='localhost')

    cr = con.cursor()

    cr.execute("UPDATE tablet SET username = '{0}' WHERE id = '{1}';".format(username, id))
    con.commit()
    con.close()

def set_fraction(id, fraction):
    con = p.connect(dbname='testdb', user='postgres',
                    password='JLhP1CgJ225603', host='localhost')

    cr = con.cursor()

    cr.execute("UPDATE tablet SET fraction = '{0}' WHERE id = '{1}';".format(fraction, id))
    con.commit()
    con.close()

def check_name(string):
    res = False
    res += ' ' in string
    res += '&' in string
    res += '?' in string
    res += '!' in string
    res += '@' in string
    res += ':' in string
    return res



def add(data):
    frac = ['Blue', 'Red', 'Green', 'Black', 'White']
    con = p.connect(dbname='testdb', user='postgres',
                    password='JLhP1CgJ225603', host='localhost')

    cr = con.cursor()

    cr.execute("INSERT INTO tablet(username, id, level, fraction) VALUES ('{0}', '{1:06d}', '{2}', '{3}');".format(data,
                                                                                                               randint(0, 999999),
                                                                                                               randint(1, 99),
                                                                                                               frac[randint(0, len(frac))]))


    con.commit()
    con.close()

def get_data():
    con = p.connect(dbname='testdb', user='postgres',
                    password='JLhP1CgJ225603', host='localhost')

    cr = con.cursor()

    cr.execute("SELECT * FROM tablet;")
    data = cr.fetchall()

    con.commit()
    con.close()

    all_data = []
    for record in data:
        all_data.append({'username': record[0], 'id': record[1], 'lvl': record[2], 'frac': record[3]})
    return all_data

app = Flask(__name__)


@app.route('/')
def home():
    return redirect('/users/')


@app.route('/users/', methods=['post', 'get'])
def users():
    username = ''
    message = ''
    if request.method == 'POST':
        username = request.form.get('username')

    if username != '':
        if check_name(username) == 0:
            add(username)
        else:
            message = "Wrong username format"

    clickers = []
    for record in get_data():
        clickers.append(['/users/{0}'.format(record['id']), record['username']])
    return render_template("list.html", data=clickers, message=message)

@app.route('/users/<id>', methods=['post', 'get'])
def profile(id):
    username = ''
    fraction = None
    if request.method == 'POST':
        username = request.form.get('username')
        fraction = request.form.get('fraction')

    if username != '':
        if check_name(username) == 0:
            set_username(id, username)
        else:
            message = "Wrong username format"
    if fraction != None:
            set_fraction(id, fraction)
    else:
        pass

    id_list = []
    for record in get_data():
        id_list.append(record['id'])
    if id in id_list:
        i = id_list.index(id)
        return render_template("profile.html", data=get_data()[i])
    else:
        abort(404)


if __name__ == '__main__':
    app.run(debug=True)