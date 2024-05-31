from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from .models import Product, Category
from .recommender import Recommender
from cart.forms import AddProductToCartForm


def product_list(request, category_slug=None):
    """
    Return products with certain category.
    If there is no category, it will return all products.
    """
    categories = Category.objects.all()
    category = None
    products = Product.objects.filter(is_available=True)

    if category_slug:
        language = request.LANGUAGE_CODE
        category = get_object_or_404(
            Category,
            translations__language_code=language,
            translations__slug=category_slug,
        )
        products = products.filter(category=category)

    paginator = Paginator(products, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "categories": categories,
        "category": category,
        "paginator": paginator,
        "page_obj": page_obj,
    }

    return render(request, "shop/product/product_list.html", context=context)


def product_detail(request, id, slug):
    """Return certain product via id snd slug (with recommend products)"""
    language = request.LANGUAGE_CODE
    product = get_object_or_404(
        Product,
        is_available=True,
        id=id,
        translations__language_code=language,
        translations__slug=slug,
    )
    cart_form = AddProductToCartForm()

    recommender = Recommender()
    recommend_products = recommender.suggest_products([product], 5)

    context = {
        "product": product,
        "cart_form": cart_form,
        "recommend_products": recommend_products,
    }

    return render(request, "shop/product/product_detail.html", context=context)
