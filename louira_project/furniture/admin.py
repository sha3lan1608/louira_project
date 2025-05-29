# admin.py - Insert this in your Django app's admin.py file
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Collection,
    FurnitureItem,
    GalleryImage,
    NewsArticle,
    Project,
    ContactInquiry,
    CompanyInfo,
)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["name", "featured", "created_at", "item_count"]
    list_filter = ["featured", "created_at"]
    search_fields = ["name", "description"]
    list_editable = ["featured"]

    def item_count(self, obj):
        return obj.items.count()

    item_count.short_description = "Items"


class GalleryImageInline(admin.TabularInline):
    model = FurnitureItem.gallery_images.through
    extra = 1


@admin.register(FurnitureItem)
class FurnitureItemAdmin(admin.ModelAdmin):
    list_display = ["name", "collection", "category", "price", "featured", "is_bespoke"]
    list_filter = ["collection", "category", "featured", "is_bespoke", "created_at"]
    search_fields = ["name", "description", "materials"]
    list_editable = ["featured", "price"]
    inlines = [GalleryImageInline]

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("name", "collection", "category", "description")},
        ),
        ("Details", {"fields": ("materials", "dimensions", "price", "is_bespoke")}),
        ("Media", {"fields": ("image",)}),
        ("Settings", {"fields": ("featured",)}),
    )


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ["alt_text", "image_preview"]
    search_fields = ["alt_text"]

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover;" />',
                obj.image.url,
            )
        return "No Image"

    image_preview.short_description = "Preview"


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "published_date", "featured"]
    list_filter = ["featured", "published_date"]
    search_fields = ["title", "content"]
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ["featured"]
    date_hierarchy = "published_date"

    fieldsets = (
        ("Article Information", {"fields": ("title", "slug", "author")}),
        ("Content", {"fields": ("excerpt", "content")}),
        ("Media", {"fields": ("image",)}),
        ("Publishing", {"fields": ("published_date", "featured")}),
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["title", "project_type", "location", "completion_date", "featured"]
    list_filter = ["project_type", "featured", "completion_date"]
    search_fields = ["title", "description", "location"]
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ["featured"]
    date_hierarchy = "completion_date"


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ["full_name", "email", "subject", "created_at", "replied"]
    list_filter = ["subject", "replied", "created_at"]
    search_fields = ["first_name", "last_name", "email", "message"]
    list_editable = ["replied"]
    readonly_fields = ["created_at"]
    date_hierarchy = "created_at"

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    full_name.short_description = "Name"

    fieldsets = (
        (
            "Contact Information",
            {"fields": ("first_name", "last_name", "email", "phone")},
        ),
        ("Inquiry Details", {"fields": ("subject", "message")}),
        ("Status", {"fields": ("replied", "created_at")}),
    )


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Basic Information",
            {"fields": ("company_name", "tagline", "about_text", "founder_quote")},
        ),
        ("Contact Details", {"fields": ("address", "phone", "email", "opening_hours")}),
        (
            "Social Media",
            {
                "fields": (
                    "social_facebook",
                    "social_instagram",
                    "social_twitter",
                    "social_pinterest",
                )
            },
        ),
    )

    def has_add_permission(self, request):
        # Only allow one company info object
        return not CompanyInfo.objects.exists()


# Customize admin site
admin.site.site_header = "LOUIRA Administration"
admin.site.site_title = "LOUIRA Admin"
admin.site.index_title = "Welcome to LOUIRA Administration"
