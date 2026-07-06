from .utils import *
from .config import *
class FeatureNormalizer:
    def __init__(self):
        pass
    def normalize_scores(self, features):

     shoulder = self.normalize_shoulders(features["shoulders"])
     head = self.normalize_head(features["head"])
     hands = self.normalize_hands(features["hands"])
     hips = self.normalize_hips(features["hips"])
     legs = self.normalize_legs(features["legs"])
     body = self.normalize_body(features["body"])

     final_score = self.calculate_final_score([
        (shoulder,0.20),
        (head,0.15),
        (hands,0.10),
        (hips,0.20),
        (legs,0.20),
        (body,0.15)
    ])

     return final_score
    
    def calculate_final_score(self, scores):
     total_weight = 0
     weighted_sum = 0
     for result, weight in scores:
        if result["pose_score"] is None:
            continue
        weighted_sum += result["pose_score"] * weight
        total_weight += weight
     if total_weight == 0:
        return normalize_result(
            score=None,
            reason=EvaluationReason.NOT_VISIBLE
        )
     final_score = weighted_sum / total_weight
     return normalize_result(
        round(final_score,2)
    )

    def normalize_shoulders(self, shoulder):
        if not shoulder["both_visible"]:
            return normalize_result(
                score= None,
                valid= False,
                confidence=shoulder["confidence"],
                reason=EvaluationReason.NOT_VISIBLE
            )
        angle_score = normalize(shoulder["angle"],5,25)
        ratio_score = normalize(shoulder["difference_ratio"],0.01,0.20)
        final_score = weighted_average([(angle_score,0.5),(ratio_score,0.5)])
        return normalize_result(
        final_score,
        confidence=shoulder["confidence"]
        )

    def normalize_head(self, head):
      if not head["visible"]:
           return normalize_result(
            None,
            False,
            head["confidence"],
            EvaluationReason.NOT_VISIBLE
           )
      score = normalize(head["head_angle"],5,25)
      return normalize_result(
        score,
        confidence=head["confidence"]
      )

    def normalize_hands(self,hands):
     if hands["visibility_ratio"]==0:
        return normalize_result(
            None,
            False,
            hands["confidence"],
            EvaluationReason.NOT_VISIBLE
        )

     score = hands["visibility_ratio"]*100
     return normalize_result(
        round(score,2),
        confidence=hands["confidence"]
    )

    def normalize_hips(self,hips):
     if not hips["both_visible"]:
        return normalize_result(
            None,
            False,
            hips["confidence"],
            EvaluationReason.NOT_VISIBLE
        )
     angle_score = normalize(hips["angle"],5,25)
     ratio_score = normalize(hips["difference_ratio"],0.01,0.15)
     final_score = weighted_average([(angle_score,0.5),(ratio_score,0.5)])
     return normalize_result(
        final_score,
        confidence=hips["confidence"]
    )

    def normalize_legs(self,legs):
     if not legs["both_visible"]:
        return normalize_result(
            None,
            False,
            legs["confidence"],
            EvaluationReason.NOT_VISIBLE
        )
     left_score = normalize(legs["left_deviation"],2,25)
     right_score = normalize(legs["right_deviation"],2,25)
     final_score = weighted_average([(left_score,0.5),(right_score,0.5)])

     return normalize_result(
        final_score,
        confidence=legs["confidence"]

    )

    def normalize_body(self,body):
     if not body["visible"]:
        return normalize_result(
            None,
            False,
            body["confidence"],
            EvaluationReason.NOT_VISIBLE
        )

     torso_score = normalize(body["torso_angle"],3,20)
     offset_score = normalize(body["offset_ratio"],0.01,0.10)
     final_score = weighted_average([(torso_score,0.7),(offset_score,0.3)])

     return normalize_result(
        final_score,
        confidence=body["confidence"]
    )    
