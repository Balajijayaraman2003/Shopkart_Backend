from django.core.management.base import BaseCommand
from faker import Faker
from django.utils.text import slugify
import random
from ...models import Product  # Update with your actual app name

class Command(BaseCommand):
    help = 'Generate 100 fake product records'

    def handle(self, *args, **kwargs):
        fake = Faker()
        products = []

        for _ in range(100):
            name = fake.unique.word().capitalize()
            old_price = round(random.uniform(10000, 50000), 2)
            discount_percent = random.randint(5, 40)
            selling_price = round(old_price * (1 - discount_percent / 100), 2)

            product = Product(
                name=name,
                description=fake.paragraph(nb_sentences=3),
                short_description=fake.sentence(nb_words=8),
                old_price=old_price,
                selling_price=selling_price,
                rating=round(random.uniform(1.0, 5.0), 1),
                rating_count=random.randint(1, 500),
                category_id=1,  # Ensure category with ID 1 exists
                brand=fake.company(),
                slug=slugify(name),
                in_stock=random.choice([True, False]),
                stock_quantity=random.randint(0, 100),
                discount_percent=discount_percent
            )
            products.append(product)

        Product.objects.bulk_create(products)
        self.stdout.write(self.style.SUCCESS('✅ Successfully created 100 fake products'))