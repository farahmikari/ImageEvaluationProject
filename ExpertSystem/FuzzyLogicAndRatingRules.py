from experta import *
from Facts import *
from fuzzy_layer import compute_memberships

class FuzzyLogicAndRatingRules(KnowledgeEngine):

# -----Fact Initial---------------------------------------------------------------------------------------------
    @DefFacts()
    def initial_facts(self):
        yield Fact(system="FuzzyLogicAndRatingRules", stage="start")
#-------------------------------------------------------------------------------------------
    @Rule(AS.sc << Score(name=MATCH.n, value=MATCH.v),NOT(Membership(name=MATCH.n)),salience=300 )
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

# ---------------------------------------------------------------------------

if __name__ == "__main__":
    examples = [
        dict(lighting=85, blur=90, pose=88, eye_open=92),
        dict(lighting=50, blur=55, pose=48, eye_open=60),
        dict(lighting=80, blur=85, pose=90, eye_open=20),
        dict(lighting=40, blur=95, pose=90, eye_open=95),
    ]

    for i, ex in enumerate(examples, 1):
        print(f"\n=== Example {i}: {ex} ===")
        engine = FuzzyLogicAndRatingRules()
        engine.reset()
        for criterion, value in ex.items():
            engine.declare(Score(name=criterion, value=float(value)))
        engine.run()