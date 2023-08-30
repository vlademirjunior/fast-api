from pydantic import BaseModel

class CustomBaseModel(BaseModel):
    # Deprecated
    def dict(self, *args, **kwargs):
        d = super().dict(self, *args, **kwargs)
        d = {k: v for k, v in d.items() if v is not None}
        return d