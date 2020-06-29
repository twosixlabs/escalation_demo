# coding: utf-8
from sqlalchemy import BigInteger, Column, Float, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class MeanPenguinStat(Base):
    __tablename__ = "mean_penguin_stat"

    index = Column(BigInteger, primary_key=True, index=True)
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
    __tablename__ = "penguin_size"

    index = Column(BigInteger, primary_key=True, index=True)
    study_name = Column(Text)
    species = Column(Text)
    island = Column(Text)
    sex = Column(Text)
    region = Column(Text)
    culmen_depth_mm = Column(Float(53))
    culmen_length_mm = Column(Float(53))
    flipper_length_mm = Column(Float(53))
    body_mass_g = Column(Float(53))
