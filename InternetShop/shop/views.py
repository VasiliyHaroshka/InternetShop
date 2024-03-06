from django.shortcuts import render, get_object_or_404

from .models import Product, Category


def list_of_products(request, category_slug=None):
    """
    Return products with certain category.
    If there is no category, it will return all products.
    """
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        prodocts = products.filter(category=category)

    context = {
        "categories": categories,
        "category": category,
        "products": products,
    }

    return render(request, "shop/product_list.html", context=context)


def product_detail(request, id, slug):
    """Return certain product via id snd slug"""
    product = get_object_or_404(Product, is_available=True, id=id, slug=slug)
    context = {
        "product": product,
    }

    return render(request, "shop/product_detail.html", context=context)
