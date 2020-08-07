# coding: utf-8
from sqlalchemy import BigInteger, Column, Float, Table, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


t_experimental_stability_score = Table(
    "experimental_stability_score",
    metadata,
    Column("row_index", BigInteger),
    Column("dataset", Text),
    Column("name", Text),
    Column("counts0_t", Float(53)),
    Column("counts1_t", Float(53)),
    Column("counts2_t", Float(53)),
    Column("counts3_t", Float(53)),
    Column("counts4_t", Float(53)),
    Column("counts5_t", Float(53)),
    Column("counts6_t", Float(53)),
    Column("downsamp_counts1_t", Float(53)),
    Column("downsamp_counts2_t", Float(53)),
    Column("downsamp_counts3_t", Float(53)),
    Column("downsamp_counts4_t", Float(53)),
    Column("downsamp_counts5_t", Float(53)),
    Column("downsamp_counts6_t", Float(53)),
    Column("pred_counts1_t", Float(53)),
    Column("pred_counts2_t", Float(53)),
    Column("pred_counts3_t", Float(53)),
    Column("pred_counts4_t", Float(53)),
    Column("pred_counts5_t", Float(53)),
    Column("pred_counts6_t", Float(53)),
    Column("delta_llh1_t", Float(53)),
    Column("delta_llh2_t", Float(53)),
    Column("delta_llh3_t", Float(53)),
    Column("delta_llh4_t", Float(53)),
    Column("delta_llh5_t", Float(53)),
    Column("delta_llh6_t", Float(53)),
    Column("signed_delta_llh1_t", Float(53)),
    Column("signed_delta_llh2_t", Float(53)),
    Column("signed_delta_llh3_t", Float(53)),
    Column("signed_delta_llh4_t", Float(53)),
    Column("signed_delta_llh5_t", Float(53)),
    Column("signed_delta_llh6_t", Float(53)),
    Column("sel_k_t", Float(53)),
    Column("sum_delta_llh_t", Float(53)),
    Column("sum_signed_delta_llh_t", Float(53)),
    Column("ec50_95ci_lbound_t", Float(53)),
    Column("ec50_95ci_ubound_t", Float(53)),
    Column("ec50_95ci_t", Float(53)),
    Column("ec50_v2_t", Float(53)),
    Column("protein_sequence_t", Text),
    Column("full_protein_sequence_t", Text),
    Column("ec50_pred_t", Float(53)),
    Column("ec50_rise_v2_t", Float(53)),
    Column("stabilityscore_v2_t", Float(53)),
    Column("counts0_c", Float(53)),
    Column("counts1_c", Float(53)),
    Column("counts2_c", Float(53)),
    Column("counts3_c", Float(53)),
    Column("counts4_c", Float(53)),
    Column("counts5_c", Float(53)),
    Column("counts6_c", Float(53)),
    Column("downsamp_counts1_c", Float(53)),
    Column("downsamp_counts2_c", Float(53)),
    Column("downsamp_counts3_c", Float(53)),
    Column("downsamp_counts4_c", Float(53)),
    Column("downsamp_counts5_c", Float(53)),
    Column("downsamp_counts6_c", Float(53)),
    Column("pred_counts1_c", Float(53)),
    Column("pred_counts2_c", Float(53)),
    Column("pred_counts3_c", Float(53)),
    Column("pred_counts4_c", Float(53)),
    Column("pred_counts5_c", Float(53)),
    Column("pred_counts6_c", Float(53)),
    Column("delta_llh1_c", Float(53)),
    Column("delta_llh2_c", Float(53)),
    Column("delta_llh3_c", Float(53)),
    Column("delta_llh4_c", Float(53)),
    Column("delta_llh5_c", Float(53)),
    Column("delta_llh6_c", Float(53)),
    Column("signed_delta_llh1_c", Float(53)),
    Column("signed_delta_llh2_c", Float(53)),
    Column("signed_delta_llh3_c", Float(53)),
    Column("signed_delta_llh4_c", Float(53)),
    Column("signed_delta_llh5_c", Float(53)),
    Column("signed_delta_llh6_c", Float(53)),
    Column("sel_k_c", Float(53)),
    Column("sum_delta_llh_c", Float(53)),
    Column("sum_signed_delta_llh_c", Float(53)),
    Column("ec50_95ci_lbound_c", Float(53)),
    Column("ec50_95ci_ubound_c", Float(53)),
    Column("ec50_95ci_c", Float(53)),
    Column("ec50_v2_c", Float(53)),
    Column("protein_sequence_c", Text),
    Column("full_protein_sequence_c", Text),
    Column("ec50_pred_c", Float(53)),
    Column("ec50_rise_v2_c", Float(53)),
    Column("stabilityscore_v2_c", Float(53)),
    Column("stabilityscore_v2", Float(53)),
    Column("ec50_c", Float(53)),
    Column("ec50_t", Float(53)),
    Column("stabilityscore_c", Float(53)),
    Column("stabilityscore_t", Float(53)),
    Column("ec50_rise_c", Float(53)),
    Column("ec50_rise_t", Float(53)),
    Column("stabilityscore", Float(53)),
    Column("ec50_t_calibrated_1", Float(53)),
    Column("ec50_c_calibrated_1", Float(53)),
    Column("ec50_calibrated_t", Float(53)),
    Column("ec50_calibrated_c", Float(53)),
    Column("ec50_rise_calibrated_t", Float(53)),
    Column("ec50_rise_calibrated_c", Float(53)),
    Column("stabilityscore_calibrated_t", Float(53)),
    Column("stabilityscore_calibrated_c", Float(53)),
    Column("stabilityscore_calibrated", Float(53)),
    Column("ec50_cnn_pred_t", Float(53)),
    Column("ec50_cnn_pred_c", Float(53)),
    Column("stabilityscore_cnn_t", Float(53)),
    Column("stabilityscore_cnn_c", Float(53)),
    Column("stabilityscore_cnn", Float(53)),
    Column("stabilityscore_cnn_calibrated_c", Float(53)),
    Column("stabilityscore_cnn_calibrated_t", Float(53)),
    Column("stabilityscore_cnn_calibrated", Float(53)),
    Column("sequence", Text),
    Column("upload_id", BigInteger),
)


