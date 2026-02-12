from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from app.auth import get_current_buyer, get_current_user
from app.db_depends import get_async_db
from app.models.products import Product as ProductModel
from app.models.reviews import Review as ReviewModel
from app.models.users import User as UserModel
from app.schemas import Review as ReviewSchema
from app.schemas import ReviewCreate

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.get("/", response_model=list[ReviewSchema], status_code=status.HTTP_200_OK)
async def get_reviews(db: AsyncSession = Depends(get_async_db)):
    """
    Возвращает список всех активных отзывов
    """

    result = await db.scalars(select(ReviewModel).where(ReviewModel.is_active))
    reviews = result.all()
    return reviews


@router.get(
    "/{product_id}/reviews",
    response_model=list[ReviewSchema],
    status_code=status.HTTP_200_OK,
)
async def get_reviews_by_product(
    product_id: int, db: AsyncSession = Depends(get_async_db)
):
    """
    Возвращает список активных отзывов для указанного товара
    """

    result = await db.scalars(
        select(ProductModel).where(
            ProductModel.id == product_id, ProductModel.is_active
        )
    )

    product = result.first()

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found or inactive",
        )

    result = await db.scalars(
        select(ReviewModel).where(
            ReviewModel.product_id == product_id, ReviewModel.is_active
        )
    )
    reviews = result.all()
    return reviews


@router.post("/", response_model=ReviewSchema, status_code=status.HTTP_201_CREATED)
async def create_review(
    review: ReviewCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_buyer),
):
    """
    Создает новый отзыв для указанного товара
    """

    result = await db.scalars(
        select(ProductModel).where(
            ProductModel.id == review.product_id, ProductModel.is_active
        )
    )

    db_product = result.first()

    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found or inactive",
        )

    result = await db.scalars(
        select(ReviewModel).where(
            ReviewModel.product_id == db_product.id,
            ReviewModel.user_id == current_user.id,
        )
    )

    db_review = result.first()

    if db_review is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user review for this product already exists",
        )

    db_review = ReviewModel(**review.model_dump(), user_id=current_user.id)
    db.add(db_review)
    await db.commit()
    await db.refresh(db_review)
    await update_product_rating(db, review.product_id)
    return db_review


@router.delete(
    "/{review_id}", response_model=ReviewSchema, status_code=status.HTTP_200_OK
)
async def delete_review(
    review_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_user),
):
    result = await db.scalars(
        select(ReviewModel).where(ReviewModel.id == review_id, ReviewModel.is_active)
    )

    db_review = result.first()
    if db_review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Review not found or inactive"
        )

    if current_user.role == "admin" or current_user.id == db_review.user_id:
        db_review.is_active = False
        await db.commit()
        await db.refresh(db_review)
        await update_product_rating(db, db_review.product_id)
        return db_review

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="The user is not the author of the review or does not have the 'admin' role",
    )


async def update_product_rating(db: AsyncSession, product_id: int):
    result = await db.execute(
        select(func.avg(ReviewModel.grade)).where(
            ReviewModel.product_id == product_id, ReviewModel.is_active
        )
    )
    avg_rating = result.scalar() or 0.0
    product = await db.get(ProductModel, product_id)
    product.rating = avg_rating
    await db.commit()
