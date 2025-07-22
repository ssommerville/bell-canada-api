from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List, Optional, Dict, Any
from . import models, schemas
from datetime import datetime

# Business CRUD operations
def get_business(db: Session, business_id: str) -> Optional[models.Business]:
    return db.query(models.Business).filter(models.Business.id == business_id).first()

def get_businesses(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    search: Optional[str] = None,
    industry: Optional[str] = None,
    province: Optional[str] = None,
    city: Optional[str] = None,
    account_status: Optional[str] = None
) -> List[models.Business]:
    query = db.query(models.Business)
    
    # Apply filters
    if search:
        search_filter = or_(
            models.Business.company_name.ilike(f"%{search}%"),
            models.Business.email.ilike(f"%{search}%"),
            models.Business.phone.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    if industry:
        query = query.filter(models.Business.industry == industry)
    
    if province:
        query = query.filter(models.Business.province == province)
    
    if city:
        query = query.filter(models.Business.city == city)
    
    if account_status:
        query = query.filter(models.Business.account_status == account_status)
    
    return query.offset(skip).limit(limit).all()

def get_businesses_count(
    db: Session,
    search: Optional[str] = None,
    industry: Optional[str] = None,
    province: Optional[str] = None,
    city: Optional[str] = None,
    account_status: Optional[str] = None
) -> int:
    query = db.query(models.Business)
    
    # Apply same filters as get_businesses
    if search:
        search_filter = or_(
            models.Business.company_name.ilike(f"%{search}%"),
            models.Business.email.ilike(f"%{search}%"),
            models.Business.phone.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    if industry:
        query = query.filter(models.Business.industry == industry)
    
    if province:
        query = query.filter(models.Business.province == province)
    
    if city:
        query = query.filter(models.Business.city == city)
    
    if account_status:
        query = query.filter(models.Business.account_status == account_status)
    
    return query.count()

def create_business(db: Session, business: schemas.BusinessCreate) -> models.Business:
    # Calculate total monthly revenue from services
    total_monthly_revenue = sum(service.monthly_price for service in business.services)
    
    # Create business object
    db_business = models.Business(
        id=business.id if hasattr(business, 'id') else None,
        company_name=business.company_name,
        industry=business.industry,
        employee_count=business.employee_count,
        annual_revenue=business.annual_revenue,
        street_number=business.street_number,
        street_name=business.street_name,
        city=business.city,
        province=business.province,
        postal_code=business.postal_code,
        country=business.country,
        phone=business.phone,
        email=business.email,
        website=business.website,
        bell_customer_since=business.bell_customer_since,
        account_manager=business.account_manager,
        total_monthly_revenue=total_monthly_revenue,
        payment_method=business.payment_method,
        account_status=business.account_status,
        last_contact_date=business.last_contact_date,
        notes=business.notes
    )
    
    db.add(db_business)
    db.commit()
    db.refresh(db_business)
    
    # Create services
    for service in business.services:
        db_service = models.Service(
            business_id=db_business.id,
            service_type=service.service_type,
            service_name=service.service_name,
            monthly_price=service.monthly_price,
            details=service.details,
            contract_start=service.contract_start,
            contract_end=service.contract_end,
            status=service.status
        )
        db.add(db_service)
    
    db.commit()
    db.refresh(db_business)
    return db_business

def update_business(db: Session, business_id: str, business_update: schemas.BusinessUpdate) -> Optional[models.Business]:
    db_business = get_business(db, business_id)
    if not db_business:
        return None
    
    # Update only provided fields
    update_data = business_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_business, field, value)
    
    db.commit()
    db.refresh(db_business)
    return db_business

def delete_business(db: Session, business_id: str) -> bool:
    db_business = get_business(db, business_id)
    if not db_business:
        return False
    
    db.delete(db_business)
    db.commit()
    return True

# Service CRUD operations
def get_service(db: Session, service_id: int) -> Optional[models.Service]:
    return db.query(models.Service).filter(models.Service.id == service_id).first()

def get_services_by_business(db: Session, business_id: str) -> List[models.Service]:
    return db.query(models.Service).filter(models.Service.business_id == business_id).all()

def get_services(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    service_type: Optional[str] = None,
    status: Optional[str] = None,
    business_id: Optional[str] = None
) -> List[models.Service]:
    query = db.query(models.Service)
    
    if service_type:
        query = query.filter(models.Service.service_type == service_type)
    
    if status:
        query = query.filter(models.Service.status == status)
    
    if business_id:
        query = query.filter(models.Service.business_id == business_id)
    
    return query.offset(skip).limit(limit).all()

def create_service(db: Session, service: schemas.ServiceCreate, business_id: str) -> models.Service:
    db_service = models.Service(
        business_id=business_id,
        service_type=service.service_type,
        service_name=service.service_name,
        monthly_price=service.monthly_price,
        details=service.details,
        contract_start=service.contract_start,
        contract_end=service.contract_end,
        status=service.status
    )
    
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    
    # Update business total monthly revenue
    update_business_revenue(db, business_id)
    
    return db_service

def update_service(db: Session, service_id: int, service_update: dict) -> Optional[models.Service]:
    db_service = get_service(db, service_id)
    if not db_service:
        return None
    
    for field, value in service_update.items():
        setattr(db_service, field, value)
    
    db.commit()
    db.refresh(db_service)
    
    # Update business total monthly revenue
    update_business_revenue(db, db_service.business_id)
    
    return db_service

def delete_service(db: Session, service_id: int) -> bool:
    db_service = get_service(db, service_id)
    if not db_service:
        return False
    
    business_id = db_service.business_id
    db.delete(db_service)
    db.commit()
    
    # Update business total monthly revenue
    update_business_revenue(db, business_id)
    
    return True

def update_business_revenue(db: Session, business_id: str):
    """Update the total monthly revenue for a business based on its services"""
    total_revenue = db.query(func.sum(models.Service.monthly_price)).filter(
        models.Service.business_id == business_id
    ).scalar() or 0.0
    
    db_business = get_business(db, business_id)
    if db_business:
        db_business.total_monthly_revenue = total_revenue
        db.commit()

# Analytics functions
def get_revenue_analytics(db: Session) -> Dict[str, Any]:
    # Total and average monthly revenue
    total_revenue = db.query(func.sum(models.Business.total_monthly_revenue)).scalar() or 0.0
    avg_revenue = db.query(func.avg(models.Business.total_monthly_revenue)).scalar() or 0.0
    
    # Revenue by industry
    revenue_by_industry = db.query(
        models.Business.industry,
        func.sum(models.Business.total_monthly_revenue)
    ).group_by(models.Business.industry).all()
    
    # Revenue by province
    revenue_by_province = db.query(
        models.Business.province,
        func.sum(models.Business.total_monthly_revenue)
    ).group_by(models.Business.province).all()
    
    # Revenue by service type
    revenue_by_service_type = db.query(
        models.Service.service_type,
        func.sum(models.Service.monthly_price)
    ).group_by(models.Service.service_type).all()
    
    return {
        "total_monthly_revenue": total_revenue,
        "average_monthly_revenue": avg_revenue,
        "revenue_by_industry": dict(revenue_by_industry),
        "revenue_by_province": dict(revenue_by_province),
        "revenue_by_service_type": dict(revenue_by_service_type)
    }

def get_customer_analytics(db: Session) -> Dict[str, Any]:
    # Total customers
    total_customers = db.query(models.Business).count()
    
    # Customers by industry
    customers_by_industry = db.query(
        models.Business.industry,
        func.count(models.Business.id)
    ).group_by(models.Business.industry).all()
    
    # Customers by province
    customers_by_province = db.query(
        models.Business.province,
        func.count(models.Business.id)
    ).group_by(models.Business.province).all()
    
    # Customers by status
    customers_by_status = db.query(
        models.Business.account_status,
        func.count(models.Business.id)
    ).group_by(models.Business.account_status).all()
    
    # Average services per customer
    total_services = db.query(models.Service).count()
    avg_services = total_services / total_customers if total_customers > 0 else 0
    
    return {
        "total_customers": total_customers,
        "customers_by_industry": dict(customers_by_industry),
        "customers_by_province": dict(customers_by_province),
        "customers_by_status": dict(customers_by_status),
        "average_services_per_customer": avg_services
    } 