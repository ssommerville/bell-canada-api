#!/usr/bin/env python3
"""
Deployment helper for Render
This script helps set up the database and load data after deployment
"""

import os
import sys
import subprocess
import time
from datetime import datetime

def print_step(step, description):
    """Print a formatted step"""
    print(f"\n{'='*50}")
    print(f"STEP {step}: {description}")
    print(f"{'='*50}")

def check_render_env():
    """Check if we're running on Render"""
    return os.getenv('RENDER') == 'true'

def setup_database():
    """Set up database tables and load data"""
    print_step(1, "Setting up database")
    
    try:
        # Import database modules
        sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))
        from app.database import engine
        from app.models import Base
        
        # Create tables
        print("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created")
        
        # Load data if this is a fresh deployment
        if check_render_env():
            print("Running on Render - checking if data needs to be loaded...")
            from app.database import SessionLocal
            from app.models import Business
            
            db = SessionLocal()
            try:
                business_count = db.query(Business).count()
                if business_count == 0:
                    print("No data found - loading sample data...")
                    load_sample_data()
                else:
                    print(f"✅ Database already has {business_count} businesses")
            finally:
                db.close()
        
        return True
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

def load_sample_data():
    """Load sample data into the database"""
    print_step(2, "Loading sample data")
    
    try:
        # Check if JSON file exists
        json_file = "bell_canada_businesses.json"
        if not os.path.exists(json_file):
            print("Generating sample data...")
            subprocess.run(["python3", "generate_bell_data.py"], check=True)
        
        # Load data
        print("Loading data into database...")
        subprocess.run(["python3", "load_data.py"], check=True)
        print("✅ Sample data loaded successfully")
        return True
    except Exception as e:
        print(f"❌ Data loading failed: {e}")
        return False

def main():
    """Main deployment function"""
    print("🚀 Bell Canada B2B API - Render Deployment Helper")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if check_render_env():
        print("✅ Running on Render platform")
    else:
        print("ℹ️  Running locally (not on Render)")
    
    # Set up database
    if not setup_database():
        print("❌ Deployment failed during database setup")
        sys.exit(1)
    
    print("\n🎉 Deployment setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Your API should be accessible at your Render URL")
    print("2. Visit /docs for API documentation")
    print("3. Test the /health endpoint")
    print("4. Start making API calls for Salesforce integration!")

if __name__ == "__main__":
    main() 