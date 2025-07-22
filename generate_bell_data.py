#!/usr/bin/env python3
"""
Bell Canada B2B Telecommunications Dataset Generator
Creates realistic data for Canadian businesses using Bell services
"""

import json
import random
from datetime import datetime, timedelta
import csv

# Canadian cities and provinces for realistic addresses
CANADIAN_CITIES = [
    {"city": "Toronto", "province": "ON", "postal_code_prefix": "M"},
    {"city": "Montreal", "province": "QC", "postal_code_prefix": "H"},
    {"city": "Vancouver", "province": "BC", "postal_code_prefix": "V"},
    {"city": "Calgary", "province": "AB", "postal_code_prefix": "T"},
    {"city": "Edmonton", "province": "AB", "postal_code_prefix": "T"},
    {"city": "Ottawa", "province": "ON", "postal_code_prefix": "K"},
    {"city": "Winnipeg", "province": "MB", "postal_code_prefix": "R"},
    {"city": "Quebec City", "province": "QC", "postal_code_prefix": "G"},
    {"city": "Hamilton", "province": "ON", "postal_code_prefix": "L"},
    {"city": "Kitchener", "province": "ON", "postal_code_prefix": "N"},
    {"city": "London", "province": "ON", "postal_code_prefix": "N"},
    {"city": "Victoria", "province": "BC", "postal_code_prefix": "V"},
    {"city": "Halifax", "province": "NS", "postal_code_prefix": "B"},
    {"city": "Saskatoon", "province": "SK", "postal_code_prefix": "S"},
    {"city": "Regina", "province": "SK", "postal_code_prefix": "S"},
    {"city": "St. John's", "province": "NL", "postal_code_prefix": "A"},
    {"city": "Fredericton", "province": "NB", "postal_code_prefix": "E"},
    {"city": "Charlottetown", "province": "PE", "postal_code_prefix": "C"},
    {"city": "Whitehorse", "province": "YT", "postal_code_prefix": "Y"},
    {"city": "Yellowknife", "province": "NT", "postal_code_prefix": "X"},
    {"city": "Iqaluit", "province": "NU", "postal_code_prefix": "X"}
]

# Business types and industries
BUSINESS_TYPES = [
    "Technology", "Healthcare", "Finance", "Manufacturing", "Retail", 
    "Education", "Legal", "Consulting", "Real Estate", "Construction",
    "Transportation", "Hospitality", "Media", "Non-Profit", "Government"
]

# Bell Canada services
BELL_SERVICES = {
    "Internet": {
        "Fiber 100": {"price": 89.99, "speed": "100 Mbps"},
        "Fiber 500": {"price": 119.99, "speed": "500 Mbps"},
        "Fiber 1G": {"price": 149.99, "speed": "1 Gbps"},
        "Fiber 3G": {"price": 199.99, "speed": "3 Gbps"},
        "Business DSL": {"price": 69.99, "speed": "25 Mbps"}
    },
    "Phone": {
        "Basic Business Line": {"price": 29.99, "features": "Local calling"},
        "Business Bundle": {"price": 49.99, "features": "Local + Long distance"},
        "Unlimited Canada": {"price": 79.99, "features": "Unlimited Canada calling"},
        "International Bundle": {"price": 129.99, "features": "Canada + US + International"}
    },
    "Mobile": {
        "Business Basic": {"price": 45.00, "data": "2GB"},
        "Business Plus": {"price": 65.00, "data": "10GB"},
        "Business Unlimited": {"price": 85.00, "data": "Unlimited"},
        "Enterprise Plan": {"price": 120.00, "data": "Unlimited + Hotspot"}
    },
    "TV": {
        "Basic TV": {"price": 39.99, "channels": 50},
        "Popular TV": {"price": 59.99, "channels": 100},
        "Premium TV": {"price": 89.99, "channels": 200},
        "Ultimate TV": {"price": 129.99, "channels": 400}
    },
    "Cloud": {
        "Basic Cloud": {"price": 19.99, "storage": "100GB"},
        "Business Cloud": {"price": 49.99, "storage": "1TB"},
        "Enterprise Cloud": {"price": 99.99, "storage": "5TB"}
    },
    "Security": {
        "Basic Security": {"price": 14.99, "features": "Firewall + Antivirus"},
        "Advanced Security": {"price": 29.99, "features": "Firewall + Antivirus + VPN"},
        "Enterprise Security": {"price": 59.99, "features": "Full security suite"}
    }
}

