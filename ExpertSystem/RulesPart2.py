
from experta import Rule, MATCH
from Facts import Label, Membership, Quality, Explanation
from defuzzification import final_quality_value


class KnowledgeBaseRulesPart2:
    @Rule(Label(name="lighting", label="medium"),
        Label(name="blur", label="medium"),
        Label(name="pose", label="medium"),
        Label(name="eye_open", label="high"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_42_medium_medium_medium_high(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Medium", value=value))
        self.declare(Explanation(rule_name="combo_42_medium_medium_medium_high",
        reason=f"lighting=medium, blur=medium, pose=medium, eye_open=high -> Medium (value={value})"))

    @Rule(Label(name="lighting", label="medium"),
        Label(name="blur", label="medium"),
        Label(name="pose", label="high"),
        Label(name="eye_open", label="low"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_43_medium_medium_high_low(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_43_medium_medium_high_low",
                                  reason=f"lighting=medium, blur=medium, pose=high, eye_open=low -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="medium"),
        Label(name="blur", label="medium"),
        Label(name="pose", label="high"),
        Label(name="eye_open", label="medium"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_44_medium_medium_high_medium(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Medium", value=value))
        self.declare(Explanation(rule_name="combo_44_medium_medium_high_medium",
                                  reason=f"lighting=medium, blur=medium, pose=high, eye_open=medium -> Medium (value={value})"))

    @Rule(
        Label(name="lighting", label="medium"),
        Label(name="blur", label="medium"),
        Label(name="pose", label="high"),
        Label(name="eye_open", label="high"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_45_medium_medium_high_high(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="High", value=value))
        self.declare(Explanation(rule_name="combo_45_medium_medium_high_high",
                                  reason=f"lighting=medium, blur=medium, pose=high, eye_open=high -> High (value={value})"))

    @Rule(
        Label(name="lighting", label="medium"),
        Label(name="blur", label="high"),
        Label(name="pose", label="low"),
        Label(name="eye_open", label="low"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_46_medium_high_low_low(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_46_medium_high_low_low",
                                  reason=f"lighting=medium, blur=high, pose=low, eye_open=low -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="medium"),
        Label(name="blur", label="high"),
        Label(name="pose", label="low"),
        Label(name="eye_open", label="medium"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_47_medium_high_low_medium(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_47_medium_high_low_medium",
                                  reason=f"lighting=medium, blur=high, pose=low, eye_open=medium -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="medium"),
        Label(name="blur", label="high"),
        Label(name="pose", label="low"),
        Label(name="eye_open", label="high"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_48_medium_high_low_high(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_48_medium_high_low_high",
                                  reason=f"lighting=medium, blur=high, pose=low, eye_open=high -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="medium"),
        Label(name="blur", label="high"),
        Label(name="pose", label="medium"),
        Label(name="eye_open", label="low"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_49_medium_high_medium_low(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_49_medium_high_medium_low",
                                  reason=f"lighting=medium, blur=high, pose=medium, eye_open=low -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="medium"),
        Label(name="blur", label="high"),
        Label(name="pose", label="medium"),
        Label(name="eye_open", label="medium"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_50_medium_high_medium_medium(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Medium", value=value))
        self.declare(Explanation(rule_name="combo_50_medium_high_medium_medium",
                                  reason=f"lighting=medium, blur=high, pose=medium, eye_open=medium -> Medium (value={value})"))

    @Rule(
        Label(name="lighting", label="medium"),
        Label(name="blur", label="high"),
        Label(name="pose", label="medium"),
        Label(name="eye_open", label="high"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_51_medium_high_medium_high(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="High", value=value))
        self.declare(Explanation(rule_name="combo_51_medium_high_medium_high",
                                  reason=f"lighting=medium, blur=high, pose=medium, eye_open=high -> High (value={value})"))

    @Rule(
        Label(name="lighting", label="medium"),
        Label(name="blur", label="high"),
        Label(name="pose", label="high"),
        Label(name="eye_open", label="low"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_52_medium_high_high_low(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_52_medium_high_high_low",
                                  reason=f"lighting=medium, blur=high, pose=high, eye_open=low -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="medium"),
        Label(name="blur", label="high"),
        Label(name="pose", label="high"),
        Label(name="eye_open", label="medium"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_53_medium_high_high_medium(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="High", value=value))
        self.declare(Explanation(rule_name="combo_53_medium_high_high_medium",
                                  reason=f"lighting=medium, blur=high, pose=high, eye_open=medium -> High (value={value})"))

    @Rule(
        Label(name="lighting", label="medium"),
        Label(name="blur", label="high"),
        Label(name="pose", label="high"),
        Label(name="eye_open", label="high"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_54_medium_high_high_high(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="High", value=value))
        self.declare(Explanation(rule_name="combo_54_medium_high_high_high",
                                  reason=f"lighting=medium, blur=high, pose=high, eye_open=high -> High (value={value})"))

    @Rule(
        Label(name="lighting", label="high"),
        Label(name="blur", label="low"),
        Label(name="pose", label="low"),
        Label(name="eye_open", label="low"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_55_high_low_low_low(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_55_high_low_low_low",
                                  reason=f"lighting=high, blur=low, pose=low, eye_open=low -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="high"),
        Label(name="blur", label="low"),
        Label(name="pose", label="low"),
        Label(name="eye_open", label="medium"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_56_high_low_low_medium(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_56_high_low_low_medium",
                                  reason=f"lighting=high, blur=low, pose=low, eye_open=medium -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="high"),
        Label(name="blur", label="low"),
        Label(name="pose", label="low"),
        Label(name="eye_open", label="high"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_57_high_low_low_high(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_57_high_low_low_high",
                                  reason=f"lighting=high, blur=low, pose=low, eye_open=high -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="high"),
        Label(name="blur", label="low"),
        Label(name="pose", label="medium"),
        Label(name="eye_open", label="low"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_58_high_low_medium_low(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_58_high_low_medium_low",
                                  reason=f"lighting=high, blur=low, pose=medium, eye_open=low -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="high"),
        Label(name="blur", label="low"),
        Label(name="pose", label="medium"),
        Label(name="eye_open", label="medium"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_59_high_low_medium_medium(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_59_high_low_medium_medium",
                                  reason=f"lighting=high, blur=low, pose=medium, eye_open=medium -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="high"),
        Label(name="blur", label="low"),
        Label(name="pose", label="medium"),
        Label(name="eye_open", label="high"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_60_high_low_medium_high(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_60_high_low_medium_high",
                                  reason=f"lighting=high, blur=low, pose=medium, eye_open=high -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="high"),
        Label(name="blur", label="low"),
        Label(name="pose", label="high"),
        Label(name="eye_open", label="low"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_61_high_low_high_low(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_61_high_low_high_low",
                                  reason=f"lighting=high, blur=low, pose=high, eye_open=low -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="high"),
        Label(name="blur", label="low"),
        Label(name="pose", label="high"),
        Label(name="eye_open", label="medium"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_62_high_low_high_medium(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_62_high_low_high_medium",
                                  reason=f"lighting=high, blur=low, pose=high, eye_open=medium -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="high"),
        Label(name="blur", label="low"),
        Label(name="pose", label="high"),
        Label(name="eye_open", label="high"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_63_high_low_high_high(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_63_high_low_high_high",
                                  reason=f"lighting=high, blur=low, pose=high, eye_open=high -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="high"),
        Label(name="blur", label="medium"),
        Label(name="pose", label="low"),
        Label(name="eye_open", label="low"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_64_high_medium_low_low(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_64_high_medium_low_low",
                                  reason=f"lighting=high, blur=medium, pose=low, eye_open=low -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="high"),
        Label(name="blur", label="medium"),
        Label(name="pose", label="low"),
        Label(name="eye_open", label="medium"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_65_high_medium_low_medium(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_65_high_medium_low_medium",
                                  reason=f"lighting=high, blur=medium, pose=low, eye_open=medium -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="high"),
        Label(name="blur", label="medium"),
        Label(name="pose", label="low"),
        Label(name="eye_open", label="high"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_66_high_medium_low_high(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_66_high_medium_low_high",
                                  reason=f"lighting=high, blur=medium, pose=low, eye_open=high -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="high"),
        Label(name="blur", label="medium"),
        Label(name="pose", label="medium"),
        Label(name="eye_open", label="low"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_67_high_medium_medium_low(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_67_high_medium_medium_low",
                                  reason=f"lighting=high, blur=medium, pose=medium, eye_open=low -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="high"),
        Label(name="blur", label="medium"),
        Label(name="pose", label="medium"),
        Label(name="eye_open", label="medium"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_68_high_medium_medium_medium(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Medium", value=value))
        self.declare(Explanation(rule_name="combo_68_high_medium_medium_medium",
                                  reason=f"lighting=high, blur=medium, pose=medium, eye_open=medium -> Medium (value={value})"))

    @Rule(
        Label(name="lighting", label="high"),
        Label(name="blur", label="medium"),
        Label(name="pose", label="medium"),
        Label(name="eye_open", label="high"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_69_high_medium_medium_high(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Medium", value=value))
        self.declare(Explanation(rule_name="combo_69_high_medium_medium_high",
                                  reason=f"lighting=high, blur=medium, pose=medium, eye_open=high -> Medium (value={value})"))

    @Rule(
        Label(name="lighting", label="high"),
        Label(name="blur", label="medium"),
        Label(name="pose", label="high"),
        Label(name="eye_open", label="low"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_70_high_medium_high_low(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_70_high_medium_high_low",
                                  reason=f"lighting=high, blur=medium, pose=high, eye_open=low -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="high"),
        Label(name="blur", label="medium"),
        Label(name="pose", label="high"),
        Label(name="eye_open", label="medium"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_71_high_medium_high_medium(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Medium", value=value))
        self.declare(Explanation(rule_name="combo_71_high_medium_high_medium",
                                  reason=f"lighting=high, blur=medium, pose=high, eye_open=medium -> Medium (value={value})"))

    @Rule(
        Label(name="lighting", label="high"),
        Label(name="blur", label="medium"),
        Label(name="pose", label="high"),
        Label(name="eye_open", label="high"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_72_high_medium_high_high(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="High", value=value))
        self.declare(Explanation(rule_name="combo_72_high_medium_high_high",
                                  reason=f"lighting=high, blur=medium, pose=high, eye_open=high -> High (value={value})"))

    @Rule(
        Label(name="lighting", label="high"),
        Label(name="blur", label="high"),
        Label(name="pose", label="low"),
        Label(name="eye_open", label="low"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_73_high_high_low_low(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_73_high_high_low_low",
                                  reason=f"lighting=high, blur=high, pose=low, eye_open=low -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="high"),
        Label(name="blur", label="high"),
        Label(name="pose", label="low"),
        Label(name="eye_open", label="medium"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_74_high_high_low_medium(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_74_high_high_low_medium",
                                  reason=f"lighting=high, blur=high, pose=low, eye_open=medium -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="high"),
        Label(name="blur", label="high"),
        Label(name="pose", label="low"),
        Label(name="eye_open", label="high"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_75_high_high_low_high(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_75_high_high_low_high",
                                  reason=f"lighting=high, blur=high, pose=low, eye_open=high -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="high"),
        Label(name="blur", label="high"),
        Label(name="pose", label="medium"),
        Label(name="eye_open", label="low"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_76_high_high_medium_low(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_76_high_high_medium_low",
                                  reason=f"lighting=high, blur=high, pose=medium, eye_open=low -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="high"),
        Label(name="blur", label="high"),
        Label(name="pose", label="medium"),
        Label(name="eye_open", label="medium"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_77_high_high_medium_medium(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Medium", value=value))
        self.declare(Explanation(rule_name="combo_77_high_high_medium_medium",
                                  reason=f"lighting=high, blur=high, pose=medium, eye_open=medium -> Medium (value={value})"))

    @Rule(
        Label(name="lighting", label="high"),
        Label(name="blur", label="high"),
        Label(name="pose", label="medium"),
        Label(name="eye_open", label="high"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_78_high_high_medium_high(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="High", value=value))
        self.declare(Explanation(rule_name="combo_78_high_high_medium_high",
                                  reason=f"lighting=high, blur=high, pose=medium, eye_open=high -> High (value={value})"))

    @Rule(
        Label(name="lighting", label="high"),
        Label(name="blur", label="high"),
        Label(name="pose", label="high"),
        Label(name="eye_open", label="low"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_79_high_high_high_low(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Low", value=value))
        self.declare(Explanation(rule_name="combo_79_high_high_high_low",
                                  reason=f"lighting=high, blur=high, pose=high, eye_open=low -> Low (value={value})"))

    @Rule(
        Label(name="lighting", label="high"),
        Label(name="blur", label="high"),
        Label(name="pose", label="high"),
        Label(name="eye_open", label="medium"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_80_high_high_high_medium(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="High", value=value))
        self.declare(Explanation(rule_name="combo_80_high_high_high_medium",
                                  reason=f"lighting=high, blur=high, pose=high, eye_open=medium -> High (value={value})"))

    @Rule(
        Label(name="lighting", label="high"),
        Label(name="blur", label="high"),
        Label(name="pose", label="high"),
        Label(name="eye_open", label="high"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
    )
    def combo_81_high_high_high_high(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="High", value=value))
        self.declare(Explanation(rule_name="combo_81_high_high_high_high",
                                  reason=f"lighting=high, blur=high, pose=high, eye_open=high -> High (value={value})"))