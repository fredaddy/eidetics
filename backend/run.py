from app import create_app, db
import logging

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)
