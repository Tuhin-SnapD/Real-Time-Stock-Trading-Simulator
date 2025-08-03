from flask import Flask, render_template
from src.api.routes import api_bp
import os

def create_app():
    """Application factory pattern for creating Flask app."""
    app = Flask(__name__, 
                template_folder='static/templates',
                static_folder='static')
    
    # Register blueprints
    app.register_blueprint(api_bp)
    
    # Configure app
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    @app.route('/')
    def index():
        """Main dashboard route."""
        return render_template('index.html')
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        return render_template('500.html'), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    print("🚀 Starting Real-Time Stock Trading Simulator...")
    print(f"📊 Dashboard available at: http://localhost:{port}")
    print(f"🔧 Debug mode: {debug}")
    
    app.run(host='0.0.0.0', port=port, debug=debug) 