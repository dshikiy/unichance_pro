from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    applications = relationship("Application", back_populates="user")

class University(Base):
    __tablename__ = "universities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    city = Column(String, nullable=False)
    description = Column(Text)
    website = Column(String)
    
    programs = relationship("Program", back_populates="university")

class Program(Base):
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True, index=True)
    university_id = Column(Integer, ForeignKey("universities.id"))
    name = Column(String, nullable=False)
    degree = Column(String) 
    
    min_ielts = Column(Float, default=6.0)
    min_sat = Column(Integer, nullable=True)
    gpa_min = Column(Float, default=3.0)
    
    deadline = Column(String, nullable=True)
    has_full_grant = Column(Boolean, default=False)
    
    university = relationship("University", back_populates="programs")
    scholarships = relationship("Scholarship", back_populates="program")
    applications = relationship("Application", back_populates="program")

class Scholarship(Base):
    __tablename__ = "scholarships"

    id = Column(Integer, primary_key=True, index=True)
    program_id = Column(Integer, ForeignKey("programs.id"))
    type = Column(String)
    description = Column(Text)
    
    program = relationship("Program", back_populates="scholarships")

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    program_id = Column(Integer, ForeignKey("programs.id"))
    chance_score = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="applications")
    program = relationship("Program", back_populates="applications")