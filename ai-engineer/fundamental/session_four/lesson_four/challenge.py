from pydantic import Field, BaseModel, ValidationError


class Citation(BaseModel):
    source: str
    page: int = Field(ge=1)

class Answer(BaseModel):
    answer: str
    confidence: float = Field(ge=0, le=1)
    citations: list[Citation]

raw_json1 = '{"answer": "answer1", "confidence": 0.5, "citations": [{"source": "wikipedia", "page": 5}]}'
hasil = Answer.model_validate_json(raw_json1)
print(hasil)
print(type(hasil.citations[0]))
# 4 : mungkin type nya Citation ? karena citations refrensi list nya dari Citation


raw_json2 = '{"answer": "answer2", "confidence" : 2.4, "citations": [{"source": "stackoverflow", "page": 0}]}'
try:
    hasil2 = Answer.model_validate_json(raw_json2)
except ValidationError as e:
    print(e.error_count())
    print(e.errors())
# 5: seperti nya count error nya 2
# ini setelah saya run [{'type': 'less_than_equal', 'loc': ('confidence',), 'msg': 'Input should be less than or equal to 1', 'input': 2.4, 'ctx': {'le': 1.0}, 'url': 'https://err
# ors.pydantic.dev/2.14/v/less_than_equal'}, {'type': 'greater_than_equal', 'loc': ('citations', 0, 'page'), 'msg': 'Input should be greater than or equal to
# 1', 'input': 0, 'ctx': {'ge': 1}, 'url': 'https://errors.pydantic.dev/2.14/v/greater_than_equal'}]
