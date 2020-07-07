# coding: utf-8
from sqlalchemy import BigInteger, Boolean, Column, Float, Integer, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class FlowMeta(Base):
    __tablename__ = "flow_meta"

    index = Column(BigInteger, primary_key=True, nullable=False, index=True)
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
    inducer_concentration = Column(Float(53))
    inducer_concentration_unit = Column(Text)
    sample_contents = Column(Text)
    temperature = Column(Float(53))
    temperature_unit = Column(Text)
    timepoint = Column(Float(53))
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
    cells_mL = Column("cells/mL", Float(53))
    upload_id = Column(Text, primary_key=True, nullable=False)
    experiment_id_short = Column(Text)


class FlowStatWide(Base):
    __tablename__ = "flow_stat_wide"

    index = Column(BigInteger, primary_key=True, nullable=False, index=True)
    sample_id = Column(Text)
    experiment_id = Column(Text)
    aliquot_id = Column(Text)
    log10_bin = Column(Float(53))
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
    upload_id = Column(Text, primary_key=True, nullable=False)


class GrowthRate(Base):
    __tablename__ = "growth_rate"

    index = Column(BigInteger, primary_key=True, nullable=False, index=True)
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
    inducer_concentration = Column(Float(53))
    inducer_concentration_unit = Column(Text)
    sample_contents = Column(Text)
    temperature = Column(Float(53))
    temperature_unit = Column(Text)
    od = Column(Float(53))
    dead = Column(Boolean)
    ungrowing = Column(Boolean)
    doubling_time = Column(Float(53))
    n0 = Column(Float(53))
    upload_id = Column(Text, primary_key=True, nullable=False)


class MeanPenguinStat(Base):
    __tablename__ = "mean_penguin_stat"

    index = Column(BigInteger, primary_key=True, nullable=False, index=True)
    study_name = Column(Text)
    species = Column(Text)
    sex = Column(Text)
    culmen_length = Column(Float(53))
    culmen_depth = Column(Float(53))
    flipper_length = Column(Float(53))
    body_mass = Column(Float(53))
    delta_15_n = Column(Float(53))
    delta_13_c = Column(Float(53))
    upload_id = Column(Text, primary_key=True, nullable=False)


class PenguinSize(Base):
    __tablename__ = "penguin_size"

    index = Column(BigInteger, primary_key=True, nullable=False, index=True)
    study_name = Column(Text)
    species = Column(Text)
    island = Column(Text)
    sex = Column(Text)
    region = Column(Text)
    culmen_depth_mm = Column(Float(53))
    culmen_length_mm = Column(Float(53))
    flipper_length_mm = Column(Float(53))
    body_mass_g = Column(Float(53))
    upload_id = Column(Text, primary_key=True, nullable=False)


class PenguinSizeSmall(Base):
    __tablename__ = "penguin_size_small"

    index = Column(BigInteger, primary_key=True, nullable=False, index=True)
    species = Column(Text)
    island = Column(Text)
    culmen_length_mm = Column(Float(53))
    culmen_depth_mm = Column(Integer)
    flipper_length_mm = Column(Integer)
    body_mass_g = Column(Integer)
    sex = Column(Text)
    upload_id = Column(Text, primary_key=True, nullable=False)


class PlateReader(Base):
    __tablename__ = "plate_reader"

    index = Column(BigInteger, primary_key=True, nullable=False, index=True)
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
    inducer_concentration = Column(Float(53))
    inducer_concentration_unit = Column(Text)
    sample_contents = Column(Text)
    temperature = Column(Float(53))
    temperature_unit = Column(Text)
    timepoint = Column(Float(53))
    timepoint_unit = Column(Text)
    well = Column(Text)
    container_id = Column(Text)
    aliquot_id = Column(Text)
    od = Column(Float(53))
    fluor_gain_0_16 = Column("fluor_gain_0.16", Float(53))
    fluor_gain_0_16_od = Column("fluor_gain_0.16/od", Float(53))
    upload_id = Column(Text, primary_key=True, nullable=False)
