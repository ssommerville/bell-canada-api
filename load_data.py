#!/usr/bin/env python3
"""
Data loader for Bell Canada B2B API
Loads generated JSON data into the database
"""

import json
import sys
import os
from datetime import datetime
from sqlalchemy.orm import Session

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.database import SessionLocal, engine
from app.models import Base, Business, Service

def parse_date(date_string):
    """Parse date string to datetime object"""
    try:
        return datetime.strptime(date_string, "%Y-%m-%d")
    except ValueError:
        return datetime.now()

def load_data_from_json(json_file_path: str):
    """Load data from JSON file into database"""
    print(f"Loading data from {json_file_path}...")
    
    # Read JSON file
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Clear existing data
        print("Clearing existing data...")
        db.query(Service).delete()
        db.query(Business).delete()
        db.commit()
        
        # Load businesses
        print(f"Loading {len(data)} businesses...")
        for i, business_data in enumerate(data):
            if i % 100 == 0:
                print(f"Processed {i} businesses...")
            
            # Create business object
            business = Business(
                id=business_data["id"],
                company_name=business_data["company_name"],
                industry=business_data["industry"],
                employee_count=business_data["employee_count"],
                annual_revenue=business_data["annual_revenue"],
                street_number=business_data["address"]["street_number"],
                street_name=business_data["address"]["street_name"],
                city=business_data["address"]["city"],
                province=business_data["address"]["province"],
                postal_code=business_data["address"]["postal_code"],
                country=business_data["address"]["country"],
                phone=business_data["phone"],
                email=business_data["email"],
                website=business_data["website"],
                bell_customer_since=parse_date(business_data["bell_customer_since"]),
                account_manager=business_data["account_manager"],
                total_monthly_revenue=business_data["total_monthly_revenue"],
                payment_method=business_data["payment_method"],
                account_status=business_data["account_status"],
                last_contact_date=parse_date(business_data["last_contact_date"]),
                notes=business_data["notes"]
            )
            
            db.add(business)
            db.flush()  # Get the ID without committing
            
            # Create services for this business
            for service_data in business_data["services"]:
                service = Service(
                    business_id=business.id,
                    service_type=service_data["service_type"],
                    service_name=service_data["service_name"],
                    monthly_price=service_data["monthly_price"],
                    details=service_data["details"],
                    contract_start=parse_date(service_data["contract_start"]),
                    contract_end=parse_date(service_data["contract_end"]),
                    status=service_data["status"]
                )
                db.add(service)
            
            # Commit every 50 businesses to avoid memory issues
            if (i + 1) % 50 == 0:
                db.commit()
                print(f"Committed {i + 1} businesses...")
        
        # Final commit
        db.commit()
        print(f"Successfully loaded {len(data)} businesses!")
        
        # Print summary
        business_count = db.query(Business).count()
        service_count = db.query(Service).count()
        total_revenue = db.query(Business.total_monthly_revenue).all()
        total_revenue_sum = sum([r[0] for r in total_revenue])
        
        print(f"\nDatabase Summary:")
        print(f"  Businesses: {business_count}")
        print(f"  Services: {service_count}")
        print(f"  Total Monthly Revenue: ${total_revenue_sum:,.2f}")
        print(f"  Average Revenue per Business: ${total_revenue_sum/business_count:,.2f}")
        
    except Exception as e:
        print(f"Error loading data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def main():
    """Main function"""
    json_file = "bell_canada_businesses.json"
    
    if not os.path.exists(json_file):
        print(f"Error: {json_file} not found!")
        print("Please run generate_bell_data.py first to create the data file.")
        sys.exit(1)
    
    # Create tables
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    # Load data
    load_data_from_json(json_file)
    
    print("\nData loading complete! You can now start the API server.")

if __name__ == "__main__":
    main() 