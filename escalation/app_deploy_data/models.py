# coding: utf-8
from sqlalchemy import Boolean, Column, DateTime, Float, Integer, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class CaliforniaFires(Base):
    __tablename__ = 'california_fires'

    upload_id = Column(Integer, primary_key=True, nullable=False)
    row_index = Column(Integer, primary_key=True, nullable=False)
    uniqueid = Column(Text)
    name = Column(Text)
    location = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    acresburned = Column(Integer)
    fueltype = Column(Integer)
    percentcontained = Column(Integer)
    controlstatement = Column(Text)
    conditionstatement = Column(Text)
    counties = Column(Text)
    countyids = Column(Text)
    searchdescription = Column(Text)
    searchkeywords = Column(Text)
    adminunit = Column(Text)
    updated = Column(Text)
    started = Column(Text)
    extinguished = Column(Integer)
    archiveyear = Column(Integer)
    public = Column(Integer)
    active = Column(Integer)
    featured = Column(Integer)
    calfireincident = Column(Integer)
    majorincident = Column(Integer)
    final = Column(Integer)
    status = Column(Text)
    canonicalurl = Column(Text)
    structuresdestroyed = Column(Integer)
    structuresdamaged = Column(Integer)
    structuresthreatened = Column(Integer)
    structuresevacuated = Column(Integer)
    personnelinvolved = Column(Integer)
    crewsinvolved = Column(Integer)
    injuries = Column(Integer)
    fatalities = Column(Integer)
    helicopters = Column(Integer)
    engines = Column(Integer)
    dozers = Column(Integer)
    watertenders = Column(Integer)
    airtankers = Column(Integer)


class DataUploadMetadata(Base):
    __tablename__ = 'data_upload_metadata'

    upload_id = Column(Integer, primary_key=True, nullable=False)
    table_name = Column(Text, primary_key=True, nullable=False)
    upload_time = Column(DateTime)
    active = Column(Boolean)
    username = Column(Text)
    notes = Column(Text)


class MeanPenguinStat(Base):
    __tablename__ = 'mean_penguin_stat'

    upload_id = Column(Integer, primary_key=True, nullable=False)
    row_index = Column(Integer, primary_key=True, nullable=False)
    study_name = Column(Text)
    species = Column(Text)
    sex = Column(Text)
    culmen_length = Column(Float(53))
    culmen_depth = Column(Float(53))
    flipper_length = Column(Float(53))
    body_mass = Column(Float(53))
    delta_15_n = Column(Float(53))
    delta_13_c = Column(Float(53))


class PenguinSize(Base):
    __tablename__ = 'penguin_size'

    upload_id = Column(Integer, primary_key=True, nullable=False)
    row_index = Column(Integer, primary_key=True, nullable=False)
    study_name = Column(Text)
    species = Column(Text)
    island = Column(Text)
    sex = Column(Text)
    region = Column(Text)
    culmen_depth_mm = Column(Float(53))
    culmen_length_mm = Column(Float(53))
    flipper_length_mm = Column(Integer)
    body_mass_g = Column(Integer)


class PenguinSizeSmall(Base):
    __tablename__ = 'penguin_size_small'

    upload_id = Column(Integer, primary_key=True, nullable=False)
    row_index = Column(Integer, primary_key=True, nullable=False)
    species = Column(Text)
    island = Column(Text)
    culmen_length_mm = Column(Float(53))
    culmen_depth_mm = Column(Float(53))
    flipper_length_mm = Column(Integer)
    body_mass_g = Column(Integer)
    sex = Column(Text)
