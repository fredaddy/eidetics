from app import create_app, db
from flask_migrate import Migrate

print("Creating app...")
app = create_app()
print("App created")

print("Initializing Migrate...")
migrate = Migrate(app, db)
print("Migrate initialized")

if __name__ == '__main__':
    print("Running app...")
    app.run()