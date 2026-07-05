
from experta import Rule, MATCH
from Facts import Label, Membership, Quality, Explanation
from defuzzification import final_quality_value


class KnowledgeBaseRulesPart1:
    @Rule(Label(name="lighting", label="low"),
        Label(name="blur", label="low"),
        Label(name="pose", label="low"),
        Label(name="eye_open", label="low"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_01_low_low_low_low(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_01_low_low_low_low",
        reason=f"lighting=low, blur=low, pose=low, eye_open=low -> Low (value={value})"))

    @Rule( Label(name="lighting", label="low"),
        Label(name="blur", label="low"),
        Label(name="pose", label="low"),
        Label(name="eye_open", label="medium"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_02_low_low_low_medium(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_02_low_low_low_medium",
        reason=f"lighting=low, blur=low, pose=low, eye_open=medium -> Low (value={value})"))

    @Rule(Label(name="lighting", label="low"),
        Label(name="blur", label="low"),
        Label(name="pose", label="low"),
        Label(name="eye_open", label="high"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_03_low_low_low_high(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_03_low_low_low_high",
        reason=f"lighting=low, blur=low, pose=low, eye_open=high -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="low"),
        Label(name="blur", label="low"),
        Label(name="pose", label="medium"),
        Label(name="eye_open", label="low"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_04_low_low_medium_low(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_04_low_low_medium_low",
         reason=f"lighting=low, blur=low, pose=medium, eye_open=low -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="low"),
        Label(name="blur", label="low"),
        Label(name="pose", label="medium"),
        Label(name="eye_open", label="medium"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_05_low_low_medium_medium(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_05_low_low_medium_medium",
     reason=f"lighting=low, blur=low, pose=medium, eye_open=medium -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="low"),
        Label(name="blur", label="low"),
        Label(name="pose", label="medium"),
        Label(name="eye_open", label="high"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_06_low_low_medium_high(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_06_low_low_medium_high",
                                  reason=f"lighting=low, blur=low, pose=medium, eye_open=high -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="low"),
        Label(name="blur", label="low"),
        Label(name="pose", label="high"),
        Label(name="eye_open", label="low"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_07_low_low_high_low(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_07_low_low_high_low",
        reason=f"lighting=low, blur=low, pose=high, eye_open=low -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="low"),
        Label(name="blur", label="low"),
        Label(name="pose", label="high"),
        Label(name="eye_open", label="medium"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_08_low_low_high_medium(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_08_low_low_high_medium",
                                  reason=f"lighting=low, blur=low, pose=high, eye_open=medium -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="low"),
        Label(name="blur", label="low"),
        Label(name="pose", label="high"),
        Label(name="eye_open", label="high"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_09_low_low_high_high(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_09_low_low_high_high",
         reason=f"lighting=low, blur=low, pose=high, eye_open=high -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="low"),
        Label(name="blur", label="medium"),
        Label(name="pose", label="low"),
        Label(name="eye_open", label="low"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_10_low_medium_low_low(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_10_low_medium_low_low",
        reason=f"lighting=low, blur=medium, pose=low, eye_open=low -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="low"),
        Label(name="blur", label="medium"),
        Label(name="pose", label="low"),
        Label(name="eye_open", label="medium"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_11_low_medium_low_medium(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_11_low_medium_low_medium",
        reason=f"lighting=low, blur=medium, pose=low, eye_open=medium -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="low"),
        Label(name="blur", label="medium"),
        Label(name="pose", label="low"),
        Label(name="eye_open", label="high"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_12_low_medium_low_high(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_12_low_medium_low_high",
         reason=f"lighting=low, blur=medium, pose=low, eye_open=high -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="low"),
        Label(name="blur", label="medium"),
        Label(name="pose", label="medium"),
        Label(name="eye_open", label="low"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_13_low_medium_medium_low(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_13_low_medium_medium_low",
        reason=f"lighting=low, blur=medium, pose=medium, eye_open=low -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="low"),
        Label(name="blur", label="medium"),
        Label(name="pose", label="medium"),
        Label(name="eye_open", label="medium"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_14_low_medium_medium_medium(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Medium", value=value))
        self.declare(Explanation(rule_name="combo_14_low_medium_medium_medium",
         reason=f"lighting=low, blur=medium, pose=medium, eye_open=medium -> Medium (value={value})"))

    @Rule(
        Label(name="lighting", label="low"),
        Label(name="blur", label="medium"),
        Label(name="pose", label="medium"),
        Label(name="eye_open", label="high"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_15_low_medium_medium_high(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Medium", value=value))
        self.declare(Explanation(rule_name="combo_15_low_medium_medium_high",
         reason=f"lighting=low, blur=medium, pose=medium, eye_open=high -> Medium (value={value})"))

    @Rule(
        Label(name="lighting", label="low"),
        Label(name="blur", label="medium"),
        Label(name="pose", label="high"),
        Label(name="eye_open", label="low"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_16_low_medium_high_low(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_16_low_medium_high_low",
        reason=f"lighting=low, blur=medium, pose=high, eye_open=low -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="low"),
        Label(name="blur", label="medium"),
        Label(name="pose", label="high"),
        Label(name="eye_open", label="medium"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_17_low_medium_high_medium(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Medium", value=value))
        self.declare(Explanation(rule_name="combo_17_low_medium_high_medium",
                                  reason=f"lighting=low, blur=medium, pose=high, eye_open=medium -> Medium (value={value})"))

    @Rule(
        Label(name="lighting", label="low"),
        Label(name="blur", label="medium"),
        Label(name="pose", label="high"),
        Label(name="eye_open", label="high"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_18_low_medium_high_high(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Medium", value=value))
        self.declare(Explanation(rule_name="combo_18_low_medium_high_high",
        reason=f"lighting=low, blur=medium, pose=high, eye_open=high -> Medium (value={value})"))

    @Rule(
        Label(name="lighting", label="low"),
        Label(name="blur", label="high"),
        Label(name="pose", label="low"),
        Label(name="eye_open", label="low"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_19_low_high_low_low(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_19_low_high_low_low",
        reason=f"lighting=low, blur=high, pose=low, eye_open=low -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="low"),
        Label(name="blur", label="high"),
        Label(name="pose", label="low"),
        Label(name="eye_open", label="medium"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_20_low_high_low_medium(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_20_low_high_low_medium",
       reason=f"lighting=low, blur=high, pose=low, eye_open=medium -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="low"),
        Label(name="blur", label="high"),
        Label(name="pose", label="low"),
        Label(name="eye_open", label="high"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_21_low_high_low_high(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_21_low_high_low_high",
         reason=f"lighting=low, blur=high, pose=low, eye_open=high -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="low"),
        Label(name="blur", label="high"),
        Label(name="pose", label="medium"),
        Label(name="eye_open", label="low"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_22_low_high_medium_low(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_22_low_high_medium_low",
        reason=f"lighting=low, blur=high, pose=medium, eye_open=low -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="low"),
        Label(name="blur", label="high"),
        Label(name="pose", label="medium"),
        Label(name="eye_open", label="medium"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_23_low_high_medium_medium(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Medium", value=value))
        self.declare(Explanation(rule_name="combo_23_low_high_medium_medium",
        reason=f"lighting=low, blur=high, pose=medium, eye_open=medium -> Medium (value={value})"))

    @Rule(
        Label(name="lighting", label="low"),
        Label(name="blur", label="high"),
        Label(name="pose", label="medium"),
        Label(name="eye_open", label="high"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_24_low_high_medium_high(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Medium", value=value))
        self.declare(Explanation(rule_name="combo_24_low_high_medium_high",
         reason=f"lighting=low, blur=high, pose=medium, eye_open=high -> Medium (value={value})"))

    @Rule(
        Label(name="lighting", label="low"),
        Label(name="blur", label="high"),
        Label(name="pose", label="high"),
        Label(name="eye_open", label="low"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_25_low_high_high_low(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_25_low_high_high_low",
        reason=f"lighting=low, blur=high, pose=high, eye_open=low -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="low"),
        Label(name="blur", label="high"),
        Label(name="pose", label="high"),
        Label(name="eye_open", label="medium"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_26_low_high_high_medium(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Medium", value=value))
        self.declare(Explanation(rule_name="combo_26_low_high_high_medium",
                                  reason=f"lighting=low, blur=high, pose=high, eye_open=medium -> Medium (value={value})"))

    @Rule(
        Label(name="lighting", label="low"),
        Label(name="blur", label="high"),
        Label(name="pose", label="high"),
        Label(name="eye_open", label="high"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_27_low_high_high_high(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="High", value=value))
        self.declare(Explanation(rule_name="combo_27_low_high_high_high",
        reason=f"lighting=low, blur=high, pose=high, eye_open=high -> High (value={value})"))

    @Rule(
        Label(name="lighting", label="medium"),
        Label(name="blur", label="low"),
        Label(name="pose", label="low"),
        Label(name="eye_open", label="low"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_28_medium_low_low_low(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_28_medium_low_low_low",
         reason=f"lighting=medium, blur=low, pose=low, eye_open=low -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="medium"),
        Label(name="blur", label="low"),
        Label(name="pose", label="low"),
        Label(name="eye_open", label="medium"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_29_medium_low_low_medium(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_29_medium_low_low_medium",
        reason=f"lighting=medium, blur=low, pose=low, eye_open=medium -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="medium"),
        Label(name="blur", label="low"),
        Label(name="pose", label="low"),
        Label(name="eye_open", label="high"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_30_medium_low_low_high(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_30_medium_low_low_high",
        reason=f"lighting=medium, blur=low, pose=low, eye_open=high -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="medium"),
        Label(name="blur", label="low"),
        Label(name="pose", label="medium"),
        Label(name="eye_open", label="low"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_31_medium_low_medium_low(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_31_medium_low_medium_low",
                                  reason=f"lighting=medium, blur=low, pose=medium, eye_open=low -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="medium"),
        Label(name="blur", label="low"),
        Label(name="pose", label="medium"),
        Label(name="eye_open", label="medium"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_32_medium_low_medium_medium(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_32_medium_low_medium_medium",
     reason=f"lighting=medium, blur=low, pose=medium, eye_open=medium -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="medium"),
        Label(name="blur", label="low"),
        Label(name="pose", label="medium"),
        Label(name="eye_open", label="high"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_33_medium_low_medium_high(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_33_medium_low_medium_high",
        reason=f"lighting=medium, blur=low, pose=medium, eye_open=high -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="medium"),
        Label(name="blur", label="low"),
        Label(name="pose", label="high"),
        Label(name="eye_open", label="low"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_34_medium_low_high_low(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_34_medium_low_high_low",
                                  reason=f"lighting=medium, blur=low, pose=high, eye_open=low -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="medium"),
        Label(name="blur", label="low"),
        Label(name="pose", label="high"),
        Label(name="eye_open", label="medium"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_35_medium_low_high_medium(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_35_medium_low_high_medium",
                                  reason=f"lighting=medium, blur=low, pose=high, eye_open=medium -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="medium"),
        Label(name="blur", label="low"),
        Label(name="pose", label="high"),
        Label(name="eye_open", label="high"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_36_medium_low_high_high(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_36_medium_low_high_high",
                                  reason=f"lighting=medium, blur=low, pose=high, eye_open=high -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="medium"),
        Label(name="blur", label="medium"),
        Label(name="pose", label="low"),
        Label(name="eye_open", label="low"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_37_medium_medium_low_low(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_37_medium_medium_low_low",
                                  reason=f"lighting=medium, blur=medium, pose=low, eye_open=low -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="medium"),
        Label(name="blur", label="medium"),
        Label(name="pose", label="low"),
        Label(name="eye_open", label="medium"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_38_medium_medium_low_medium(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_38_medium_medium_low_medium",
                                  reason=f"lighting=medium, blur=medium, pose=low, eye_open=medium -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="medium"),
        Label(name="blur", label="medium"),
        Label(name="pose", label="low"),
        Label(name="eye_open", label="high"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_39_medium_medium_low_high(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_39_medium_medium_low_high",
                                  reason=f"lighting=medium, blur=medium, pose=low, eye_open=high -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="medium"),
        Label(name="blur", label="medium"),
        Label(name="pose", label="medium"),
        Label(name="eye_open", label="low"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_40_medium_medium_medium_low(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_40_medium_medium_medium_low",
                                  reason=f"lighting=medium, blur=medium, pose=medium, eye_open=low -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="medium"),
        Label(name="blur", label="medium"),
        Label(name="pose", label="medium"),
        Label(name="eye_open", label="medium"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_41_medium_medium_medium_medium(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Medium", value=value))
        self.declare(Explanation(rule_name="combo_41_medium_medium_medium_medium",
                                  reason=f"lighting=medium, blur=medium, pose=medium, eye_open=medium -> Medium (value={value})"))