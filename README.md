# Bell Canada B2B API

A comprehensive API for managing Bell Canada business customers and services. This project provides a realistic dataset and API endpoints for practicing Salesforce integration and other business applications.

## Features

- **Business Management**: CRUD operations for business customers
- **Service Management**: Manage Bell services (Internet, Phone, Mobile, TV, Cloud, Security)
- **Analytics**: Revenue and customer analytics
- **Realistic Data**: 1000+ generated Canadian businesses with realistic data
- **RESTful API**: Full REST API with filtering, pagination, and search
- **Documentation**: Auto-generated API documentation with Swagger UI

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate Sample Data

```bash
python generate_bell_data.py
```

This will create:
- `bell_canada_businesses.json` (1.8MB)
- `bell_canada_businesses.csv` (387KB)

### 3. Load Data into Database

```bash
python load_data.py
```

This will:
- Create SQLite database
- Load 1000 businesses with their services
- Display summary statistics

### 4. Start the API Server

```bash
python run.py
```

The API will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## API Endpoints

### Business Endpoints

- `GET /api/v1/businesses` - List businesses with filtering and pagination
- `GET /api/v1/businesses/{id}` - Get specific business
- `POST /api/v1/businesses` - Create new business
- `PUT /api/v1/businesses/{id}` - Update business
- `DELETE /api/v1/businesses/{id}` - Delete business

### Service Endpoints

- `GET /api/v1/services` - List services with filtering
- `GET /api/v1/services/{id}` - Get specific service
- `GET /api/v1/businesses/{id}/services` - Get services for a business
- `POST /api/v1/businesses/{id}/services` - Add service to business
- `PUT /api/v1/services/{id}` - Update service
- `DELETE /api/v1/services/{id}` - Delete service

### Analytics Endpoints

- `GET /api/v1/analytics/revenue` - Revenue analytics
- `GET /api/v1/analytics/customers` - Customer analytics
- `GET /api/v1/analytics/summary` - Combined analytics summary

### Utility Endpoints

- `GET /api/v1/industries` - List all industries
- `GET /api/v1/provinces` - List all provinces
- `GET /api/v1/cities` - List cities (optionally filtered by province)
- `GET /api/v1/service-types` - List all service types

## Query Parameters

### Business Filtering

- `search` - Search in company name, email, or phone
- `industry` - Filter by industry
- `province` - Filter by province
- `city` - Filter by city
- `account_status` - Filter by account status
- `skip` - Number of records to skip (pagination)
- `limit` - Number of records to return (pagination)

### Service Filtering

- `service_type` - Filter by service type
- `status` - Filter by service status
- `business_id` - Filter by business ID

## Example API Calls

### Get all businesses in Toronto
```bash
curl "http://localhost:8000/api/v1/businesses?city=Toronto&limit=10"
```

### Search for technology companies
```bash
curl "http://localhost:8000/api/v1/businesses?industry=Technology&search=tech"
```

### Get revenue analytics
```bash
curl "http://localhost:8000/api/v1/analytics/revenue"
```

### Get services for a specific business
```bash
curl "http://localhost:8000/api/v1/businesses/BELL-000001/services"
```

## Data Structure

### Business Object
```json
{
  "id": "BELL-000001",
  "company_name": "Advanced Solutions Inc.",
  "industry": "Technology",
  "employee_count": 50,
  "annual_revenue": 5000000,
  "street_number": 1234,
  "street_name": "Main Street",
  "city": "Toronto",
  "province": "ON",
  "postal_code": "M5V 3A8",
  "country": "Canada",
  "phone": "+1-416-555-0123",
  "email": "info@advancedsolutions.ca",
  "website": "www.advancedsolutions.ca",
  "bell_customer_since": "2020-01-15T00:00:00",
  "account_manager": "Manager 1",
  "total_monthly_revenue": 299.97,
  "payment_method": "Credit Card",
  "account_status": "Active",
  "last_contact_date": "2024-01-15T00:00:00",
  "notes": "Excellent customer, always pays on time",
  "services": [...]
}
```

