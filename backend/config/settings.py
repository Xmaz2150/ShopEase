from os import getenv

class Config:
    SEASE_PGSQL_USER = getenv('SEASE_PGSQL_USER') or 'postgres'
    SEASE_PGSQL_PWD = getenv('SEASE_PGSQL_PWD') or 'root'
    SEASE_PGSQL_HOST_PORT = getenv('SEASE_PGSQL_HOST_PORT') or '5432'
    SEASE_PGSQL_HOST = getenv('SEASE_PGSQL_HOST') or 'localhost:{}'.format(SEASE_PGSQL_HOST_PORT)
    SEASE_PGSQL_DB = getenv('SEASE_PGSQL_DB') or 'shopease'
    SEASE_ENV = getenv('SEASE_ENV')
    POSTGRESQL_DATABASE_URI = getenv(
        'DATABASE_URL') or 'postgresql+psycopg2://{}:{}@{}/{}'.format(
            SEASE_PGSQL_USER, SEASE_PGSQL_PWD, SEASE_PGSQL_HOST, SEASE_PGSQL_DB
    )

    IS_SU = getenv('IS_SU') or 'user'
    SECRET_KEY = getenv('SECRET_KEY', 'supersecretkey')
    JWT_SECRET_KEY = getenv('JWT_SECRET_KEY', 'supersecretjwtkey')

    UPLOAD_FOLDER = getenv('UPLOAD_PATH') or 'static/uploads/images'

    IMG_URL_PREFIX = '/SE/img/'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
