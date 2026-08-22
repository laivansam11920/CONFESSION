from flask import request

def get_locale():
    lang = request.args.get('lang')
    if lang in ['vi', 'en']:
        return lang
    return request.accept_languages.best_match(['vi', 'en'])
