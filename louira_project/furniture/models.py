from django.db import models
from django.urls import reverse
from django.utils import timezone


class Collection(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="collections/")
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("collection_detail", kwargs={"pk": self.pk})


class FurnitureItem(models.Model):
    CATEGORY_CHOICES = [
        ("living", "Living Room"),
        ("dining", "Dining Room"),
        ("bedroom", "Bedroom"),
        ("office", "Home Office"),
        ("decorative", "Decorative Objects"),
    ]

    name = models.CharField(max_length=200)
    collection = models.ForeignKey(
        Collection, on_delete=models.CASCADE, related_name="items"
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to="furniture/")
    gallery_images = models.ManyToManyField("GalleryImage", blank=True)
    materials = models.TextField()
    dimensions = models.CharField(max_length=200)
    is_bespoke = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.collection.name}"

    def get_absolute_url(self):
        return reverse("furniture_detail", kwargs={"pk": self.pk})


class GalleryImage(models.Model):
    image = models.ImageField(upload_to="gallery/")
    alt_text = models.CharField(max_length=200)

    def __str__(self):
        return self.alt_text


class NewsArticle(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=300)
    image = models.ImageField(upload_to="news/")
    author = models.CharField(max_length=100)
    published_date = models.DateTimeField(default=timezone.now)
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["-published_date"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("news_detail", kwargs={"slug": self.slug})


class Project(models.Model):
    PROJECT_TYPES = [
        ("residential", "Residential"),
        ("commercial", "Commercial"),
        ("hospitality", "Hospitality"),
        ("yacht", "Yacht"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPES)
    description = models.TextField()
    location = models.CharField(max_length=200)
    completion_date = models.DateField()
    main_image = models.ImageField(upload_to="projects/")
    gallery_images = models.ManyToManyField(GalleryImage, blank=True)
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["-completion_date"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("project_detail", kwargs={"slug": self.slug})


class ContactInquiry(models.Model):
    INQUIRY_TYPES = [
        ("general", "General Inquiry"),
        ("custom", "Custom Project"),
        ("collection", "Collection Information"),
        ("showroom", "Showroom Visit"),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=20, choices=INQUIRY_TYPES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    replied = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.subject}"


class CompanyInfo(models.Model):
    company_name = models.CharField(max_length=100, default="LOUIRA")
    tagline = models.CharField(max_length=200)
    about_text = models.TextField()
    founder_quote = models.TextField()
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    opening_hours = models.TextField()
    social_facebook = models.URLField(blank=True)
    social_instagram = models.URLField(blank=True)
    social_twitter = models.URLField(blank=True)
    social_pinterest = models.URLField(blank=True)

    class Meta:
        verbose_name = "Company Information"
        verbose_name_plural = "Company Information"

    def __str__(self):
        return self.company_name
