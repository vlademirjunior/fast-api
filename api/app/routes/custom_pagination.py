from fastapi_pagination.bases import AbstractPage, AbstractParams, RawParams, Optional
from typing import Any, TypeVar, Generic, Sequence
# from fastapi_pagination import Params
from pydantic import BaseModel
from fastapi import Query
from sqlalchemy.orm import Query as QuerySql
from fastapi_pagination.utils import verify_params

T = TypeVar("T")

class CustomParams(BaseModel, AbstractParams):
    current_page: int = Query(1, ge=1, description="Numero da Pagina")
    items_per_page: int = Query(1, ge=1, description="Numero da Pagina")

    def to_raw_params(self) -> RawParams:
        return RawParams(
            limit=self.items_per_page,
            offset=self.items_per_page * (self.current_page - 1)
        )

# Herdar os atributos da AbstractPage com T para poder especificar o tipo qualquer de basemodel para custom entender
class CustomPage(AbstractPage[T], Generic[T]):
    current_page: int
    items_per_page: int
    # Sequencia de um tipo generico, que é o mesmo tipo basemodel response
    items: Sequence[T]
    message: str

    # __params_type__ = Params
    __params_type__ = CustomParams

    @classmethod
    def create(cls,
        items: Sequence[T],
        params: AbstractParams,
        message: str,
        **kwargs: Any):

        # posso fazer algum tipo de validacao para vallidar se e uma instancia que estamos esperando ou qualquer outro processamento
        if not isinstance(params, CustomParams):
            raise ValueError("Pagina deve ser utilizada com parametros")

        kwargs['message'] = message
        
        return cls(items=items,
                   current_page=params.current_page,
                   items_per_page=params.items_per_page,
                   **kwargs)  # cls é uma instancia da classe


def paginate_query(query: T, params: AbstractParams) -> T:
    raw_params = params.to_raw_params().as_limit_offset()
    return query.limit(raw_params.limit).offset(raw_params.offset) # voce pode colocar -1 para um shift para baixo no filtro do banco aqui voce customiza sua paginacao

def custom_sqlalchemy_paginate(query: QuerySql[Any], params: Optional[AbstractParams] = None) -> Any:
    params, _ = verify_params(params, "limit-offset")

    items = paginate_query(query, params).all()

    return CustomPage.create(items=items, params=params, message = "Mensagem padrao por algum motivo")
