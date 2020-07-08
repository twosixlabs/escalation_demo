# coding: utf-8
from sqlalchemy import BigInteger, CheckConstraint, Column, Float, Integer, Text
from sqlalchemy.dialects.mysql import TINYINT, TINYTEXT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class FlowMeta(Base):
    __tablename__ = "flow_meta"

    row_index = Column(BigInteger, primary_key=True, nullable=False)
    _id = Column(Text)
    sample_id = Column(Text)
    experiment_reference = Column(Text)
    experiment_id = Column(Text)
    lab = Column(Text)
    replicate = Column(Integer)
    replicate_group = Column(Text)
    replicate_group_string = Column(Text)
    strain = Column(Text)
    strain_name = Column(Text)
    strain_class = Column(Text)
    standard_type = Column(Text)
    control_type = Column(Text)
    media_type = Column(Text)
    inducer_type = Column(Text)
    inducer_concentration = Column(Float)
    inducer_concentration_unit = Column(Text)
    sample_contents = Column(Text)
    temperature = Column(Float)
    temperature_unit = Column(Text)
    timepoint = Column(Float)
    timepoint_unit = Column(Text)
    aliquot_id = Column(Text)
    flow_rate_uL_min = Column("flow_rate_uL/min", Integer)
    date_of_experiment = Column(Text)
    TX_plate_name = Column(Text)
    TX_project_name = Column(Text)
    TX_sample_name = Column(Text)
    total_counts = Column(Integer)
    flow_volume = Column(Integer)
    well = Column(Text)
    cells_mL = Column("cells/mL", Float)
    upload_id = Column(BigInteger, primary_key=True, nullable=False)
    experiment_id_short = Column(Text)


class FlowStatWide(Base):
    __tablename__ = "flow_stat_wide"

    row_index = Column(BigInteger, primary_key=True, nullable=False)
    sample_id = Column(Text)
    experiment_id = Column(Text)
    aliquot_id = Column(Text)
    log10_bin = Column(Float)
    BL1_A = Column("BL1-A", Integer)
    BL1_H = Column("BL1-H", Integer)
    BL1_W = Column("BL1-W", Integer)
    FSC_A = Column("FSC-A", Integer)
    FSC_H = Column("FSC-H", Integer)
    FSC_W = Column("FSC-W", Integer)
    RL1_A = Column("RL1-A", Integer)
    RL1_H = Column("RL1-H", Integer)
    RL1_W = Column("RL1-W", Integer)
    SSC_A = Column("SSC-A", Integer)
    SSC_H = Column("SSC-H", Integer)
    SSC_W = Column("SSC-W", Integer)
    upload_id = Column(BigInteger, primary_key=True, nullable=False)


class GrowthRate(Base):
    __tablename__ = "growth_rate"
    __table_args__ = (
        CheckConstraint("(`dead` in (0,1))"),
        CheckConstraint("(`ungrowing` in (0,1))"),
    )

    row_index = Column(BigInteger, primary_key=True, nullable=False)
    experiment_id = Column(Text)
    well = Column(Text)
    strain = Column(Text)
    experiment_reference = Column(Text)
    lab = Column(Text)
    strain_name = Column(Text)
    strain_class = Column(Text)
    standard_type = Column(Text)
    control_type = Column(Text)
    media_type = Column(Text)
    inducer_type = Column(Text)
    inducer_concentration = Column(Float)
    inducer_concentration_unit = Column(Text)
    sample_contents = Column(Text)
    temperature = Column(Float)
    temperature_unit = Column(Text)
    od = Column(Float)
    dead = Column(TINYINT(1))
    ungrowing = Column(TINYINT(1))
    doubling_time = Column(Float)
    n0 = Column(Float)
    upload_id = Column(BigInteger, primary_key=True, nullable=False)


class PlateReader(Base):
    __tablename__ = "plate_reader"

    row_index = Column(BigInteger, primary_key=True, nullable=False)
    _id = Column(Text)
    sample_id = Column(Text)
    experiment_reference = Column(Text)
    experiment_id = Column(Text)
    lab = Column(Text)
    replicate = Column(Integer)
    replicate_group = Column(Text)
    replicate_group_string = Column(Text)
    strain = Column(Text)
    strain_name = Column(Text)
    strain_class = Column(Text)
    standard_type = Column(Text)
    control_type = Column(Text)
    media_type = Column(Text)
    inducer_type = Column(Text)
    inducer_concentration = Column(Float)
    inducer_concentration_unit = Column(Text)
    sample_contents = Column(Text)
    temperature = Column(Float)
    temperature_unit = Column(Text)
    timepoint = Column(Float)
    timepoint_unit = Column(Text)
    well = Column(Text)
    container_id = Column(Text)
    aliquot_id = Column(Text)
    od = Column(Float)
    fluor_gain_0_16 = Column("fluor_gain_0.16", Float)
    fluor_gain_0_16_od = Column("fluor_gain_0.16/od", Float)
    upload_id = Column(BigInteger, primary_key=True, nullable=False)
