from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Product


@login_required
def dashboard(request):
    organization = request.user.organization
    products = Product.objects.filter(organization=organization)

    total_products = products.count()
    total_stock = sum(p.quantity for p in products)

    low_stock_products = [
        p for p in products
        if p.quantity <= (
            p.low_stock_threshold
            if p.low_stock_threshold is not None
            else 5
        )
    ]

    return render(request, "inventory/dashboard.html", {
        "total_products": total_products,
        "total_stock": total_stock,
        "low_stock_products": low_stock_products,
    })