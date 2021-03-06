import re
from flask import request, redirect, make_response
from paste import app

import paste.controllers.pastes.converters
from paste.controllers.helpers import render
from paste.controllers.pastes.variables import expires_at
from paste.controllers.pastes.controller import PasteController


@app.route('/paste', methods=['POST'])
def paste():
    try:
        content = request.form['paste[body]']

        if 'paste[restricted]' in request.form and request.form['paste[restricted]'] == '1':
            restricted = True
        else:
            restricted = False

        lang = request.form['paste[lang]']
        if lang == '0':
            lang = 'plain'

        lang = re.sub('[^0-9a-zA-Z]+', '', lang)

        expiration = expires_at(request.form['paste[expir]'])

        uid = PasteController().write(ip_addr=request.remote_addr,
                                      syntax=lang,
                                      expiration=expiration,
                                      contents=content,
                                      private=restricted)

        return redirect('/paste/%s' % uid, code=302)
    except:
        return render('index', errors=['Bla failed j00'])


@app.route('/paste/<browse:paste>')
def view_paste(paste):
    if isinstance(paste, (str, unicode)):
        return paste

    return render('paste', paste=paste)


@app.route('/paste/<browse:paste>/raw')
def view_paste_raw(paste):
    if isinstance(paste, (str, unicode)):
        return paste

    r = make_response(paste['contents'], 200)
    r.headers.set('Content-Type', "text/plain")
    return r

