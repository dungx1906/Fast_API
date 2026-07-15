from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

patient_medication = Table(
    "patient_medication",
    Base.metadata,
    Column("patient_id", Integer, ForeignKey("patients.id"), primary_key=True),
    Column("medication_id", Integer, ForeignKey("medications.id"), primary_key=True)
)

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    specialty = Column(String(100), nullable=False)

    patients = relationship("Patient", back_populates="doctor", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Doctor(id={self.id}, name='{self.name}', specialty='{self.specialty}')>"

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_code = Column(String(50), unique=True, nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)

    doctor = relationship("Doctor", back_populates="patients")
    insurance = relationship("Insurance", uselist=False, back_populates="patient", cascade="all, delete-orphan")
    medications = relationship("Medication", secondary=patient_medication, back_populates="patients")

    def __repr__(self):
        return f"<Patient(id={self.id}, code='{self.patient_code}')>"

class Insurance(Base):
    __tablename__ = "insurances"

    id = Column(Integer, primary_key=True, autoincrement=True)
    insurance_number = Column(String(50), unique=True, nullable=False)
    expiry_date = Column(Date, nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), unique=True, nullable=False)

    patient = relationship("Patient", back_populates="insurance")

    def __repr__(self):
        return f"<Insurance(id={self.id}, number='{self.insurance_number}')>"

class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    patients = relationship("Patient", secondary=patient_medication, back_populates="medications")

    def __repr__(self):
        return f"<Medication(id={self.id}, name='{self.name}')>"