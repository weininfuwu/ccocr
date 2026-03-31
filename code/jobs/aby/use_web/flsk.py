#!/usr/bin/env python3
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   flsk.py     250606  cy
#   updated: 260320 add do_shutdown, suppress werkzeug logs
#
#--------1---------2---------3---------4---------5---------6---------7--------#

import json
import logging
import os
import signal
import sys
import threading

from flask import Flask, render_template, request, redirect

[ myself, jobid, flsk_root ] = sys.argv
flsk_tmpl = os.path.join(flsk_root, 'templates')
flsk_stat = os.path.join(flsk_root, 'static')

app = Flask(__name__, static_folder=flsk_stat, template_folder=flsk_tmpl)

logging.getLogger('werkzeug').setLevel(logging.ERROR)

@app.route('/')
def root():
    return render_template('index.html', jobid=jobid)

@app.route('/fabicon.ico')
def favicon():
    return redirect('/static/favicon.ico')

@app.route('/post', methods=['POST'])
def post():
    with open(os.path.join(flsk_root, 'checked.json'), 'w',
                                                encoding='utf-8') as f:
        json.dump(request.json, f, indent=2, ensure_ascii=False)
    return json.dumps({'reply': 'OKOK'})

def do_shutdown():
    try:
        os.kill(os.getpid(), signal.SIGTERM)
    except Exception:
        pass

@app.route('/bye', methods=['GET'])
def bye():
    threading.Thread(target=do_shutdown, daemon=True).start()
    return 'ブラウザは勝手に閉じます'

app.run(host='127.0.0.1', port=5001, debug=False, use_reloader=False)
