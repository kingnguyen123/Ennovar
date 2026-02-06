import os
import sys
import subprocess
import atexit
from flask import Flask
from flask_cors import CORS
from backend.routes.products import products_bp
from backend.routes.sales import sales_bp
from backend.routes.forecast import forecast_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(products_bp)
app.register_blueprint(sales_bp)
app.register_blueprint(forecast_bp)

# Global variable to track frontend process
frontend_process = None

def start_frontend():
    """Start the frontend development server"""
    global frontend_process
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    
    if not os.path.exists(frontend_dir):
        print("Frontend directory not found")
        return
    
    try:
        print("Starting frontend server...")
        # Start npm run dev in the frontend directory
        frontend_process = subprocess.Popen(
            ['npm', 'run', 'dev'],
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == 'win32' else 0
        )
        print("Frontend server started")
    except Exception as e:
        print(f"Error starting frontend: {e}")

def cleanup():
    """Cleanup function to stop frontend server on exit"""
    global frontend_process
    if frontend_process:
        print("\nStopping frontend server...")
        try:
            if sys.platform == 'win32':
                subprocess.call(['taskkill', '/F', '/T', '/PID', str(frontend_process.pid)], 
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                frontend_process.terminate()
                frontend_process.wait(timeout=5)
        except Exception as e:
            print(f"Error stopping frontend: {e}")

# Register cleanup function
atexit.register(cleanup)

if __name__ == '__main__':
    # Only start frontend in main process (not reloader)
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        start_frontend()
    
    # Start backend server
    print("Starting backend server...")
    try:
        app.run(debug=True, port=5000, use_reloader=True)
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        cleanup()
        sys.exit(0)