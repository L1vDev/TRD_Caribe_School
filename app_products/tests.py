from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .models import Category, Products

class CategoryModelTest(TestCase):
    def test_create_category_valid(self):
        cat = Category.objects.create(name="Electrónica")
        self.assertEqual(Category.objects.count(), 1)

    def test_category_name_is_correct(self):
        cat = Category.objects.create(name="Electrónica")
        self.assertEqual(cat.name, "Electrónica")

    def test_create_category_duplicate_name(self):
        Category.objects.create(name="Electrónica")
        with self.assertRaises(IntegrityError):
            Category.objects.create(name="Electrónica")

    def test_update_category(self):
        cat = Category.objects.create(name="Electrónica")
        cat.name = "Electrodomésticos"
        cat.save()
        cat.refresh_from_db()
        self.assertEqual(cat.name, "Electrodomésticos")

    def test_delete_category(self):
        cat = Category.objects.create(name="Electrónica")
        cat.delete()
        self.assertEqual(Category.objects.count(), 0)

    def test_create_category_empty_name(self):
        cat = Category(name="")
        with self.assertRaises(ValidationError):
            cat.full_clean()

class ProductsModelTest(TestCase):
    def setUp(self):
        self.cat1 = Category.objects.create(name="Electrónica")
        self.cat2 = Category.objects.create(name="Hogar")

    def test_create_product_valid(self):
        prod = Products.objects.create(
            name="Televisor",
            canon_name="televisor",
            price=1000.00,
            discount=10.00,
            stock=5,
            available=True
        )
        self.assertEqual(Products.objects.count(), 1)

    def test_product_name_is_correct(self):
        prod = Products.objects.create(
            name="Televisor",
            canon_name="televisor",
            price=1000.00,
            discount=10.00,
            stock=5,
            available=True
        )
        self.assertEqual(prod.name, "Televisor")

    def test_product_price_is_correct(self):
        prod = Products.objects.create(
            name="Televisor",
            canon_name="televisor",
            price=1000.00,
            discount=10.00,
            stock=5,
            available=True
        )
        self.assertEqual(prod.price, 1000.00)

    def test_product_discount_is_correct(self):
        prod = Products.objects.create(
            name="Televisor",
            canon_name="televisor",
            price=1000.00,
            discount=10.00,
            stock=5,
            available=True
        )
        self.assertEqual(prod.discount, 10.00)

    def test_product_category_add(self):
        prod = Products.objects.create(
            name="Televisor",
            canon_name="televisor",
            price=1000.00,
            discount=10.00,
            stock=5,
            available=True
        )
        prod.category.add(self.cat1, self.cat2)
        self.assertEqual(prod.category.count(), 2)

    def test_create_product_negative_price(self):
        prod = Products(
            name="Radio",
            canon_name="radio",
            price=-50.00,
            discount=5.00,
            stock=2,
            available=True
        )
        with self.assertRaises(ValidationError):
            prod.full_clean()

    def test_create_product_discount_above_100(self):
        prod = Products(
            name="Laptop",
            canon_name="laptop",
            price=2000.00,
            discount=150.00,
            stock=3,
            available=True
        )
        with self.assertRaises(ValidationError):
            prod.full_clean()

    def test_update_product_price(self):
        prod = Products.objects.create(
            name="Tablet",
            canon_name="tablet",
            price=500.00,
            discount=5.00,
            stock=10,
            available=True
        )
        prod.price = 450.00
        prod.save()
        prod.refresh_from_db()
        self.assertEqual(prod.price, 450.00)

    def test_update_product_discount(self):
        prod = Products.objects.create(
            name="Tablet",
            canon_name="tablet",
            price=500.00,
            discount=5.00,
            stock=10,
            available=True
        )
        prod.discount = 20.00
        prod.save()
        prod.refresh_from_db()
        self.assertEqual(prod.discount, 20.00)

    def test_delete_product(self):
        prod = Products.objects.create(
            name="Auriculares",
            canon_name="auriculares",
            price=100.00,
            discount=0.00,
            stock=15,
            available=True
        )
        prod.delete()
        self.assertEqual(Products.objects.count(), 0)

    def test_create_product_missing_required_fields(self):
        prod = Products(
            canon_name="sin_nombre",
            price=100.00,
            discount=0.00,
            stock=1,
            available=True
        )
        with self.assertRaises(ValidationError):
            prod.full_clean()

    def test_product_category_add_cat1(self):
        prod = Products.objects.create(
            name="Cafetera",
            canon_name="cafetera",
            price=300.00,
            discount=15.00,
            stock=7,
            available=True
        )
        prod.category.add(self.cat1)
        self.assertIn(self.cat1, prod.category.all())

    def test_product_category_not_in_cat2(self):
        prod = Products.objects.create(
            name="Cafetera",
            canon_name="cafetera",
            price=300.00,
            discount=15.00,
            stock=7,
            available=True
        )
        prod.category.add(self.cat1)
        self.assertNotIn(self.cat2, prod.category.all())