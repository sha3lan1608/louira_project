from django.urls import path
from . import views

app_name = "louira"

urlpatterns = [
    # Main pages
    path("", views.home_view, name="home"),
    path("company/", views.company_view, name="company"),
    path("contact/", views.contact_view, name="contact"),
    path("search/", views.search_view, name="search"),
    # Collections
    path("collections/", views.collections_view, name="collections"),
    path(
        "collections/<int:pk>/", views.collection_detail_view, name="collection_detail"
    ),
    # Furniture
    path("furniture/<int:pk>/", views.furniture_detail_view, name="furniture_detail"),
    # News
    path("news/", views.news_view, name="news"),
    path("news/<slug:slug>/", views.news_detail_view, name="news_detail"),
    # Projects
    path("projects/", views.projects_view, name="projects"),
    path("projects/<slug:slug>/", views.project_detail_view, name="project_detail"),
    # AJAX endpoints
    path(
        "ajax/collections/", views.load_more_collections, name="load_more_collections"
    ),
    path(
        "ajax/furniture-filter/", views.furniture_filter_ajax, name="furniture_filter"
    ),
]
