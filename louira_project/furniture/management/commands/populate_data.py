from django.core.management.base import BaseCommand
from furniture.models import Collection, FurnitureItem, NewsArticle, CompanyInfo
from django.utils import timezone


class Command(BaseCommand):
    help = "Populate the database with sample data"

    def handle(self, *args, **options):
        # Create Company Info
        company_info, created = CompanyInfo.objects.get_or_create(
            company_name="LOUIRA",
            defaults={
                "tagline": "Luxury Egyptian Furniture Excellence",
                "about_text": "We design, manufacture and distribute high-end Made in Egypt furniture all over the world.",
                "founder_quote": "I am really proud to carry on the family business and continue the tradition of Egyptian craftsmanship.",
                "address": "Furniture Manufacturing District, Damietta, Egypt",
                "phone": "+20 XXX XXX XXXX",
                "email": "info@louira.com",
                "opening_hours": "Saturday to Thursday: 8:00 AM - 6:00 PM",
            },
        )

        # Create Collections
        collections_data = [
            {
                "name": "Masterpiece Collection",
                "description": "Exquisite handcrafted pieces that represent the pinnacle of luxury furniture design.",
                "featured": True,
            },
            {
                "name": "Luxury Living",
                "description": "Elegant sofas, armchairs, consoles, and bookcases designed for sophisticated living spaces.",
                "featured": True,
            },
            {
                "name": "Dining Excellence",
                "description": "Magnificent dining tables, chairs, and sideboards crafted for memorable gatherings.",
                "featured": False,
            },
            {
                "name": "Bedroom Sanctuary",
                "description": "Luxurious beds, wardrobes, and bedroom furniture for ultimate comfort and style.",
                "featured": True,
            },
            {
                "name": "Executive Office",
                "description": "Professional office furniture that combines functionality with elegance.",
                "featured": False,
            },
            {
                "name": "Artistic Accents",
                "description": "Decorative pieces, lighting, and accessories for luxury interior spaces.",
                "featured": False,
            },
        ]

        for collection_data in collections_data:
            collection, created = Collection.objects.get_or_create(
                name=collection_data["name"], defaults=collection_data
            )
            if created:
                self.stdout.write(f"Created collection: {collection.name}")

        # Create News Articles
        news_data = [
            {
                "title": "Discover the artistry of LOUIRA",
                "slug": "discover-artistry-louira",
                "content": "From bespoke classic furniture to innovative design solutions, explore our latest masterpieces...",
                "excerpt": "From bespoke classic furniture to innovative design solutions, explore our latest masterpieces...",
                "author": "LOUIRA Team",
                "featured": True,
            },
            {
                "title": "New Collection Launch",
                "slug": "new-collection-launch",
                "content": "Introducing our latest collection featuring precious materials and innovative craftsmanship...",
                "excerpt": "Introducing our latest collection featuring precious materials and innovative craftsmanship...",
                "author": "Design Team",
                "featured": True,
            },
            {
                "title": "The Psychology of Luxury",
                "slug": "psychology-of-luxury",
                "content": "Explore the motivations, emotions, and perceptions that drive luxury furniture design...",
                "excerpt": "Explore the motivations, emotions, and perceptions that drive luxury furniture design...",
                "author": "Research Team",
                "featured": True,
            },
        ]

        for news_item in news_data:
            article, created = NewsArticle.objects.get_or_create(
                slug=news_item["slug"], defaults=news_item
            )
            if created:
                self.stdout.write(f"Created news article: {article.title}")

        self.stdout.write(
            self.style.SUCCESS("Successfully populated database with sample data")
        )
