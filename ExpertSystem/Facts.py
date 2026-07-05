from experta import *

#الدرجة الابتدائية الخاصة بكل معيار
class Score(Fact):
    name  = Field(str, mandatory=True)   # 'lighting' | 'blur' | 'pose' | 'eye_open'
    value = Field(float, mandatory=True)

#تصنيفات الدرجة الموجودة
class Membership(Fact):
    name   = Field(str, mandatory=True)
    low    = Field(float, mandatory=True)
    medium = Field(float, mandatory=True)
    high   = Field(float, mandatory=True)

#  قيمة الانتماء الخاصة بكل فئة للتصنيفات
class Label(Fact):
    name   = Field(str, mandatory=True)
    label  = Field(str, mandatory=True)     # 'low' | 'medium' | 'high'
    degree = Field(float, mandatory=True)   # its winning membership degree

# الدرجة النهائسة والدرجة الجودة المستحقة للصورة
class Quality(Fact):
    label = Field(str, mandatory=True)      # 'Low' | 'Medium' | 'High'
    value = Field(float, mandatory=True)     # 0-100 representative score

#تقديم سبب مقنع لدرجة النهائية
class Explanation(Fact):
    rule_name = Field(str, mandatory=True)
    reason    = Field(str, mandatory=True)