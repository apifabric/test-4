# created from response - used to create database and project
#  should run without error
#  if not, check for decimal, indent, or import issues

import decimal

import logging



logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

import sqlalchemy



from sqlalchemy.sql import func  # end imports from system/genai/create_db_models_inserts/create_db_models_prefix.py

from logic_bank.logic_bank import Rule

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime

# Base class for declarative class definitions
Base = declarative_base()

# Database configuration
engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
Session = sessionmaker(bind=engine)
session = Session()

class Doctor(Base):
    """
    description: Represents a doctor with specialization and contact details.
    """
    __tablename__ = 'doctor'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    specialization = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    
class Patient(Base):
    """
    description: Represents a patient with personal details and contact information.
    """
    __tablename__ = 'patient'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    gender = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    address = Column(String, nullable=True)
    
class Appointment(Base):
    """
    description: Represents an appointment made by a patient with a doctor.
    """
    __tablename__ = 'appointment'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey('patient.id'), nullable=False)
    doctor_id = Column(Integer, ForeignKey('doctor.id'), nullable=False)
    appointment_date = Column(DateTime, nullable=False)
    status = Column(String, nullable=False, default='Scheduled')
    doctor = relationship("Doctor")
    patient = relationship("Patient")

class Prescription(Base):
    """
    description: Contains prescriptions issued to a patient during an appointment.
    """
    __tablename__ = 'prescription'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    appointment_id = Column(Integer, ForeignKey('appointment.id'), nullable=False)
    medication = Column(String, nullable=False)
    dosage = Column(String, nullable=False)
    notes = Column(String, nullable=True)
    appointment = relationship("Appointment")

class MedicalRecord(Base):
    """
    description: Represents the medical records/history of a patient.
    """
    __tablename__ = 'medical_record'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey('patient.id'), nullable=False)
    description = Column(String, nullable=False)
    record_date = Column(DateTime, default=datetime.datetime.utcnow)
    patient = relationship("Patient")

class Room(Base):
    """
    description: Represents a room used for conducting appointments.
    """
    __tablename__ = 'room'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    room_number = Column(String, nullable=False)
    floor = Column(Integer, nullable=True)
    availability = Column(Boolean, nullable=False, default=True)

class Procedure(Base):
    """
    description: Represents a medical procedure that can be performed.
    """
    __tablename__ = 'procedure'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    cost = Column(Float, nullable=False)
    duration = Column(Integer, nullable=False)  # Duration in minutes

class Billing(Base):
    """
    description: Represents the billing information for a patient's appointment.
    """
    __tablename__ = 'billing'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    appointment_id = Column(Integer, ForeignKey('appointment.id'), nullable=False)
    amount_due = Column(Float, nullable=False)
    date_issued = Column(DateTime, default=datetime.datetime.utcnow)
    appointment = relationship("Appointment")

class Insurance(Base):
    """
    description: Contains details about a patient's insurance plan.
    """
    __tablename__ = 'insurance'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey('patient.id'), nullable=False)
    provider = Column(String, nullable=False)
    plan = Column(String, nullable=False)
    coverage_amount = Column(Float, nullable=False)
    patient = relationship("Patient")

class Schedule(Base):
    """
    description: Represents a doctor's schedule including working hours and breaks.
    """
    __tablename__ = 'schedule'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    doctor_id = Column(Integer, ForeignKey('doctor.id'), nullable=False)
    weekday = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    doctor = relationship("Doctor")

class Treatment(Base):
    """
    description: Represents a treatment plan assigned to a patient.
    """
    __tablename__ = 'treatment'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey('patient.id'), nullable=False)
    description = Column(String, nullable=False)
    start_date = Column(DateTime, default=datetime.datetime.utcnow)
    patient = relationship("Patient")

class Referral(Base):
    """
    description: Represents a referral given to a patient for another specialist.
    """
    __tablename__ = 'referral'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey('patient.id'), nullable=False)
    from_doctor_id = Column(Integer, ForeignKey('doctor.id'), nullable=False)
    to_specialist = Column(String, nullable=False)
    reason = Column(String, nullable=True)
    date_given = Column(DateTime, default=datetime.datetime.utcnow)
    patient = relationship("Patient")
    from_doctor = relationship("Doctor")

# Creating the database tables
Base.metadata.create_all(engine)

# Sample Data
doctors = [
    Doctor(name='Dr. John Doe', specialization='Cardiology'),
    Doctor(name='Dr. Jane Smith', specialization='Pediatrics')
]

patients = [
    Patient(name='Alice Johnson'),
    Patient(name='Bob Brown')
]

rooms = [
    Room(room_number='101', floor=1),
    Room(room_number='102', floor=1)
]

procedures = [
    Procedure(name='X-Ray', cost=150.0, duration=30),
    Procedure(name='Blood Test', cost=75.0, duration=15)
]

session.add_all(doctors + patients + rooms + procedures)
session.commit()

appointments = [
    Appointment(patient_id=1, doctor_id=1, appointment_date=datetime.datetime(2024, 1, 15, 10, 0)),
    Appointment(patient_id=2, doctor_id=2, appointment_date=datetime.datetime(2024, 1, 15, 11, 0))
]

medical_records = [
    MedicalRecord(patient_id=1, description='Annual Physical'),
    MedicalRecord(patient_id=2, description='Flu')
]

bills = [
    Billing(appointment_id=1, amount_due=150.0),
    Billing(appointment_id=2, amount_due=75.0)
]

insurances = [
    Insurance(patient_id=1, provider='HealthUnited', plan='Silver', coverage_amount=5000.0),
    Insurance(patient_id=2, provider='MediCare', plan='Gold', coverage_amount=10000.0)
]

schedules = [
    Schedule(doctor_id=1, weekday='Monday', start_time=datetime.datetime(2024, 1, 15, 9, 0), end_time=datetime.datetime(2024, 1, 15, 17, 0)),
    Schedule(doctor_id=2, weekday='Monday', start_time=datetime.datetime(2024, 1, 15, 9, 0), end_time=datetime.datetime(2024, 1, 15, 17, 0))
]

treatments = [
    Treatment(patient_id=1, description='Healthy diet plan'),
    Treatment(patient_id=2, description='Vaccination')
]

session.add_all(appointments + medical_records + bills + insurances + schedules + treatments)
session.commit()

prescriptions = [
    Prescription(appointment_id=1, medication='Aspirin', dosage='1 tablet daily'),
    Prescription(appointment_id=2, medication='Ibuprofen', dosage='2 tablets every 4 hours')
]

referrals = [
    Referral(patient_id=1, from_doctor_id=1, to_specialist='Orthopedic', reason='Joint pain'),
    Referral(patient_id=2, from_doctor_id=2, to_specialist='ENT', reason='Recurrent ear infection')
]

session.add_all(prescriptions + referrals)
session.commit()
