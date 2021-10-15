from sqlalchemy import engine_from_config

from models import initialize_sql


def main(global_config, **settings):
    """This function returns a Pyramid WSGI application."""
    config = Configurator(settings=settings)
    config.scan("models")  # the "important" line
    engine = engine_from_config(settings, "sqlalchemy.")
    initialize_sql(engine)
    # other statements here
    config.add_handler("main", "/{action}", "myapp.handlers:MyHandler")
    return config.make_wsgi_app()
