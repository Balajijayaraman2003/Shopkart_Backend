import os
from django.core.management.base import BaseCommand
from django.core.files import File
from ...models import ProductImages

class Command(BaseCommand):
    help = "Import all images from a specific directory into ProductImages model"

    def add_arguments(self, parser):
        parser.add_argument(
            "--directory",
            type=str,
            default=r"C:\Users\Balaji J\OneDrive\Pictures\Ecommerce",
            help="Path to the directory containing product images (default: Ecommerce folder)"
        )

    def handle(self, *args, **options):
        directory = options["directory"]

        if not os.path.isdir(directory):
            self.stderr.write(self.style.ERROR(f"{directory} is not a valid directory"))
            return

        image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]

        count = 0
        for root, _, files in os.walk(directory):  # recursive scan
            for filename in files:
                if any(filename.lower().endswith(ext) for ext in image_extensions):
                    filepath = os.path.join(root, filename)

                    # Avoid duplicates by checking filename
                    if ProductImages.objects.filter(image__icontains=filename).exists():
                        self.stdout.write(self.style.WARNING(f"Skipping duplicate: {filename}"))
                        continue

                    with open(filepath, "rb") as f:
                        product_image = ProductImages()
                        product_image.image.save(filename, File(f), save=True)
                        count += 1
                        self.stdout.write(self.style.SUCCESS(f"Imported: {filename}"))

        self.stdout.write(self.style.SUCCESS(f"Successfully imported {count} images"))