# views.py - Insert this in your Django app's views.py file
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import (
    Collection,
    FurnitureItem,
    NewsArticle,
    Project,
    ContactInquiry,
    CompanyInfo,
)
from .forms import ContactForm


def home_view(request):
    """Homepage view with featured content"""
    context = {
        "featured_collections": Collection.objects.filter(featured=True)[:6],
        "latest_news": NewsArticle.objects.filter(featured=True)[:3],
        "featured_projects": Project.objects.filter(featured=True)[:3],
        "company_info": CompanyInfo.objects.first(),
    }
    return render(request, "index.html", context)


def collections_view(request):
    """All collections page"""
    collections = Collection.objects.all().order_by("name")
    paginator = Paginator(collections, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "collections": page_obj,
    }
    return render(request, "collections.html", context)


def collection_detail_view(request, pk):
    """Individual collection detail page"""
    collection = get_object_or_404(Collection, pk=pk)
    furniture_items = collection.items.all()

    # Filter by category if specified
    category = request.GET.get("category")
    if category:
        furniture_items = furniture_items.filter(category=category)

    context = {
        "collection": collection,
        "furniture_items": furniture_items,
        "categories": FurnitureItem.CATEGORY_CHOICES,
        "selected_category": category,
    }
    return render(request, "collection_detail.html", context)


def furniture_detail_view(request, pk):
    """Individual furniture item detail page"""
    furniture = get_object_or_404(FurnitureItem, pk=pk)
    related_items = FurnitureItem.objects.filter(
        collection=furniture.collection
    ).exclude(pk=pk)[:4]

    context = {
        "furniture": furniture,
        "related_items": related_items,
    }
    return render(request, "furniture_detail.html", context)


def news_view(request):
    """News listing page"""
    news_list = NewsArticle.objects.all()
    search = request.GET.get("search")

    if search:
        news_list = news_list.filter(
            Q(title__icontains=search) | Q(content__icontains=search)
        )

    paginator = Paginator(news_list, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "search": search,
        "featured_article": NewsArticle.objects.filter(featured=True).first(),
    }
    return render(request, "news.html", context)


def news_detail_view(request, slug):
    """Individual news article page"""
    article = get_object_or_404(NewsArticle, slug=slug)
    related_articles = NewsArticle.objects.exclude(slug=slug)[:3]

    context = {
        "article": article,
        "related_articles": related_articles,
    }
    return render(request, "news_detail.html", context)


def projects_view(request):
    """Projects listing page"""
    projects = Project.objects.all()
    project_type = request.GET.get("type")

    if project_type:
        projects = projects.filter(project_type=project_type)

    paginator = Paginator(projects, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "project_types": Project.PROJECT_TYPES,
        "selected_type": project_type,
    }
    return render(request, "projects.html", context)


def project_detail_view(request, slug):
    """Individual project detail page"""
    project = get_object_or_404(Project, slug=slug)
    related_projects = Project.objects.filter(
        project_type=project.project_type
    ).exclude(slug=slug)[:3]

    context = {
        "project": project,
        "related_projects": related_projects,
    }
    return render(request, "project_detail.html", context)


def company_view(request):
    """Company/About page"""
    company_info = CompanyInfo.objects.first()
    context = {
        "company_info": company_info,
    }
    return render(request, "company.html", context)


def contact_view(request):
    """Contact page with form handling"""
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the inquiry
            ContactInquiry.objects.create(
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                email=form.cleaned_data["email"],
                phone=form.cleaned_data["phone"],
                subject=form.cleaned_data["subject"],
                message=form.cleaned_data["message"],
            )
            messages.success(
                request, "Thank you for your message! We will get back to you soon."
            )
            return redirect("contact")
    else:
        form = ContactForm()

    company_info = CompanyInfo.objects.first()
    context = {
        "form": form,
        "company_info": company_info,
    }
    return render(request, "contact.html", context)


def search_view(request):
    """Global search functionality"""
    query = request.GET.get("q", "")
    results = []

    if query:
        # Search in collections
        collections = Collection.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

        # Search in furniture items
        furniture = FurnitureItem.objects.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(materials__icontains=query)
        )

        # Search in news
        news = NewsArticle.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

        # Search in projects
        projects = Project.objects.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(location__icontains=query)
        )

        results = {
            "collections": collections,
            "furniture": furniture,
            "news": news,
            "projects": projects,
            "total": collections.count()
            + furniture.count()
            + news.count()
            + projects.count(),
        }

    context = {
        "query": query,
        "results": results,
    }
    return render(request, "search_results.html", context)


# API Views for AJAX requests
from django.http import JsonResponse
from django.template.loader import render_to_string


def load_more_collections(request):
    """AJAX view to load more collections"""
    page = request.GET.get("page", 1)
    collections = Collection.objects.all()
    paginator = Paginator(collections, 6)
    page_obj = paginator.get_page(page)

    html = render_to_string(
        "partials/collection_cards.html",
        {
            "collections": page_obj,
        },
    )

    return JsonResponse(
        {
            "html": html,
            "has_next": page_obj.has_next(),
            "next_page": page_obj.next_page_number() if page_obj.has_next() else None,
        }
    )


def furniture_filter_ajax(request):
    """AJAX view for filtering furniture items"""
    collection_id = request.GET.get("collection_id")
    category = request.GET.get("category")

    furniture = FurnitureItem.objects.all()

    if collection_id:
        furniture = furniture.filter(collection_id=collection_id)

    if category:
        furniture = furniture.filter(category=category)

    html = render_to_string(
        "partials/furniture_cards.html",
        {
            "furniture_items": furniture,
        },
    )

    return JsonResponse({"html": html, "count": furniture.count()})
