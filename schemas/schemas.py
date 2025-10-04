from pydantic import BaseModel, Field


class ModelInputForm(BaseModel):
    model: str = Field()
    koi_period: float = Field()
    koi_period_err1: float = Field()
    koi_period_err2: float = Field()
    koi_time0bk_err1: float = Field()
    koi_time0bk_err2: float = Field()
    koi_time0_err1: float = Field()
    koi_time0_err2: float = Field()
    koi_impact: float = Field()
    koi_duration: float = Field()
    koi_duration_err1: float = Field()
    koi_duration_err2: float = Field()
    koi_depth: float = Field()
    koi_prad: float = Field()
    koi_prad_err1: float = Field()
    koi_sma: float = Field()
    koi_insol_err1: float = Field()
    koi_insol_err2: float = Field()
    koi_model_snr: float = Field()
    koi_num_transits: float = Field()
    koi_bin_oedp_sig: float = Field()
    koi_srad: float = Field()

    def to_list(self):
        return [
            self.koi_period,
            self.koi_period_err1,
            self.koi_period_err2,
            self.koi_time0bk_err1,
            self.koi_time0bk_err2,
            self.koi_time0_err1,
            self.koi_time0_err2,
            self.koi_impact,
            self.koi_duration,
            self.koi_duration_err1,
            self.koi_duration_err2,
            self.koi_depth,
            self.koi_prad,
            self.koi_prad_err1,
            self.koi_sma,
            self.koi_insol_err1,
            self.koi_insol_err2,
            self.koi_model_snr,
            self.koi_num_transits,
            self.koi_bin_oedp_sig,
            self.koi_srad,
        ]


class ChatMessage(BaseModel):
    message: str
