# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  October 31, 2024 15:44:53
# Database: sqlite:////tmp/tmp.EZqoW5W9Ie/test/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *



class Doctor(SAFRSBaseX, Base):
    """
    description: Represents a doctor with specialization and contact details.
    """
    __tablename__ = 'doctor'
    _s_collection_name = 'Doctor'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    specialization = Column(String, nullable=False)
    phone = Column(String)
    email = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    AppointmentList : Mapped[List["Appointment"]] = relationship(back_populates="doctor")
    ReferralList : Mapped[List["Referral"]] = relationship(back_populates="from_doctor")
    ScheduleList : Mapped[List["Schedule"]] = relationship(back_populates="doctor")



class Patient(SAFRSBaseX, Base):
    """
    description: Represents a patient with personal details and contact information.
    """
    __tablename__ = 'patient'
    _s_collection_name = 'Patient'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    gender = Column(String)
    phone = Column(String)
    email = Column(String)
    address = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    AppointmentList : Mapped[List["Appointment"]] = relationship(back_populates="patient")
    InsuranceList : Mapped[List["Insurance"]] = relationship(back_populates="patient")
    MedicalRecordList : Mapped[List["MedicalRecord"]] = relationship(back_populates="patient")
    ReferralList : Mapped[List["Referral"]] = relationship(back_populates="patient")
    TreatmentList : Mapped[List["Treatment"]] = relationship(back_populates="patient")



class Procedure(SAFRSBaseX, Base):
    """
    description: Represents a medical procedure that can be performed.
    """
    __tablename__ = 'procedure'
    _s_collection_name = 'Procedure'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    cost = Column(Float, nullable=False)
    duration = Column(Integer, nullable=False)

    # parent relationships (access parent)

    # child relationships (access children)



class Room(SAFRSBaseX, Base):
    """
    description: Represents a room used for conducting appointments.
    """
    __tablename__ = 'room'
    _s_collection_name = 'Room'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    room_number = Column(String, nullable=False)
    floor = Column(Integer)
    availability = Column(Boolean, nullable=False)

    # parent relationships (access parent)

    # child relationships (access children)



class Appointment(SAFRSBaseX, Base):
    """
    description: Represents an appointment made by a patient with a doctor.
    """
    __tablename__ = 'appointment'
    _s_collection_name = 'Appointment'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    patient_id = Column(ForeignKey('patient.id'), nullable=False)
    doctor_id = Column(ForeignKey('doctor.id'), nullable=False)
    appointment_date = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)

    # parent relationships (access parent)
    doctor : Mapped["Doctor"] = relationship(back_populates=("AppointmentList"))
    patient : Mapped["Patient"] = relationship(back_populates=("AppointmentList"))

    # child relationships (access children)
    BillingList : Mapped[List["Billing"]] = relationship(back_populates="appointment")
    PrescriptionList : Mapped[List["Prescription"]] = relationship(back_populates="appointment")



class Insurance(SAFRSBaseX, Base):
    """
    description: Contains details about a patient's insurance plan.
    """
    __tablename__ = 'insurance'
    _s_collection_name = 'Insurance'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    patient_id = Column(ForeignKey('patient.id'), nullable=False)
    provider = Column(String, nullable=False)
    plan = Column(String, nullable=False)
    coverage_amount = Column(Float, nullable=False)

    # parent relationships (access parent)
    patient : Mapped["Patient"] = relationship(back_populates=("InsuranceList"))

    # child relationships (access children)



class MedicalRecord(SAFRSBaseX, Base):
    """
    description: Represents the medical records/history of a patient.
    """
    __tablename__ = 'medical_record'
    _s_collection_name = 'MedicalRecord'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    patient_id = Column(ForeignKey('patient.id'), nullable=False)
    description = Column(String, nullable=False)
    record_date = Column(DateTime)

    # parent relationships (access parent)
    patient : Mapped["Patient"] = relationship(back_populates=("MedicalRecordList"))

    # child relationships (access children)



class Referral(SAFRSBaseX, Base):
    """
    description: Represents a referral given to a patient for another specialist.
    """
    __tablename__ = 'referral'
    _s_collection_name = 'Referral'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    patient_id = Column(ForeignKey('patient.id'), nullable=False)
    from_doctor_id = Column(ForeignKey('doctor.id'), nullable=False)
    to_specialist = Column(String, nullable=False)
    reason = Column(String)
    date_given = Column(DateTime)

    # parent relationships (access parent)
    from_doctor : Mapped["Doctor"] = relationship(back_populates=("ReferralList"))
    patient : Mapped["Patient"] = relationship(back_populates=("ReferralList"))

    # child relationships (access children)



class Schedule(SAFRSBaseX, Base):
    """
    description: Represents a doctor's schedule including working hours and breaks.
    """
    __tablename__ = 'schedule'
    _s_collection_name = 'Schedule'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    doctor_id = Column(ForeignKey('doctor.id'), nullable=False)
    weekday = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    # parent relationships (access parent)
    doctor : Mapped["Doctor"] = relationship(back_populates=("ScheduleList"))

    # child relationships (access children)



class Treatment(SAFRSBaseX, Base):
    """
    description: Represents a treatment plan assigned to a patient.
    """
    __tablename__ = 'treatment'
    _s_collection_name = 'Treatment'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    patient_id = Column(ForeignKey('patient.id'), nullable=False)
    description = Column(String, nullable=False)
    start_date = Column(DateTime)

    # parent relationships (access parent)
    patient : Mapped["Patient"] = relationship(back_populates=("TreatmentList"))

    # child relationships (access children)



class Billing(SAFRSBaseX, Base):
    """
    description: Represents the billing information for a patient's appointment.
    """
    __tablename__ = 'billing'
    _s_collection_name = 'Billing'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    appointment_id = Column(ForeignKey('appointment.id'), nullable=False)
    amount_due = Column(Float, nullable=False)
    date_issued = Column(DateTime)

    # parent relationships (access parent)
    appointment : Mapped["Appointment"] = relationship(back_populates=("BillingList"))

    # child relationships (access children)



class Prescription(SAFRSBaseX, Base):
    """
    description: Contains prescriptions issued to a patient during an appointment.
    """
    __tablename__ = 'prescription'
    _s_collection_name = 'Prescription'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    appointment_id = Column(ForeignKey('appointment.id'), nullable=False)
    medication = Column(String, nullable=False)
    dosage = Column(String, nullable=False)
    notes = Column(String)

    # parent relationships (access parent)
    appointment : Mapped["Appointment"] = relationship(back_populates=("PrescriptionList"))

    # child relationships (access children)
