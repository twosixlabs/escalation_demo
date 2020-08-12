from utility.constants import APP_CONFIG_JSON, DATA_BACKEND, POSTGRES


def configure_backend(app):
    # setup steps unique to SQL-backended apps
    if app.config[APP_CONFIG_JSON][DATA_BACKEND] in [POSTGRES]:
        from database.sql_handler import SqlHandler, SqlDataInventory
        from database.database import db, db_session

        db.init_app(app)
        data_backend_class = SqlHandler
        data_backend_writer = SqlDataInventory

        @app.teardown_appcontext
        def shutdown_session(exception=None):
            db_session.remove()

    else:
        from database.local_handler import LocalCSVHandler, LocalCSVDataInventory

        data_backend_class = LocalCSVHandler
        data_backend_writer = LocalCSVDataInventory

    app.config.data_handler = data_backend_class
    app.config.data_backend_writer = data_backend_writer
