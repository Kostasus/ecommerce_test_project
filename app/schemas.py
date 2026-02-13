from datetime import datetime
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CategoryCreate(BaseModel):
    """
    Модель для создания и обновления категории.
    Используется в POST и PUT запросах.
    """

    name: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Название категории (3-50 символов)",
    )
    parent_id: int | None = Field(
        None, description="ID родительской категории, если есть"
    )


class Category(BaseModel):
    """
    Модель для ответа с данными категории.
    Используется в GET-запросах.
    """

    id: int = Field(..., description="Уникальный идентификатор категории")
    name: str = Field(..., description="Название категории")
    parent_id: int | None = Field(
        None, description="ID родительской категории, если есть"
    )
    is_active: bool = Field(..., description="Активность категории")

    model_config = ConfigDict(from_attributes=True)


class ProductCreate(BaseModel):
    """
    Модель для создания и обновления товара.
    Используется в POST и PUT запросах.
    """

    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Название товара (3-100 символов)",
    )
    description: str | None = Field(
        None, max_length=500, description="Описание товара (до 500 символов)"
    )
    price: Decimal = Field(
        ..., gt=0, description="Цена товара (больше 0)", decimal_places=2
    )
    image_url: str | None = Field(
        None, max_length=200, description="URL изображения товара"
    )
    stock: int = Field(
        ..., ge=0, description="Количество товара на складе (0 или больше)"
    )
    category_id: int = Field(..., description="ID категории, к которой относится товар")


class Product(BaseModel):
    """
    Модель для ответа с данными товара.
    Используется в GET-запросах.
    """

    id: int = Field(..., description="Уникальный идентификатор товара")
    name: str = Field(..., description="Название товара")
    description: str | None = Field(None, description="Описание товара")
    price: Decimal = Field(
        ..., description="Цена товара в рублях", gt=0, decimal_places=2
    )
    image_url: str | None = Field(None, description="URL изображения товара")
    stock: int = Field(..., description="Количество товара на складе")
    category_id: int = Field(..., description="ID категории")
    is_active: bool = Field(..., description="Активность товара")

    model_config = ConfigDict(from_attributes=True)


class ProductList(BaseModel):
    """
    Список пагинации для товаров.
    """

    items: list[Product] = Field(description="Товары для текущей страницы")
    total: int = Field(ge=0, description="Общее количество товаров")
    page: int = Field(ge=1, description="Номер текущей страницы")
    page_size: int = Field(ge=1, description="Количество элементов на странице")

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    """
    Модель для создания пользователя
    """

    email: EmailStr = Field(description="Email пользователя")
    password: str = Field(min_length=8, description="Пароль (минимум 8 символов)")
    role: str = Field(
        default="buyer",
        pattern="^(buyer|seller|admin)$",
        description="Роль: 'buyer', 'seller' или 'admin'",
    )


class User(BaseModel):
    """
    Модель для ответа с данными пользователя
    """

    id: int
    email: EmailStr
    is_active: bool
    role: str
    model_config = ConfigDict(from_attributes=True)


class RefreshTokenRequest(BaseModel):
    """
    Модель для обновления refresh-токена
    """

    refresh_token: str


class ReviewCreate(BaseModel):
    """
    Модель для создания отзыва
    """

    product_id: Annotated[int, Field(description="Уникальный идентификатор товара")]
    comment: Annotated[str | None, Field(description="Отзыв о товаре")] = None
    grade: Annotated[int, Field(le=5, ge=1, description="Оценка товара")]


class Review(BaseModel):
    """
    Модель для ответа с данными отзыва
    """

    id: Annotated[int, Field(description="Уникальный идентификатор отзыва")]
    user_id: Annotated[int, Field(description="Уникальный идентификатор пользователя")]
    product_id: Annotated[int, Field(description="Уникальный идентификатор товара")]
    comment: Annotated[str | None, Field(description="Отзыв о товаре")] = None
    comment_date: Annotated[datetime, Field(description="Дата создания отзыва")]
    grade: Annotated[int, Field(description="Оценка товара")]
    is_active: Annotated[bool, Field(description="Признак активности отзыва")]

    model_config = ConfigDict(from_attributes=True)
