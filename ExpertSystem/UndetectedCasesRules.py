# from experta import KnowledgeEngine, Rule, NOT, MATCH, TEST, AS
# from Facts import Score, Label, Membership, Quality, QualityCandidate, Explanation
# from defuzzification import final_quality_value
# DEGS_FIELDS = ("low", "medium", "high")
# ZERO_DEGS = {"low": 0.0, "medium": 0.0, "high": 0.0}
# #حالات خاصة ناتجة عن السكور الأساسي
# class UndetectedCasesRules(KnowledgeEngine):
#     @Rule(NOT(Score(name="pose")),NOT(Label(name="pose")),salience=250,)
#     def pose_undetected(self):
#         self.declare(Label(name="pose", label="undetected", degree=1.0))
#         self.declare(Explanation(rule_name="pose_undetected",reason="No Score fact for pose - body not detected in the image"))
#
#     @Rule(NOT(Score(name="eye_open")),NOT(Label(name="eye_open")),salience=250,)
#     def eye_open_undetected(self):
#         self.declare(Label(name="eye_open", label="undetected", degree=1.0))
#         self.declare(Explanation(rule_name="eye_open_undetected",reason="No Score fact for eye_open - eyes not detected in the image"))
# #--------------------------------------------------------------------------------------------------------------
# #اعطاء تصنيف  جودة للحالات الخاصة
# # لا يوجد جسم لكن  يوجد عيون
#     @Rule(Label(name="pose", label="undetected"),
#         Label(name="eye_open", label=MATCH.el),
#         TEST(lambda el: el != "undetected"),
#         Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
#         Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
#         Membership(name="eye_open", low=MATCH.el2, medium=MATCH.em2, high=MATCH.eh2),
#         NOT(Quality()),
#         salience=100,
#     )
#     def value_pose_undetected(self, ll, lm, lh, bl, bm, bh, el2, em2, eh2):
#         lighting_degs = {"low": ll, "medium": lm, "high": lh}
#         blur_degs = {"low": bl, "medium": bm, "high": bh}
#         eye_degs = {"low": el2, "medium": em2, "high": eh2}
#         value = final_quality_value(lighting_degs, blur_degs, ZERO_DEGS, eye_degs, pose_weight=0)
#         self.declare(QualityCandidate(value=value, source="pose_undetected"))
#     @Rule(
#         Label(name ="eye_open", label="undetected"),
#         Label(name="pose", label=MATCH.pl),
#         TEST(lambda pl: pl != "undetected"),
#         Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
#         Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
#         Membership(name="pose", low=MATCH.pl2, medium=MATCH.pm2, high=MATCH.ph2),
#         NOT(Quality()),
#         salience=100,
#     )
#     def value_eye_undetected(self, ll, lm, lh, bl, bm, bh, pl2, pm2, ph2):
#         lighting_degs = {"low": ll, "medium": lm, "high": lh}
#         blur_degs = {"low": bl, "medium": bm, "high": bh}
#         pose_degs = {"low": pl2, "medium": pm2, "high": ph2}
#         value = final_quality_value(lighting_degs, blur_degs, pose_degs, ZERO_DEGS, eye_weight=0)
#         self.declare(QualityCandidate(value=value, source="eye_undetected"))
#
#     @Rule(
#         Label(name="pose", label="undetected"),
#         Label(name="eye_open", label="undetected"),
#         Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
#         Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
#         NOT(Quality()),
#         salience=100,
#     )
#     def value_both_undetected(self, ll, lm, lh, bl, bm, bh):
#         lighting_degs = {"low": ll, "medium": lm, "high": lh}
#         blur_degs = {"low": bl, "medium": bm, "high": bh}
#         value = final_quality_value(lighting_degs, blur_degs, ZERO_DEGS, ZERO_DEGS,
#          pose_weight=0, eye_weight=0)
#         self.declare(QualityCandidate(value=value, source="both_undetected"))
#
#
# #------------------------------------------------------------------------------------
#     #تتصنيف الجودة للحالات الخاصة
#     @Rule(
#         AS.cand << QualityCandidate(value=MATCH.v, source=MATCH.src),
#         TEST(lambda v: v >= 75),
#         NOT(Quality()),
#         salience=50,
#     )
#     def candidate_high(self, cand, v, src):
#         self.declare(Quality(label="High", value=v))
#         self.declare(Explanation(rule_name=f"threshold_high_{src}", reason=f"value={v} >= 75"))
#
#     @Rule(
#         AS.cand << QualityCandidate(value=MATCH.v, source=MATCH.src),
#         TEST(lambda v: 45 <= v < 75),
#         NOT(Quality()),
#         salience=50,
#     )
#     def candidate_medium(self, cand, v, src):
#         self.declare(Quality(label="Medium", value=v))
#         self.declare(Explanation(rule_name=f"threshold_medium_{src}", reason=f"45 <= value={v} < 75"))
#
#     @Rule(
#         AS.cand << QualityCandidate(value=MATCH.v, source=MATCH.src),
#         TEST(lambda v: v < 45),
#         NOT(Quality()),
#         salience=50,
#     )
#     def candidate_low(self, cand, v, src):
#         self.declare(Quality(label="Low", value=v))
#         self.declare(Explanation(rule_name=f"threshold_low_{src}", reason=f"value={v} < 45"))
#
# #------------------------------------------------------------------------
# # مشاكل عدم تطابق للحذف ع الاغلب هي قاعدة
#     @Rule(
#         Label(name="lighting"),
#         Label(name="blur"),
#         Label(name="pose"),
#         Label(name="eye_open"),
#         Membership(name="lighting", low=MATCH.ll, medium=MATCH.lm, high=MATCH.lh),
#         Membership(name="blur", low=MATCH.bl, medium=MATCH.bm, high=MATCH.bh),
#         Membership(name="pose", low=MATCH.pl, medium=MATCH.pm, high=MATCH.ph),
#         Membership(name="eye_open", low=MATCH.el, medium=MATCH.em, high=MATCH.eh),
#         NOT(Quality()),
#         salience=-1000,
#     )
#     def default_fallback(self, ll, lm, lh, bl, bm, bh, pl, pm, ph, el, em, eh):
#         value = final_quality_value(
#             {"low": ll, "medium": lm, "high": lh},
#             {"low": bl, "medium": bm, "high": bh},
#             {"low": pl, "medium": pm, "high": ph},
#             {"low": el, "medium": em, "high": eh},
#         )
#         self.declare(Quality(label="Medium", value=value))
#         self.declare(Explanation(
#             rule_name="default_fallback",
#             reason="No specific combination rule matched (should not normally happen)"))