### Service Object
```json
{
  "id": 1,
  "business_id": "BELL-000001",
  "service_type": "Internet",
  "service_name": "Fiber 500",
  "monthly_price": 119.99,
  "details": {
    "price": 119.99,
    "speed": "500 Mbps"
  },
  "contract_start": "2023-01-15T00:00:00",
  "contract_end": "2025-01-15T00:00:00",
  "status": "Active"
}
```

## Salesforce Integration Examples

### 1. Create Lead from API Data
```javascript
// Salesforce Apex
public class BellAPIIntegration {
    public static void createLeadFromBellAPI(String businessId) {
        // Call Bell API
        String apiUrl = 'http://your-api-url/api/v1/businesses/' + businessId;
        HttpRequest req = new HttpRequest();
        req.setEndpoint(apiUrl);
        req.setMethod('GET');
        
        Http http = new Http();
        HttpResponse res = http.send(req);
        
        if (res.getStatusCode() == 200) {
            Map<String, Object> businessData = (Map<String, Object>) JSON.deserializeUntyped(res.getBody());
            
            // Create Lead
            Lead newLead = new Lead();
            newLead.Company = (String) businessData.get('company_name');
            newLead.Industry = (String) businessData.get('industry');
            newLead.Phone = (String) businessData.get('phone');
            newLead.Email = (String) businessData.get('email');
            newLead.Street = businessData.get('street_number') + ' ' + businessData.get('street_name');
            newLead.City = (String) businessData.get('city');
            newLead.State = (String) businessData.get('province');
            newLead.PostalCode = (String) businessData.get('postal_code');
            newLead.Country = (String) businessData.get('country');
            
            insert newLead;
        }
    }
}
```

### 2. Sync Account Data
```javascript
// Salesforce Apex
public static void syncAccountData(String businessId) {
    // Get business data from Bell API
    String apiUrl = 'http://your-api-url/api/v1/businesses/' + businessId;
    // ... HTTP call logic ...
    
    // Update Account
    Account acc = [SELECT Id FROM Account WHERE Bell_Customer_ID__c = :businessId LIMIT 1];
    acc.Industry = (String) businessData.get('industry');
    acc.NumberOfEmployees = (Integer) businessData.get('employee_count');
    acc.AnnualRevenue = (Decimal) businessData.get('annual_revenue');
    acc.Bell_Monthly_Revenue__c = (Decimal) businessData.get('total_monthly_revenue');
    acc.Bell_Account_Status__c = (String) businessData.get('account_status');
    
    update acc;
}
```

## Deployment Options

### Local Development
- SQLite database (default)
- No additional setup required

### Production Deployment

#### Option 1: Heroku
1. Create `Procfile`:
```
web: uvicorn app.main:app --host=0.0.0.0 --port=$PORT
```

2. Set environment variables:
```bash
heroku config:set DATABASE_URL=postgresql://...
```

#### Option 2: Docker
1. Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Option 3: AWS/GCP/Azure
- Use managed PostgreSQL database
- Deploy to container services or VMs
- Set up proper CORS and security headers

## Environment Variables

Copy `env.example` to `.env` and configure:

```bash
# Database
DATABASE_URL=sqlite:///./bell_canada.db

# Server
PORT=8000
HOST=0.0.0.0

# Security
SECRET_KEY=your-secret-key
ALLOWED_ORIGINS=["http://localhost:3000"]
```

## Development

### Project Structure
```
bell-canada-api/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── database.py      # Database configuration
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   └── crud.py          # CRUD operations
├── generate_bell_data.py # Data generator
├── load_data.py         # Database loader
├── run.py              # Server runner
├── requirements.txt    # Dependencies
└── README.md          # This file
```

### Adding New Features
1. Update models in `app/models.py`
2. Add schemas in `app/schemas.py`
3. Implement CRUD operations in `app/crud.py`
4. Add endpoints in `app/main.py`
5. Update documentation

## Troubleshooting

### Common Issues

1. **Database not found**: Run `python load_data.py` first
2. **Port already in use**: Change PORT in `.env` file
3. **Import errors**: Ensure you're in the correct directory
4. **CORS issues**: Update `ALLOWED_ORIGINS` in `.env`

### Logs
Check the console output for detailed error messages. The API includes comprehensive error handling and validation.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for educational and practice purposes. The Bell Canada branding and data structure are fictional and created for learning purposes only. 