from fastapi_pagination.bases import AbstractPage, AbstractParams, Optional
from typing import Any, TypeVar, Generic, Sequence
from fastapi_pagination import Params

T = TypeVar("T")


# Herdar os atributos da AbstractPage com T para poder especificar o tipo qualquer de basemodel para custom entender
class CustomPage(AbstractPage[T], Generic[T]):
    current_page: int
    items_per_page: int
    total: int
    # Sequencia de um tipo generico, que é o mesmo tipo basemodel response
    items: Sequence[T]

    __params_type__ = Params

    @classmethod
    def create(cls,
        items: Sequence[T],
        params: AbstractParams,
        *,
        total: Optional[int] = None,
        **kwargs: Any):
        return cls(items=items,
                   current_page=params.page,
                   items_per_page=params.size,
                   total=total,
                   **kwargs)  # cls é uma instancia da classe
