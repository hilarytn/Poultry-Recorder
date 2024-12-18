from flask import Flask
from extensions import db, jwt, migrate, mail, init_redis, init_cloudinary
from routes.auth import auth_bp
from routes.feed import feeds_bp
from routes.batch import batches_bp
from routes.vaccination import vaccination_bp
from routes.expense import expenses_bp
from routes.customer import customers_bp
from routes.sale import sales_bp
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    init_redis(app)

    with app.app_context():
        init_cloudinary()  

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(feeds_bp, url_prefix='/poultry')
    app.register_blueprint(batches_bp, url_prefix='/batch')
    app.register_blueprint(vaccination_bp, url_prefix='/vaccination')
    app.register_blueprint(expenses_bp, url_prefix='/expense')
    app.register_blueprint(customers_bp, url_prefix='/customer')
    app.register_blueprint(sales_bp, url_prefix='/sale')
    # app.register_blueprint(profile_bp, url_prefix='/profile')
    # app.register_blueprint(content_bp, url_prefix='/content')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)