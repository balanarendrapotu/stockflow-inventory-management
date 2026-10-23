from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Product
from .forms import ProductForm
from django.db.models import Q
from decimal import Decimal


@login_required
def dashboard(request):
    organization = request.user.organization

    products = Product.objects.filter(
        organization=organization
    )

    total_products = products.count()
    total_stock = sum(p.quantity for p in products)
    total_inventory_value = sum(
    (p.cost_price or Decimal("0.00")) * p.quantity
    for p in products)

    low_stock_products = [
        p for p in products
        if p.quantity <= (
            p.low_stock_threshold
            if p.low_stock_threshold is not None
            else 5
        )
    ]

    return render(
        request,
        "inventory/dashboard.html",
        {
            "total_products": total_products,
            "total_stock": total_stock,
            "low_stock_products": low_stock_products,
            "total_inventory_value": total_inventory_value,
        },
    )






@login_required
def product_list(request):
    products = Product.objects.filter(
        organization=request.user.organization
    )

    search_query = request.GET.get("search", "").strip()

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(sku__icontains=search_query)
        )

    return render(
        request,
        "inventory/product_list.html",
        {
            "products": products,
            "search_query": search_query,
        }
    )



@login_required
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)

        if form.is_valid():
            product = form.save(commit=False)
            product.organization = request.user.organization
            product.save()
            return redirect("product_list")
    else:
        form = ProductForm()

    return render(
        request,
        "inventory/product_form.html",
        {"form": form}
    )


@login_required
def product_edit(request, pk):
    product = get_object_or_404(
        Product,
        pk=pk,
        organization=request.user.organization
    )

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)

        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductForm(instance=product)

    return render(
        request,
        "inventory/product_form.html",
        {
            "form": form,
            "title": "Edit Product",
        }
    )


@login_required
def product_edit(request, pk):
    product = get_object_or_404(
        Product,
        pk=pk,
        organization=request.user.organization
    )

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)

        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductForm(instance=product)

    return render(
        request,
        "inventory/product_form.html",
        {"form": form}
    )



@login_required
def product_delete(request, pk):
    product = get_object_or_404(
        Product,
        pk=pk,
        organization=request.user.organization
    )

    if request.method == "POST":
        product.delete()
        return redirect("product_list")

    return render(
        request,
        "inventory/product_confirm_delete.html",
        {"product": product}
    )