# Company name components
COMPANY_PREFIXES = [
    "Advanced", "Canadian", "Global", "Premier", "Elite", "Professional",
    "Innovative", "Strategic", "Dynamic", "Excellence", "Quality", "Reliable",
    "Trusted", "Leading", "Modern", "Digital", "Smart", "Future", "Next",
    "Peak", "Summit", "Prime", "Core", "Central", "Metro", "Urban", "Regional"
]

COMPANY_MAIN_NAMES = [
    "Solutions", "Systems", "Technologies", "Services", "Consulting", "Group",
    "Partners", "Associates", "Enterprises", "Corporation", "Industries",
    "Manufacturing", "Trading", "Import", "Export", "Distribution", "Logistics",
    "Healthcare", "Medical", "Dental", "Legal", "Financial", "Insurance",
    "Real Estate", "Construction", "Engineering", "Architecture", "Design",
    "Marketing", "Advertising", "Media", "Communications", "Education",
    "Training", "Development", "Research", "Laboratories", "Pharmaceuticals"
]

COMPANY_SUFFIXES = [
    "Inc.", "Ltd.", "Corp.", "LLC", "Partnership", "Associates", "Group",
    "International", "Canada", "North", "West", "East", "Central"
]

def generate_company_name():
    """Generate a realistic Canadian company name"""
    prefix = random.choice(COMPANY_PREFIXES)
    main = random.choice(COMPANY_MAIN_NAMES)
    suffix = random.choice(COMPANY_SUFFIXES)
    
    # Sometimes skip prefix or suffix for variety
    if random.random() < 0.3:
        return f"{main} {suffix}"
    elif random.random() < 0.2:
        return f"{prefix} {main}"
    else:
        return f"{prefix} {main} {suffix}"

def generate_address():
    """Generate a realistic Canadian address"""
    city_data = random.choice(CANADIAN_CITIES)
    
    # Generate street number
    street_number = random.randint(1, 9999)
    
    # Generate street name
    street_names = [
        "Main", "King", "Queen", "Broadway", "Central", "First", "Second",
        "Oak", "Maple", "Pine", "Cedar", "Elm", "Birch", "Spruce", "Willow",
        "Victoria", "Albert", "George", "Edward", "Charles", "William",
        "John", "Robert", "Michael", "David", "James", "Thomas", "Richard",
        "University", "College", "School", "Church", "Market", "Commerce",
        "Business", "Industrial", "Technology", "Innovation", "Progress"
    ]
    
    street_name = random.choice(street_names)
    street_types = ["Street", "Avenue", "Road", "Boulevard", "Drive", "Way", "Lane"]
    street_type = random.choice(street_types)
    
    # Generate postal code
    postal_code = f"{city_data['postal_code_prefix']}{random.randint(1, 9)}{random.choice('ABCEGHJKLMNPRSTVWXYZ')} {random.randint(1, 9)}{random.choice('ABCEGHJKLMNPRSTVWXYZ')}{random.randint(1, 9)}"
    
    return {
        "street_number": street_number,
        "street_name": f"{street_name} {street_type}",
        "city": city_data["city"],
        "province": city_data["province"],
        "postal_code": postal_code,
        "country": "Canada"
    }

def generate_phone_number():
    """Generate a realistic Canadian phone number"""
    area_codes = ["416", "647", "437", "905", "289", "365", "343", "613", "819", "873", "450", "579", "354", "581", "418", "581", "514", "438", "450", "579", "354", "581", "418", "581", "604", "778", "236", "672", "250", "778", "236", "672", "403", "587", "825", "780", "825", "587", "403", "204", "431", "506", "709", "782", "902", "782", "709", "506", "431", "204", "306", "639", "474", "306", "639", "474", "867", "867"]
    
    area_code = random.choice(area_codes)
    prefix = random.randint(200, 999)
    line_number = random.randint(1000, 9999)
    
    return f"+1-{area_code}-{prefix}-{line_number}"

