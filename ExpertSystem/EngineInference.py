from experta import *
from Facts import *
from fuzzy_layer import compute_memberships
from defuzzification import final_quality_value

class EngineRules(KnowledgeEngine):

# -----Fact Initial---------------------------------------------------------------------------------------------
    @DefFacts()
    def initial_facts(self):
        yield Fact(system="FuzzyLogicAndRatingRules", stage="start")
#-------------------------------------------------------------------------------------------
    @Rule(AS.sc << Score(name=MATCH.n, value=MATCH.v),
          NOT(Membership(name=MATCH.n)),
          salience=300 )
    def fuzzify(self, sc, n, v):
        deg = compute_memberships(v)
        self.declare(Membership(name=n, low=deg["low"], medium=deg["medium"], high=deg["high"]))

#كان هناك قيمة انتماء ال high  عالية
    @Rule(AS.mb << Membership(name=MATCH.n, high=MATCH.h, medium=MATCH.m, low=MATCH.l),
        NOT(Label(name=MATCH.n)),
        TEST(lambda h: h > 0),TEST(lambda h, m: h >= m),TEST(lambda h, l: h >= l),salience=203)
    def labelHigh(self, mb, n, h):
        self.declare(Label(name=n, label="high", degree=h))

# كان هناك قيمة انتماء ال medium  عالية
    @Rule( AS.mb << Membership(name=MATCH.n, high=MATCH.h, medium=MATCH.m, low=MATCH.l),
        NOT(Label(name=MATCH.n)),
        TEST(lambda m: m > 0),TEST(lambda m, h: m >= h), TEST(lambda m, l: m >= l),salience=202)
    def labelMedium(self, mb, n, m):
        self.declare(Label(name=n, label="medium", degree=m))

 # كان هناك قيمة انتماء ال low  عالية
    @Rule(AS.mb << Membership(name=MATCH.n, high=MATCH.h, medium=MATCH.m, low=MATCH.l),
        NOT(Label(name=MATCH.n)),
        TEST(lambda l: l > 0),TEST(lambda l, h: l >= h),TEST(lambda l, m: l >= m), salience=201 )
    def labelLow(self, mb, n, l):
        self.declare(Label(name=n, label="low", degree=l))

#-------------------------------------------------------------------------------------
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


#-------------------------------------------------------------------------------------
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


#----------------------------------------------------------------------------------
ZERO_DEGS = {"low": 0.0, "medium": 0.0, "high": 0.0}
#حالات خاصة ناتجة عن السكور الأساسي
class UndetectedCasesRules(KnowledgeEngine):
    @Rule(NOT(Score(name="pose")),NOT(Label(name="pose")),salience=250,)
    def pose_undetected(self):
        self.declare(Label(name="pose", label="undetected", degree=1.0))
        self.declare(Explanation(rule_name="pose_undetected",reason="No Score fact for pose - body not detected in the image"))

    @Rule(NOT(Score(name="eye_open")),NOT(Label(name="eye_open")),salience=250,)
    def eye_open_undetected(self):
        self.declare(Label(name="eye_open", label="undetected", degree=1.0))
        self.declare(Explanation(rule_name="eye_open_undetected",reason="No Score fact for eye_open - eyes not detected in the image"))
