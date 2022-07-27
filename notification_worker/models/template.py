from pydantic import BaseModel


class Template(BaseModel):
    title: str
    code: str
    template_data: str
    subject: str
