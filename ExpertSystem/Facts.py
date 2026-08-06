import _compat_patch  # noqa: F401  (لازم قبل أي شي تاني)
from experta import KnowledgeEngine
from experta import *

class Score(Fact):
    name  = Field(str, mandatory=True)
    value = Field(float, mandatory=True)

class Membership(Fact):
    name   = Field(str, mandatory=True)
    low    = Field(float, mandatory=True)
    medium = Field(float, mandatory=True)
    high   = Field(float, mandatory=True)

class CriterionValue(Fact):
    name = Field(str, mandatory=True)
    value = Field(float, mandatory=True)
    weight = Field(float, mandatory=True)

class Label(Fact):
    name   = Field(str, mandatory=True)
    label  = Field(str, mandatory=True)
    value = Field(float, mandatory=True)

class Quality(Fact):
    label = Field(str, mandatory=True)
    value = Field(float, mandatory=True)

class BaseScore(Fact):
    value = Field(float, mandatory=True)

class Explanation(Fact):
    rule_name = Field(str, mandatory=True)
    reason    = Field(str, mandatory=True)

