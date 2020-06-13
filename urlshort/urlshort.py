from flask import render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint
import json
import os.path
from werkzeug.utils  import secure_filename

bp = Blueprint('urlshort', __name__)

@bp.route('/')
def home():
    return render_template('home.html', codes=session.keys())

#to allow both get and post methods
@bp.route('/your-url', methods=['GET','POST'])
def your_url():
    if request.method == 'POST':
        urls={}

        #to check if file exists and fill those details in urls dictionary
        if os.path.exists('urls.json'):
            with open ('urls.json') as urls_file:
                urls = json.load(urls_file)

        #to check if short name already exists
        if request.form['code'] in urls.keys():
            flash('That short name has already been taken. Please select another name')
            return redirect(url_for('urlshort.home'))

        #to check if input is file or url
        if 'url' in request.form.keys():
            urls[request.form['code']]={'url':request.form['url']}
        else:
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save('C:/Users/dell/Desktop/url-shortner/urlshort/static/user_files/'+full_name)
            urls[request.form['code']]={'file':full_name}

        #to write new url in json
        with open('urls.json','w') as url_file:
            json.dump(urls, url_file)
            session[request.form['code']] = True

        # to go to next page
        return render_template('your_url.html', code=request.form['code'])

    else:
        #return redirect('/')
        return redirect(url_for('urlshort.home'))

#to go to the webpage provided to short code
@bp.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open ('urls.json') as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                    return redirect (url_for('static', filename='user_files/' + urls[code]['file']))
    return abort(404)

#for undefined route
@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

#for json api
@bp.route('/api')
def session_api():
    return jsonify(list(session.keys()))