class StructuralMetric(Base):
    __tablename__ = "structural_metrics"

    row_index = Column(BigInteger, primary_key=True, nullable=False)
    dataset = Column(Text)
    name = Column(Text)
    sequence = Column(Text)
    AlaCount = Column(Float(53))
    T1_absq = Column(Float(53))
    T1_netq = Column(Float(53))
    Tend_absq = Column(Float(53))
    Tend_netq = Column(Float(53))
    Tminus1_absq = Column(Float(53))
    Tminus1_netq = Column(Float(53))
    Unnamed__0 = Column("Unnamed: 0", Text)
    abego_res_profile = Column(Float(53))
    abego_res_profile_penalty = Column(Float(53))
    avg_all_frags = Column(Float(53))
    avg_best_frag = Column(Float(53))
    bb = Column(Float(53))
    buns_bb_heavy = Column(Float(53))
    buns_nonheavy = Column(Float(53))
    buns_sc_heavy = Column(Float(53))
    buried_minus_exposed = Column(Float(53))
    buried_np = Column(Float(53))
    buried_np_AFILMVWY = Column(Float(53))
    buried_np_AFILMVWY_per_res = Column(Float(53))
    buried_np_per_res = Column(Float(53))
    buried_over_exposed = Column(Float(53))
    chip_name = Column(Text)
    chymo_cut_sites = Column(BigInteger)
    chymo_with_LM_cut_sites = Column(Float(53))
    contact_all = Column(Float(53))
    contact_core_SASA = Column(Float(53))
    contact_core_SCN = Column(Float(53))
    contig_not_hp_avg = Column(Float(53))
    contig_not_hp_avg_norm = Column(Float(53))
    contig_not_hp_internal_max = Column(BigInteger)
    contig_not_hp_max = Column(BigInteger)
    degree = Column(Float(53))
    description = Column(Text)
    dslf_fa13 = Column(Float(53))
    dssp = Column(Text)
    entropy = Column(Float(53))
    exposed_hydrophobics = Column(Float(53))
    exposed_np_AFILMVWY = Column(Float(53))
    exposed_polars = Column(Float(53))
    exposed_total = Column(Float(53))
    fa_atr = Column(Float(53))
    fa_atr_per_res = Column(Float(53))
    fa_dun_dev = Column(Float(53))
    fa_dun_rot = Column(Float(53))
    fa_dun_semi = Column(Float(53))
    fa_elec = Column(Float(53))
    fa_intra_atr_xover4 = Column(Float(53))
    fa_intra_elec = Column(Float(53))
    fa_intra_rep_xover4 = Column(Float(53))
    fa_intra_sol_xover4 = Column(Float(53))
    fa_rep = Column(Float(53))
    fa_rep_per_res = Column(Float(53))
    fa_sol = Column(Float(53))
    frac_helix = Column(Float(53))
    frac_loop = Column(Float(53))
    frac_sheet = Column(Float(53))
    fxn_exposed_is_np = Column(Float(53))
    hbond_bb_sc = Column(Float(53))
    hbond_lr_bb = Column(Float(53))
    hbond_lr_bb_per_sheet = Column(Float(53))
    hbond_sc = Column(Float(53))
    hbond_sr_bb = Column(Float(53))
    hbond_sr_bb_per_helix = Column(Float(53))
    helix_sc = Column(Float(53))
    holes = Column(Float(53))
    hphob_sc_contacts = Column(BigInteger)
    hphob_sc_degree = Column(Float(53))
    hxl_tors = Column(Float(53))
    hydrophobicity = Column(Float(53))
    largest_hphob_cluster = Column(BigInteger)
    lk_ball = Column(Float(53))
    lk_ball_bridge = Column(Float(53))
    lk_ball_bridge_uncpl = Column(Float(53))
    lk_ball_iso = Column(Float(53))
    loop_sc = Column(Text)
    mismatch_probability = Column(Float(53))
    n_charged = Column(Float(53))
    n_hphob_clusters = Column(BigInteger)
    n_hydrophobic = Column(BigInteger)
    n_hydrophobic_noA = Column(BigInteger)
    n_polar_core = Column(Float(53))
    n_res = Column(BigInteger)
    nearest_chymo_cut_to_Cterm = Column(BigInteger)
    nearest_chymo_cut_to_Nterm = Column(BigInteger)
    nearest_chymo_cut_to_term = Column(BigInteger)
    nearest_tryp_cut_to_Cterm = Column(BigInteger)
    nearest_tryp_cut_to_Nterm = Column(BigInteger)
    nearest_tryp_cut_to_term = Column(BigInteger)
    net_atr_net_sol_per_res = Column(Float(53))
    net_atr_per_res = Column(Float(53))
    net_sol_per_res = Column(Float(53))
    netcharge = Column(Float(53))
    nres = Column(Float(53))
    nres_helix = Column(BigInteger)
    nres_loop = Column(BigInteger)
    nres_sheet = Column(BigInteger)
    omega = Column(Float(53))
    one_core_each = Column(Float(53))
    p_aa_pp = Column(Float(53))
    pack = Column(Float(53))
    percent_core_SASA = Column(Float(53))
    percent_core_SCN = Column(Float(53))
    pro_close = Column(Float(53))
    rama_prepro = Column(Float(53))
    ref = Column(Float(53))
    res_count_core_SASA = Column(Float(53))
    res_count_core_SCN = Column(Float(53))
    score_per_res = Column(Float(53))
    ss_contributes_core = Column(Float(53))
    ss_sc = Column(Text)
    sum_best_frags = Column(Float(53))
    total_score = Column(Float(53))
    tryp_cut_sites = Column(BigInteger)
    two_core_each = Column(Float(53))
    worst6frags = Column(Float(53))
    worstfrag = Column(Float(53))
    upload_id = Column(BigInteger, primary_key=True, nullable=False)


class TestPenguin(Base):
    __tablename__ = "test_penguin"

    row_index = Column(BigInteger, primary_key=True, nullable=False)
    study_name = Column(Text)
    species = Column(Text)
    island = Column(Text)
    sex = Column(Text)
    region = Column(Text)
    culmen_depth_mm = Column(Float(53))
    culmen_length_mm = Column(Float(53))
    flipper_length_mm = Column(Float(53))
    body_mass_g = Column(Float(53))
    upload_id = Column(BigInteger, primary_key=True, nullable=False)
