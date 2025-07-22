from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime

# Service schemas
class ServiceBase(BaseModel):
    service_type: str
    service_name: str
    monthly_price: float
    details: Dict[str, Any]
    contract_start: datetime
    contract_end: datetime
    status: str

class ServiceCreate(ServiceBase):
    pass

class Service(ServiceBase):
    id: int
    business_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Business schemas
class BusinessBase(BaseModel):
    company_name: str
    industry: str
    employee_count: int
    annual_revenue: float
    street_number: int
    street_name: str
    city: str
    province: str
    postal_code: str
    country: str
    phone: str
    email: str
    website: str
    bell_customer_since: datetime
    account_manager: str
    payment_method: str
    account_status: str
    last_contact_date: datetime
    notes: str

class BusinessCreate(BusinessBase):
    services: List[ServiceCreate] = []

class BusinessUpdate(BaseModel):
    company_name: Optional[str] = None
    industry: Optional[str] = None
    employee_count: Optional[int] = None
    annual_revenue: Optional[float] = None
    street_number: Optional[int] = None
    street_name: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    bell_customer_since: Optional[datetime] = None
    account_manager: Optional[str] = None
    payment_method: Optional[str] = None
    account_status: Optional[str] = None
    last_contact_date: Optional[datetime] = None
    notes: Optional[str] = None

class Business(BusinessBase):
    id: str
    total_monthly_revenue: float
    created_at: datetime
    updated_at: Optional[datetime] = None
    services: List[Service] = []
    
    class Config:
        from_attributes = True

# Response schemas
class BusinessList(BaseModel):
    businesses: List[Business]
    total: int
    page: int
    size: int
    pages: int

class ServiceList(BaseModel):
    services: List[Service]
    total: int
    page: int
    size: int
    pages: int

# Analytics schemas
class RevenueAnalytics(BaseModel):
    total_monthly_revenue: float
    average_monthly_revenue: float
    revenue_by_industry: Dict[str, float]
    revenue_by_province: Dict[str, float]
    revenue_by_service_type: Dict[str, float]

class CustomerAnalytics(BaseModel):
    total_customers: int
    customers_by_industry: Dict[str, int]
    customers_by_province: Dict[str, int]
    customers_by_status: Dict[str, int]
    average_services_per_customer: float 