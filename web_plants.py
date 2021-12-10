from flask import Flask, render_template, redirect, url_for, request
import psutil
import datetime
import water
import os

app = Flask(__name__)

def template(title = "Locsoló", text = ""):
    now = datetime.datetime.now()
    timeString = now
    templateDate = {
        'title' : title,
        'time' : timeString,
        'text' : text
        }
    return templateDate

@app.route("/")
def hello():
    templateData = template()
    return render_template('main.html', **templateData)

@app.route("/last_watered")
def check_last_watered():
    templateData = template(text = water.get_last_watered())
    return render_template('main.html', **templateData)

@app.route("/sensor")
def action():
    status = water.get_status()
    message = ""
    if (status == 1):
        message = "A talaj száraz"
    else:
        message = "A talaj nedves"

    templateData = template(text = message)
    return render_template('main.html', **templateData)

@app.route("/water")
def action2():
    water.pump_on()
    templateData = template(text = "Egyszeri öntözés")
    return render_template('main.html', **templateData)

@app.route('/', methods=['POST'])
def input():
    tank = request.form["tank"]
    templateData = template(text = "A megadott mennyiség: " + tank + " liter")
    f = open("tankCapacity.txt", "w")
    f.write(tank)
    f.close()
    return render_template('main.html', **templateData)

@app.route("/auto/water/<toggle>")
def auto_water(toggle):
    running = False
    if toggle == "ON":
        templateData = template(text = "Automatikus öntözés bekapcsolva")
        for process in psutil.process_iter():
            try:
                if process.cmdline()[1] == 'auto_water.py':
                    templateData = template(text = "A rendszer már fut")
                    running = True
            except:
                pass
        if not running:
            os.system("python3 auto_water.py&")
    else:
        templateData = template(text = "Automatikus öntözés kikapcsolva")
        os.system("pkill -f water.py")

    return render_template('main.html', **templateData)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
