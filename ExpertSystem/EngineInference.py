import _compat_patch  # noqa: F401  (لازم قبل أي شي تاني)
from experta import*
from Facts import*
from fuzzy_layer import compute_memberships
from defuzzification import*

class EngineRules(KnowledgeEngine):

    @DefFacts()
    def initial_facts(self):
        yield Fact(system="RatingRules", stage="start")

    @Rule(Score(name=MATCH.n, value=MATCH.v),
        NOT(Membership(name=MATCH.n)),
        salience=300,
    )
    def fuzzify(self, n, v):
        deg = compute_memberships(v)
        self.declare(Membership(name=n, low=deg["low"], medium=deg["medium"], high=deg["high"],
        ))

    @Rule(
        NOT(Score(name="pose")),
        NOT(CriterionValue(name="pose")),
        salience=280,
    )
    def pose_undetected(self):
        self.declare(CriterionValue(name="pose", value=0.0, weight=0.0))
        self.declare(Label(name="pose", label="undetected", value=0.0))
        self.declare(Explanation(
            rule_name="pose_undetected",
            reason="no pose score - body not detected",
        ))

    @Rule(
        NOT(Score(name="eye_open")),
        NOT(CriterionValue(name="eye_open")),
        salience=280,
    )
    def eye_open_undetected(self):
        self.declare(CriterionValue(name="eye_open", value=0.0, weight=0.0))
        self.declare(Label(name="eye_open", label="undetected", value=0.0))
        self.declare(Explanation(
            rule_name="eye_open_undetected",
            reason="no eye_open score - eyes not detected",
        ))

    @Rule(
        Membership(name=MATCH.n, low=MATCH.l, medium=MATCH.m, high=MATCH.h),
        NOT(CriterionValue(name=MATCH.n)),
        salience=250,
    )
    def defuzzify_criterion(self, n, l, m, h):
        value = crisp_value_for_criterion(l, m, h);
        self.declare(CriterionValue( name=n, value=value,weight=weight_of(n)))
    @Rule(
        CriterionValue(name=MATCH.n, value=MATCH.v, weight=MATCH.w),
        NOT(Label(name=MATCH.n)),
        TEST(lambda w: w > 0),
        TEST(lambda v: v >= HIGH_MIN),
        salience=220,
    )
    def label_high(self, n, v):
        self.declare(Label(name=n, label="high", value=v))

    @Rule(
        CriterionValue(name=MATCH.n, value=MATCH.v, weight=MATCH.w),
        NOT(Label(name=MATCH.n)),
        TEST(lambda w: w > 0),
        TEST(lambda v: LOW_MAX <= v < HIGH_MIN),
        salience=220,
    )
    def label_medium(self, n, v):
        self.declare(Label(name=n, label="medium", value=v))

    @Rule(
        CriterionValue(name=MATCH.n, value=MATCH.v, weight=MATCH.w),
        NOT(Label(name=MATCH.n)),
        TEST(lambda w: w > 0),
        TEST(lambda v: v < LOW_MAX),
        salience=220,
    )
    def label_low(self, n, v):
        self.declare(Label(name=n, label="low", value=v))

    @Rule(
        CriterionValue(name="lighting", value=MATCH.lv, weight=MATCH.lw),
        CriterionValue(name="blur", value=MATCH.bv, weight=MATCH.bw),
        CriterionValue(name="pose", value=MATCH.pv, weight=MATCH.pw),
        CriterionValue(name="eye_open", value=MATCH.ev, weight=MATCH.ew),
        NOT(BaseScore()),
        salience=150,
    )
    def aggregate(self, lv, lw, bv, bw, pv, pw, ev, ew):
        self.declare(BaseScore(value=aggregate_score(
            lv, lw, bv, bw, pv, pw, ev, ew,)))

    @Rule(
        Label(name="blur", label="low", value=MATCH.bv),
        Label(name="lighting", label=MATCH.ll),
        Label(name="pose", label=MATCH.pl),
        Label(name="eye_open", label=MATCH.el),
        BaseScore(value=MATCH.base),
        NOT(Quality()),
        salience=110,
    )
    def veto_severe_blur(self, bv, ll, pl, el, base):
        self.declare(Quality(label="Low", value=base))
        self.declare(Explanation(
            rule_name="veto_severe_blur",
            reason=(f"lighting={ll}, blur=low({bv}), pose={pl}, eye_open={el} "
                    f"-> Low (value={base}) - blur : worst unusable regardless of other criteria"),
        ))

    @Rule(
        Label(name="eye_open", label="low", value=MATCH.ev),
        Label(name="lighting", label=MATCH.ll),
        Label(name="blur", label=MATCH.bl),
        Label(name="pose", label=MATCH.pl),
        BaseScore(value=MATCH.base),
        NOT(Quality()),
        salience=105,
    )
    def veto_closed_eyes(self, ev, ll, bl, pl, base):
        self.declare(Quality(label="Low", value=base))
        self.declare(Explanation(
            rule_name="veto_closed_eyes",
            reason=(f"lighting={ll}, blur={bl}, pose={pl}, eye_open=low({ev}) "
                    f"-> Low (value={base}) - eye: eyes are closed"),
        ))

    @Rule(
        Label(name="pose", label="low", value=MATCH.pv),
        Label(name="lighting", label=MATCH.ll),
        Label(name="blur", label=MATCH.bl),
        Label(name="eye_open", label=MATCH.el),
        BaseScore(value=MATCH.base),
        NOT(Quality()),
        salience=103,
    )
    def veto_pos(self, pv, ll, bl, el, base):
        self.declare(Quality(label="Low", value=base))
        self.declare(Explanation(
            rule_name="vetopos",
            reason=(f"lighting={ll}, blur={bl}, eye_open={el}, pos=low({pv}) "
                    f"-> Low (value={base}) - pos: worst position"),
        ))
    @Rule(
        BaseScore(value=MATCH.v),
        Label(name="lighting", label=MATCH.ll),
        Label(name="blur", label=MATCH.bl),
        Label(name="pose", label=MATCH.pl),
        Label(name="eye_open", label=MATCH.el),
        TEST(lambda v: v >= HIGH_MIN),
        NOT(Quality()),
        salience=50,
    )
    def quality_high(self, v, ll, bl, pl, el):
        self.declare(Quality(label="High", value=v))
        self.declare(Explanation(
            rule_name="quality_high",
            reason=(f"lighting={ll}, blur={bl}, pose={pl}, eye_open={el} "
                    f"-> High (value={v})"),
        ))

    @Rule(
        BaseScore(value=MATCH.v),
        Label(name="lighting", label=MATCH.ll),
        Label(name="blur", label=MATCH.bl),
        Label(name="pose", label=MATCH.pl),
        Label(name="eye_open", label=MATCH.el),
        TEST(lambda v: LOW_MAX <= v < HIGH_MIN),
        NOT(Quality()),
        salience=50,
    )
    def quality_medium(self, v, ll, bl, pl, el):
        self.declare(Quality(label="Medium", value=v))
        self.declare(Explanation(
            rule_name="quality_medium",
            reason=(f"lighting={ll}, blur={bl}, pose={pl}, eye_open={el} "
                    f"-> Medium (value={v})"),
        ))

    @Rule(
        BaseScore(value=MATCH.v),
        Label(name="lighting", label=MATCH.ll),
        Label(name="blur", label=MATCH.bl),
        Label(name="pose", label=MATCH.pl),
        Label(name="eye_open", label=MATCH.el),
        TEST(lambda v: v < LOW_MAX),
        NOT(Quality()),
        salience=50,
    )
    def quality_low(self, v, ll, bl, pl, el):
        self.declare(Quality(label="Low", value=v))
        self.declare(Explanation(
            rule_name="quality_low",
            reason=(f"lighting={ll}, blur={bl}, pose={pl}, eye_open={el} "
                    f"-> Low (value={v})"),
        ))