def generate_bell_services():
    """Generate realistic Bell services for a business"""
    services = []
    
    # Most businesses have internet
    if random.random() < 0.95:
        service_type = "Internet"
        service_name = random.choice(list(BELL_SERVICES[service_type].keys()))
        service_data = BELL_SERVICES[service_type][service_name]
        
        services.append({
            "service_type": service_type,
            "service_name": service_name,
            "monthly_price": service_data["price"],
            "details": service_data,
            "contract_start": (datetime.now() - timedelta(days=random.randint(30, 1095))).strftime("%Y-%m-%d"),
            "contract_end": (datetime.now() + timedelta(days=random.randint(365, 1825))).strftime("%Y-%m-%d"),
            "status": random.choice(["Active", "Active", "Active", "Pending", "Suspended"])
        })
    
    # Many businesses have phone service
    if random.random() < 0.85:
        service_type = "Phone"
        service_name = random.choice(list(BELL_SERVICES[service_type].keys()))
        service_data = BELL_SERVICES[service_type][service_name]
        
        services.append({
            "service_type": service_type,
            "service_name": service_name,
            "monthly_price": service_data["price"],
            "details": service_data,
            "contract_start": (datetime.now() - timedelta(days=random.randint(30, 1095))).strftime("%Y-%m-%d"),
            "contract_end": (datetime.now() + timedelta(days=random.randint(365, 1825))).strftime("%Y-%m-%d"),
            "status": random.choice(["Active", "Active", "Active", "Pending", "Suspended"])
        })
    
    # Some businesses have mobile plans
    if random.random() < 0.60:
        service_type = "Mobile"
        service_name = random.choice(list(BELL_SERVICES[service_type].keys()))
        service_data = BELL_SERVICES[service_type][service_name]
        
        # Generate multiple lines for mobile
        num_lines = random.randint(1, 10)
        
        services.append({
            "service_type": service_type,
            "service_name": service_name,
            "monthly_price": service_data["price"] * num_lines,
            "details": {**service_data, "number_of_lines": num_lines},
            "contract_start": (datetime.now() - timedelta(days=random.randint(30, 1095))).strftime("%Y-%m-%d"),
            "contract_end": (datetime.now() + timedelta(days=random.randint(365, 1825))).strftime("%Y-%m-%d"),
            "status": random.choice(["Active", "Active", "Active", "Pending", "Suspended"])
        })
    
    # Some businesses have TV
    if random.random() < 0.40:
        service_type = "TV"
        service_name = random.choice(list(BELL_SERVICES[service_type].keys()))
        service_data = BELL_SERVICES[service_type][service_name]
        
        services.append({
            "service_type": service_type,
            "service_name": service_name,
            "monthly_price": service_data["price"],
            "details": service_data,
            "contract_start": (datetime.now() - timedelta(days=random.randint(30, 1095))).strftime("%Y-%m-%d"),
            "contract_end": (datetime.now() + timedelta(days=random.randint(365, 1825))).strftime("%Y-%m-%d"),
            "status": random.choice(["Active", "Active", "Active", "Pending", "Suspended"])
        })
    
    # Some businesses have cloud services
    if random.random() < 0.35:
        service_type = "Cloud"
        service_name = random.choice(list(BELL_SERVICES[service_type].keys()))
        service_data = BELL_SERVICES[service_type][service_name]
        
        services.append({
            "service_type": service_type,
            "service_name": service_name,
            "monthly_price": service_data["price"],
            "details": service_data,
            "contract_start": (datetime.now() - timedelta(days=random.randint(30, 1095))).strftime("%Y-%m-%d"),
            "contract_end": (datetime.now() + timedelta(days=random.randint(365, 1825))).strftime("%Y-%m-%d"),
            "status": random.choice(["Active", "Active", "Active", "Pending", "Suspended"])
        })
    
    # Some businesses have security services
    if random.random() < 0.30:
        service_type = "Security"
        service_name = random.choice(list(BELL_SERVICES[service_type].keys()))
        service_data = BELL_SERVICES[service_type][service_name]
        
        services.append({
            "service_type": service_type,
            "service_name": service_name,
            "monthly_price": service_data["price"],
            "details": service_data,
            "contract_start": (datetime.now() - timedelta(days=random.randint(30, 1095))).strftime("%Y-%m-%d"),
            "contract_end": (datetime.now() + timedelta(days=random.randint(365, 1825))).strftime("%Y-%m-%d"),
            "status": random.choice(["Active", "Active", "Active", "Pending", "Suspended"])
        })
    
    return services

