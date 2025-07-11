from decouple import config

class Config:
    SECRET_KEY = config('SECRET_KEY', default='secret')
    JWT_SECRET_KEY = config('JWT_SECRET_KEY', default='jwt-secret')

    APPLICATION_ROOT = '/'
    PREFERRED_URL_SCHEME = 'http'