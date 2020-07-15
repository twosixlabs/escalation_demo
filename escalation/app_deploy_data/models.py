# coding: utf-8
from sqlalchemy import BigInteger, Boolean, Column, Float, Integer, Text
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
    inducer_concentration = Column(Float(53))
    inducer_concentration_unit = Column(Text)
    sample_contents = Column(Text)
    temperature = Column(Float(53))
    temperature_unit = Column(Text)
    timepoint = Column(Float(53))
    timepoint_unit = Column(Text)
    aliquot_id = Column(Text)
    total_counts = Column(Integer)
    TX_plate_name = Column(Text)
    TX_project_name = Column(Text)
    TX_sample_name = Column(Text)
    flow_volume = Column(Integer)
    well = Column(Text)
    flow_rate_uL_min = Column("flow_rate_uL/min", Integer)
    date_of_experiment = Column(Text)
    cells_mL = Column("cells/mL", Float(53))
    upload_id = Column(BigInteger, primary_key=True, nullable=False)
    experiment_id_short = Column(Text)


class FlowStatWide(Base):
    __tablename__ = "flow_stat_wide"

    row_index = Column(BigInteger, primary_key=True, nullable=False)
    sample_id = Column(Text)
    experiment_id = Column(Text)
    aliquot_id = Column(Text)
    log10_bin = Column(Float(53))
    BL1_H = Column("BL1-H", Integer)
    BL1H_mean_log10 = Column(Float(53))
    upload_id = Column(BigInteger, primary_key=True, nullable=False)


class GrowthRate(Base):
    __tablename__ = "growth_rate"

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
    fluor_gain_0_10 = Column("fluor_gain_0.10", Float(53))
    fluor_gain_0_20 = Column("fluor_gain_0.20", Float(53))
    fluor_gain_0_10_od = Column("fluor_gain_0.10/od", Float(53))
    fluor_gain_0_20_od = Column("fluor_gain_0.20/od", Float(53))
    fluor_gain_0_30 = Column("fluor_gain_0.30", Float(53))
    fluor_gain_0_30_od = Column("fluor_gain_0.30/od", Float(53))
    upload_id = Column(BigInteger, primary_key=True, nullable=False)
