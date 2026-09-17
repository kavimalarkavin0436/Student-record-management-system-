from flask import Flask, jsonify, request, render_template_string
import sqlite3

app = Flask(__name__)

def db():
    con = sqlite3.connect('s.db')
    con.execute('CREATE TABLE IF NOT EXISTS stu (id INTEGER PRIMARY KEY, name TEXT)')
    con.commit()
    con.close()
db()

HTML = '''
<h2>Student System</h2>
<input id="n" placeholder="Student Name"> <button onclick="add()">Add</button>
<ul id="list"></ul>
<script>
function load() {
    fetch('/get').then(r => r.json()).then(d => {
        document.getElementById('list').innerHTML = d.map(s => `<li>${s[1]} <button onclick="del(${s[0]})">X</button></li>`).join('');
    });
}
function add() {
    let name = document.getElementById('n').value;
    fetch('/add', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({name})}).then(() => {document.getElementById('n').value=''; load();});
}
function del(id) {
    fetch('/del/'+id, {method:'DELETE'}).then(() => load());
}
load();
</script>
'''

@app.route('/')
def index(): return render_template_string(HTML)

@app.route('/get')
def get():
    con = sqlite3.connect('s.db')
    res = con.execute('SELECT * FROM stu').fetchall()
    con.close()
    return jsonify(res)

@app.route('/add', methods=['POST'])
def add():
    name = request.json['name']
    con = sqlite3.connect('s.db')
    con.execute('INSERT INTO stu (name) VALUES (?)', (name,))
    con.commit()
    con.close()
    return 'OK'

@app.route('/del/<int:id>', methods=['DELETE'])
def delete(id):
    con = sqlite3.connect('s.db')
    con.execute('DELETE FROM stu WHERE id=?', (id,))
    con.commit()
    con.close()
    return 'OK'

if __name__ == '__main__': app.run(port=5000)
    
