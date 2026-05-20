import decimal
import json
import html
import bleach
import bcrypt
import os
import datetime
from werkzeug.http import http_date
from flask import session

class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal): return float(obj)

def calculariva(importe):
    return importe * 0.21

def sanitize_field(data):
    if isinstance(data, str):
        return html.escape(data)
    if isinstance(data, dict):
        return {k: sanitize_field(v) for k, v in data.items()}
    if isinstance(data, list):
        return [sanitize_field(v) for v in data]
    return data

def cipher_password(password):
    PEPPER_KEY = os.getenv("PASSWORD_PEPPER")
    password_peppered = password + PEPPER_KEY
    hashAndSalt = bcrypt.hashpw(password_peppered.encode("utf-8"), bcrypt.gensalt(10))
    return hashAndSalt

def compare_password(password_hash, password):
    if password_hash is None:
        return False
    try:
        PEPPER_KEY = os.getenv("PASSWORD_PEPPER")
        password_peppered = password + PEPPER_KEY
        if isinstance(password_hash, str):
            password_hash = password_hash.encode("utf-8")
        return bcrypt.checkpw(password_peppered.encode("utf-8"), password_hash)
    except:
        return False

def prepare_response_extra_headers(include_security_headers):
    response_extra_headers = {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0',
        'Last-Modified': http_date(datetime.datetime.now()),
        'Server': ''
    }
    if include_security_headers:
        response_security_headers = {
            'X-Frame-Options': 'SAMEORIGIN',
            'Strict-Transport-Security': 'max-age=63072000; includeSubdomains',
            'X-Content-Type-Options': 'nosniff',
            'X-XSS-Protection': '1; mode=block'
        }
        response_extra_headers.update(response_security_headers)
    return response_extra_headers

def create_session(usuario, perfil):
    session["usuario"] = usuario
    session["perfil"] = perfil

def delete_session():
    session.clear()

def validar_session_normal():
    try:
        if session.get("usuario") and session["usuario"] != "":
            return True
        return False
    except:
        return False

def validar_session_admin():
    try:
        if session.get("usuario") and session["usuario"] != "" and session.get("perfil") == "admin":
            return True
        return False
    except:
        return False