#--------------------------------------------------------------------------------------------------------------
#اعطاء تصنيف  جودة للحالات الخاصة
# لا يوجد جسم لكن  يوجد عيون
    @Rule(Label(name="pose", label="undetected"),
        Label(name="eye_open", label=MATCH.el),
        TEST(lambda el: el != "undetected"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="eye_open", low=MATCH.el2, medium=MATCH.em2, high=MATCH.eh2),
        NOT(Quality()),
        salience=100,
    )
    def value_pose_undetected(self, ll, lm, lh, bl, bm, bh, el2, em2, eh2):
        lighting_degs = {"low": ll, "medium": lm, "high": lh}
        blur_degs = {"low": bl, "medium": bm, "high": bh}
        eye_degs = {"low": el2, "medium": em2, "high": eh2}
        value = final_quality_value(lighting_degs, blur_degs, ZERO_DEGS, eye_degs, pose_weight=0)
        self.declare(QualityCandidate(value=value, source="pose_undetected"))
    @Rule(
        Label(name ="eye_open", label="undetected"),
        Label(name="pose", label=MATCH.pl),
        TEST(lambda pl: pl != "undetected"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl2, medium=MATCH.pm2, high=MATCH.ph2),
        NOT(Quality()),
        salience=100,
    )
    def value_eye_undetected(self, ll, lm, lh, bl, bm, bh, pl2, pm2, ph2):
        lighting_degs = {"low": ll, "medium": lm, "high": lh}
        blur_degs = {"low": bl, "medium": bm, "high": bh}
        pose_degs = {"low": pl2, "medium": pm2, "high": ph2}
        value = final_quality_value(lighting_degs, blur_degs, pose_degs, ZERO_DEGS, eye_weight=0)
        self.declare(QualityCandidate(value=value, source="eye_undetected"))

    @Rule(
        Label(name="pose", label="undetected"),
        Label(name="eye_open", label="undetected"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        NOT(Quality()),
        salience=100,
    )
    def value_both_undetected(self, ll, lm, lh, bl, bm, bh):
        lighting_degs = {"low": ll, "medium": lm, "high": lh}
        blur_degs = {"low": bl, "medium": bm, "high": bh}
        value = final_quality_value(lighting_degs, blur_degs, ZERO_DEGS, ZERO_DEGS,
         pose_weight=0, eye_weight=0)
        self.declare(QualityCandidate(value=value, source="both_undetected"))


#------------------------------------------------------------------------------------
    #تتصنيف الجودة للحالات الخاصة
    @Rule(
        AS.cand << QualityCandidate(value=MATCH.v, source=MATCH.src),
        TEST(lambda v: v >= 75),
        NOT(Quality()),
        salience=50,
    )
    def candidate_high(self, cand, v, src):
        self.declare(Quality(label="High", value=v))
        self.declare(Explanation(rule_name=f"threshold_high_{src}", reason=f"value={v} >= 75"))

    @Rule(
        AS.cand << QualityCandidate(value=MATCH.v, source=MATCH.src),
        TEST(lambda v: 45 <= v < 75),
        NOT(Quality()),
        salience=50,
    )
    def candidate_medium(self, cand, v, src):
        self.declare(Quality(label="Medium", value=v))
        self.declare(Explanation(rule_name=f"threshold_medium_{src}", reason=f"45 <= value={v} < 75"))

    @Rule(
        AS.cand << QualityCandidate(value=MATCH.v, source=MATCH.src),
        TEST(lambda v: v < 45),
        NOT(Quality()),
        salience=50,
    )
    def candidate_low(self, cand, v, src):
        self.declare(Quality(label="Low", value=v))
        self.declare(Explanation(rule_name=f"threshold_low_{src}", reason=f"value={v} < 45"))

#------------------------------------------------------------------------
# مشاكل عدم تطابق للحذف ع الاغلب هي قاعدة
    @Rule(
        Label(name="lighting"),
        Label(name="blur"),
        Label(name="pose"),
        Label(name="eye_open"),
        Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
        Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
        Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
        Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
        NOT(Quality()),
        salience=-1000,
    )
    def default_fallback(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
        value = final_quality_value(
            {"low": ll, "medium": lm, "high": lh},
            {"low": bl, "medium": bm, "high": bh},
            {"low": pl, "medium": pm, "high": ph},
            {"low": el, "medium": em, "high": eh},
        )
        self.declare(Quality(label="Medium", value=value))
        self.declare(Explanation(
            rule_name="default_fallback",
            reason="No specific combination rule matched (should not normally happen)"))