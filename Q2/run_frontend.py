import subprocess
import sys
import os

def run_frontend():
    """Run the Streamlit frontend"""
    try:
        # Change to the script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        # Run streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", "frontend.py"], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"Error running frontend: {e}")
    except KeyboardInterrupt:
        print("\nFrontend stopped.")

if __name__ == "__main__":
    print("Starting Quick Commerce Price Comparison Frontend...")
    print("Press Ctrl+C to stop")
    run_frontend() 