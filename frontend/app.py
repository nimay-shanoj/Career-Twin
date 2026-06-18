from flask import Flask, render_template
from flask_login import login_required
from config import Config
from extensions import db, login_manager
from models import User
from auth import auth_bp
from profile_routes import profile_bp
from quiz_routes import quiz_bp
from progress_routes import progress_bp
from resume_routes import resume_bp
from overview_routes import overview_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize Extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Redirect target for @login_required
    
    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(progress_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(overview_bp)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Base Routes to render existing frontend pages
    @app.route('/')
    @app.route('/landing.html')
    def index():
        return render_template('landing.html')
        
    @app.route('/dashboard')
    @app.route('/dashboard.html')
    @login_required
    def dashboard_page():
        return render_template('dashboard.html')
        

    @app.route('/resume')
    @app.route('/resume.html')
    @login_required
    def resume_page():
        return render_template('resume.html')
        
    @app.route('/roadmap')
    @app.route('/roadmap.html')
    @login_required
    def roadmap_page():
        return render_template('roadmap.html')
        
    @app.route('/skillgap')
    @app.route('/skillgap.html')
    @login_required
    def skillgap_page():
        return render_template('skillgap.html')
        
    @app.route('/projects')
    @app.route('/projects.html')
    @login_required
    def projects_page():
        return render_template('projects.html')
        
    @app.route('/quiz')
    @app.route('/quiz.html')
    @login_required
    def quiz_page():
        return render_template('quiz.html')
        
    @app.route('/progress')
    @app.route('/progress.html')
    @login_required
    def progress_page():
        return render_template('progress.html')
        
    @app.route('/overview')
    @app.route('/overview.html')
    @login_required
    def overview_page():
        return render_template('overview.html')
        
    # Database Initialization Hook
    with app.app_context():
        try:
            db.create_all()
            print("Database tables verified/created successfully.")
        except Exception as e:
            print(f"Error during database initialization: {e}")
            print("Make sure your MySQL server is running and the database specified in Config exists.")

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
