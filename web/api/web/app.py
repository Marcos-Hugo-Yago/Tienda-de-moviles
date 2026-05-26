from flask import Flask, request, make_response
import os
import json
import logging
from logging.config import dictConfig
from funciones_auxiliares import Encoder, sanitize_field, prepare_response_extra_headers
from flask_wtf.csrf import CSRFProtect

def create_app():
    os.makedirs('logs', exist_ok=True)

    try:
        dictConfig(
            {
                "version": 1,
                "formatters": {
                    "default": {
                        "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
                    }
                },
                "handlers": {
                    "console": {
                        "class": "logging.StreamHandler",
                        "stream": "ext://sys.stdout",
                        "formatter": "default",
                    },
                    "time-rotate": {
                        "class": "logging.handlers.TimedRotatingFileHandler",
                        "filename": "logs/flask.log",
                        "when": "D",
                        "interval": 10,
                        "backupCount": 5,
                        "formatter": "default",
                    },
                },
                "root": {"level": "DEBUG", "handlers": ["console", "time-rotate"]},
            }
        )
    except Exception as e:
        logging.basicConfig(level=logging.DEBUG)
        print("Warning: File logging not available: %s" % e, flush=True)

    app = Flask(__name__)

    extra_headers = prepare_response_extra_headers(True)

    app.config.update(
        DEBUG=True,
        SECRET_KEY=os.getenv("SECRET_KEY", "clave-defecto-no-usar-en-produccion"),
        PERMANENT_SESSION_LIFETIME=600,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
    )

    app.config['WTF_CSRF_CHECK_DEFAULT'] = False
    csrf = CSRFProtect(app)

    @app.before_request
    def csrf_protect():
        if (not request.path.startswith("/api/usuarios/login")
            and not request.path.startswith("/api/usuarios/registro")
            and not request.path.startswith("/api/comentarios/")):
            csrf.protect()

    @app.before_request
    def clean_request():
        if request.is_json and not request.path.startswith("/api/comentarios/"):
            data = request.get_json(silent=True)
            if data is not None:
                request._cached_json = (sanitize_field(data), False)

    @app.after_request
    def afterRequest(response):
        response.headers['Server'] = 'API'
        app.logger.info(
            "path: %s | method: %s | status: %s | size: %s >>> %s",
            request.path,
            request.method,
            response.status,
            response.content_length,
            request.remote_addr,
        )
        response.headers.extend(extra_headers)
        return response

    @app.errorhandler(500)
    def server_error(error):
        app.logger.error('An exception occurred during a request. ERROR: %s', error)
        ret = {"status": "Internal Server Error"}
        return make_response(json.dumps(ret, cls=Encoder), 500)

    from rutas_usuarios import bp as usuarios_bp
    app.register_blueprint(usuarios_bp, url_prefix='/api/usuarios')

    from rutas_Moviles import bp as Moviles_bp
    app.register_blueprint(Moviles_bp, url_prefix='/api/Moviles')

    from rutas_ficheros import bp as ficheros_bp
    app.register_blueprint(ficheros_bp, url_prefix='/api/ficheros')

    from rutas_comentarios import bp as comentarios_bp
    app.register_blueprint(comentarios_bp, url_prefix='/api/comentarios')

    return app

if __name__ == '__main__':
    app = create_app()
    try:
        port = int(os.environ.get('PORT', 8080))
        host = os.environ.get('HOST', '0.0.0.0')
        app.run(host=host, port=port)
    except Exception as e:
        print("Error starting server: %s" % e, flush=True)
