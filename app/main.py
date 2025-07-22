from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import math
import os

from . import crud, models, schemas
from .database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Run deployment setup if on Render
if os.getenv('RENDER') == 'true':
    import subprocess
    try:
        subprocess.run(["python3", "deploy_to_render.py"], check=True)
    except Exception as e:
        print(f"Warning: Deployment setup failed: {e}")

app = FastAPI(
    title="Bell Canada B2B API",
    description="API for managing Bell Canada business customers and services",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
def read_root():
    """Root endpoint with API information"""
    return {
        "message": "Bell Canada B2B API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "businesses": "/api/v1/businesses",
            "services": "/api/v1/services",
            "analytics": "/api/v1/analytics"
        }
    }

@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Bell Canada B2B API"}

# Business endpoints
@app.get("/api/v1/businesses", response_model=schemas.BusinessList, tags=["Businesses"])
def read_businesses(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    search: Optional[str] = Query(None, description="Search in company name, email, or phone"),
    industry: Optional[str] = Query(None, description="Filter by industry"),
    province: Optional[str] = Query(None, description="Filter by province"),
    city: Optional[str] = Query(None, description="Filter by city"),
    account_status: Optional[str] = Query(None, description="Filter by account status"),
    db: Session = Depends(get_db)
):
    """Get list of businesses with optional filtering and pagination"""
    businesses = crud.get_businesses(
        db, skip=skip, limit=limit, search=search, 
        industry=industry, province=province, city=city, account_status=account_status
    )
    total = crud.get_businesses_count(
        db, search=search, industry=industry, 
        province=province, city=city, account_status=account_status
    )
    
    pages = math.ceil(total / limit) if limit > 0 else 0
    
    return schemas.BusinessList(
        businesses=businesses,
        total=total,
        page=(skip // limit) + 1 if limit > 0 else 1,
        size=limit,
        pages=pages
    )

@app.get("/api/v1/businesses/{business_id}", response_model=schemas.Business, tags=["Businesses"])
def read_business(business_id: str, db: Session = Depends(get_db)):
    """Get a specific business by ID"""
    business = crud.get_business(db, business_id=business_id)
    if business is None:
        raise HTTPException(status_code=404, detail="Business not found")
    return business

@app.post("/api/v1/businesses", response_model=schemas.Business, status_code=status.HTTP_201_CREATED, tags=["Businesses"])
def create_business(business: schemas.BusinessCreate, db: Session = Depends(get_db)):
    """Create a new business"""
    # Check if business with same ID already exists
    if hasattr(business, 'id') and business.id:
        existing_business = crud.get_business(db, business_id=business.id)
        if existing_business:
            raise HTTPException(status_code=400, detail="Business with this ID already exists")
    
    return crud.create_business(db=db, business=business)

@app.put("/api/v1/businesses/{business_id}", response_model=schemas.Business, tags=["Businesses"])
def update_business(business_id: str, business_update: schemas.BusinessUpdate, db: Session = Depends(get_db)):
    """Update a business"""
    business = crud.update_business(db=db, business_id=business_id, business_update=business_update)
    if business is None:
        raise HTTPException(status_code=404, detail="Business not found")
    return business

@app.delete("/api/v1/businesses/{business_id}", tags=["Businesses"])
def delete_business(business_id: str, db: Session = Depends(get_db)):
    """Delete a business"""
    success = crud.delete_business(db=db, business_id=business_id)
    if not success:
        raise HTTPException(status_code=404, detail="Business not found")
    return {"message": "Business deleted successfully"}

# Service endpoints
@app.get("/api/v1/services", response_model=schemas.ServiceList, tags=["Services"])
def read_services(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    service_type: Optional[str] = Query(None, description="Filter by service type"),
    status: Optional[str] = Query(None, description="Filter by service status"),
    business_id: Optional[str] = Query(None, description="Filter by business ID"),
    db: Session = Depends(get_db)
):
    """Get list of services with optional filtering and pagination"""
    services = crud.get_services(
        db, skip=skip, limit=limit, service_type=service_type, 
        status=status, business_id=business_id
    )
    
    # Count total services with same filters
    total = len(crud.get_services(db, service_type=service_type, status=status, business_id=business_id))
    pages = math.ceil(total / limit) if limit > 0 else 0
    
    return schemas.ServiceList(
        services=services,
        total=total,
        page=(skip // limit) + 1 if limit > 0 else 1,
        size=limit,
        pages=pages
    )

@app.get("/api/v1/services/{service_id}", response_model=schemas.Service, tags=["Services"])
def read_service(service_id: int, db: Session = Depends(get_db)):
    """Get a specific service by ID"""
    service = crud.get_service(db, service_id=service_id)
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

@app.get("/api/v1/businesses/{business_id}/services", response_model=List[schemas.Service], tags=["Services"])
def read_business_services(business_id: str, db: Session = Depends(get_db)):
    """Get all services for a specific business"""
    # Check if business exists
    business = crud.get_business(db, business_id=business_id)
    if business is None:
        raise HTTPException(status_code=404, detail="Business not found")
    
    return crud.get_services_by_business(db, business_id=business_id)

@app.post("/api/v1/businesses/{business_id}/services", response_model=schemas.Service, status_code=status.HTTP_201_CREATED, tags=["Services"])
def create_service(business_id: str, service: schemas.ServiceCreate, db: Session = Depends(get_db)):
    """Create a new service for a business"""
    # Check if business exists
    business = crud.get_business(db, business_id=business_id)
    if business is None:
        raise HTTPException(status_code=404, detail="Business not found")
    
    return crud.create_service(db=db, service=service, business_id=business_id)

@app.put("/api/v1/services/{service_id}", response_model=schemas.Service, tags=["Services"])
def update_service(service_id: int, service_update: dict, db: Session = Depends(get_db)):
    """Update a service"""
    service = crud.update_service(db=db, service_id=service_id, service_update=service_update)
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

@app.delete("/api/v1/services/{service_id}", tags=["Services"])
def delete_service(service_id: int, db: Session = Depends(get_db)):
    """Delete a service"""
    success = crud.delete_service(db=db, service_id=service_id)
    if not success:
        raise HTTPException(status_code=404, detail="Service not found")
    return {"message": "Service deleted successfully"}

# Analytics endpoints
@app.get("/api/v1/analytics/revenue", response_model=schemas.RevenueAnalytics, tags=["Analytics"])
def get_revenue_analytics(db: Session = Depends(get_db)):
    """Get revenue analytics"""
    return crud.get_revenue_analytics(db)

@app.get("/api/v1/analytics/customers", response_model=schemas.CustomerAnalytics, tags=["Analytics"])
def get_customer_analytics(db: Session = Depends(get_db)):
    """Get customer analytics"""
    return crud.get_customer_analytics(db)

@app.get("/api/v1/analytics/summary", tags=["Analytics"])
def get_analytics_summary(db: Session = Depends(get_db)):
    """Get a summary of all analytics"""
    revenue_analytics = crud.get_revenue_analytics(db)
    customer_analytics = crud.get_customer_analytics(db)
    
    return {
        "revenue": revenue_analytics,
        "customers": customer_analytics,
        "summary": {
            "total_customers": customer_analytics["total_customers"],
            "total_monthly_revenue": revenue_analytics["total_monthly_revenue"],
            "average_revenue_per_customer": revenue_analytics["total_monthly_revenue"] / customer_analytics["total_customers"] if customer_analytics["total_customers"] > 0 else 0
        }
    }

# Utility endpoints
@app.get("/api/v1/industries", tags=["Utilities"])
def get_industries(db: Session = Depends(get_db)):
    """Get list of all industries"""
    industries = db.query(models.Business.industry).distinct().all()
    return [industry[0] for industry in industries]

@app.get("/api/v1/provinces", tags=["Utilities"])
def get_provinces(db: Session = Depends(get_db)):
    """Get list of all provinces"""
    provinces = db.query(models.Business.province).distinct().all()
    return [province[0] for province in provinces]

@app.get("/api/v1/cities", tags=["Utilities"])
def get_cities(province: Optional[str] = Query(None, description="Filter by province"), db: Session = Depends(get_db)):
    """Get list of all cities, optionally filtered by province"""
    query = db.query(models.Business.city).distinct()
    if province:
        query = query.filter(models.Business.province == province)
    cities = query.all()
    return [city[0] for city in cities]

@app.get("/api/v1/service-types", tags=["Utilities"])
def get_service_types(db: Session = Depends(get_db)):
    """Get list of all service types"""
    service_types = db.query(models.Service.service_type).distinct().all()
    return [service_type[0] for service_type in service_types]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 