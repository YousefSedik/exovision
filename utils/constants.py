class Constants:
    TEMPLATE_DIR = "templates"
    STATIC_DIR = "static"
    FEATURES_REQUIRED_TO_PREDICT = [
        "koi_period",
        "koi_period_err1",
        "koi_period_err2",
        "koi_time0bk_err1",
        "koi_time0bk_err2",
        "koi_time0_err1",
        "koi_time0_err2",
        "koi_impact",
        "koi_duration",
        "koi_duration_err1",
        "koi_duration_err2",
        "koi_depth",
        "koi_prad",
        "koi_prad_err1",
        "koi_sma",
        "koi_insol_err1",
        "koi_insol_err2",
        "koi_model_snr",
        "koi_num_transits",
        "koi_bin_oedp_sig",
        "koi_srad",
    ]
    LENGTH_OF_FEATURES_REQUIRED_TO_PREDICT = len(FEATURES_REQUIRED_TO_PREDICT)
    FEATURES_REQUIRED_TO_PREDICT_STRING = ", ".join(FEATURES_REQUIRED_TO_PREDICT)
