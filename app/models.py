from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Business(Base):
    __tablename__ = "businesses"
    
    id = Column(String, primary_key=True, index=True)
    company_name = Column(String, index=True)
    industry = Column(String, index=True)
    employee_count = Column(Integer)
    annual_revenue = Column(Float)
    
    # Address fields
    street_number = Column(Integer)
    street_name = Column(String)
    city = Column(String, index=True)
    province = Column(String, index=True)
    postal_code = Column(String)
    country = Column(String)
    
    # Contact fields
    phone = Column(String)
    email = Column(String, index=True)
    website = Column(String)
    
    # Bell-specific fields
    bell_customer_since = Column(DateTime)
    account_manager = Column(String)
    total_monthly_revenue = Column(Float)
    payment_method = Column(String)
    account_status = Column(String, index=True)
    last_contact_date = Column(DateTime)
    notes = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship to services
    services = relationship("Service", back_populates="business", cascade="all, delete-orphan")

class Service(Base):
    __tablename__ = "services"
    
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(String, ForeignKey("businesses.id"))
    service_type = Column(String, index=True)
    service_name = Column(String)
    monthly_price = Column(Float)
    details = Column(JSON)  # Store service details as JSON
    contract_start = Column(DateTime)
    contract_end = Column(DateTime)
    status = Column(String, index=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship to business
    business = relationship("Business", back_populates="services") 