def generate_business_data(num_businesses=1000):
    """Generate comprehensive business data"""
    businesses = []
    
    for i in range(num_businesses):
        address = generate_address()
        services = generate_bell_services()
        
        # Calculate total monthly revenue
        total_monthly_revenue = sum(service["monthly_price"] for service in services)
        
        business = {
            "id": f"BELL-{str(i+1).zfill(6)}",
            "company_name": generate_company_name(),
            "industry": random.choice(BUSINESS_TYPES),
            "employee_count": random.choice([1, 2, 3, 5, 10, 15, 25, 50, 100, 250, 500, 1000, 2500, 5000]),
            "annual_revenue": random.choice([50000, 100000, 250000, 500000, 1000000, 2500000, 5000000, 10000000, 25000000, 50000000, 100000000]),
            "address": address,
            "phone": generate_phone_number(),
            "email": f"info@{generate_company_name().lower().replace(' ', '').replace('.', '').replace(',', '')}.ca",
            "website": f"www.{generate_company_name().lower().replace(' ', '').replace('.', '').replace(',', '')}.ca",
            "bell_customer_since": (datetime.now() - timedelta(days=random.randint(365, 3650))).strftime("%Y-%m-%d"),
            "account_manager": f"Manager {random.randint(1, 50)}",
            "services": services,
            "total_monthly_revenue": round(total_monthly_revenue, 2),
            "payment_method": random.choice(["Credit Card", "Bank Transfer", "Invoice", "Auto-Pay"]),
            "account_status": random.choice(["Active", "Active", "Active", "Past Due", "Suspended", "Cancelled"]),
            "last_contact_date": (datetime.now() - timedelta(days=random.randint(1, 90))).strftime("%Y-%m-%d"),
            "notes": random.choice([
                "Excellent customer, always pays on time",
                "Interested in upgrading services",
                "Has been a customer for many years",
                "Recently expanded business",
                "May need additional services",
                "Contacted about new offerings",
                "Satisfied with current services",
                "Potential for upselling",
                "Regular maintenance customer",
                "High-value customer"
            ])
        }
        
        businesses.append(business)
    
    return businesses

def save_to_json(data, filename):
    """Save data to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Data saved to {filename}")

def save_to_csv(data, filename):
    """Save data to CSV file"""
    if not data:
        return
    
    # First pass: determine all possible field names
    all_fieldnames = set()
    flattened_data = []
    
    for business in data:
        base_record = {
            "id": business["id"],
            "company_name": business["company_name"],
            "industry": business["industry"],
            "employee_count": business["employee_count"],
            "annual_revenue": business["annual_revenue"],
            "street_number": business["address"]["street_number"],
            "street_name": business["address"]["street_name"],
            "city": business["address"]["city"],
            "province": business["address"]["province"],
            "postal_code": business["address"]["postal_code"],
            "country": business["address"]["country"],
            "phone": business["phone"],
            "email": business["email"],
            "website": business["website"],
            "bell_customer_since": business["bell_customer_since"],
            "account_manager": business["account_manager"],
            "total_monthly_revenue": business["total_monthly_revenue"],
            "payment_method": business["payment_method"],
            "account_status": business["account_status"],
            "last_contact_date": business["last_contact_date"],
            "notes": business["notes"]
        }
        
        # Add service information
        for i, service in enumerate(business["services"]):
            base_record[f"service_{i+1}_type"] = service["service_type"]
            base_record[f"service_{i+1}_name"] = service["service_name"]
            base_record[f"service_{i+1}_price"] = service["monthly_price"]
            base_record[f"service_{i+1}_status"] = service["status"]
        
        # Add all field names to the set
        all_fieldnames.update(base_record.keys())
        flattened_data.append(base_record)
    
    # Convert set to sorted list for consistent ordering
    fieldnames = sorted(list(all_fieldnames))
    
    # Ensure all records have all fields (fill missing with empty string)
    for record in flattened_data:
        for field in fieldnames:
            if field not in record:
                record[field] = ""
    
    # Write to CSV
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        if flattened_data:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(flattened_data)
    
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    print("Generating Bell Canada B2B dataset...")
    
    # Generate 1000 businesses
    businesses = generate_business_data(1000)
    
    # Save in different formats
    save_to_json(businesses, "bell_canada_businesses.json")
    save_to_csv(businesses, "bell_canada_businesses.csv")
    
    # Print summary
    print(f"\nGenerated {len(businesses)} businesses")
    print(f"Total monthly revenue: ${sum(b['total_monthly_revenue'] for b in businesses):,.2f}")
    
    # Service breakdown
    service_counts = {}
    for business in businesses:
        for service in business["services"]:
            service_type = service["service_type"]
            service_counts[service_type] = service_counts.get(service_type, 0) + 1
    
    print("\nService breakdown:")
    for service_type, count in service_counts.items():
        print(f"  {service_type}: {count} subscriptions")
    
    print("\nDataset ready for API deployment!") 