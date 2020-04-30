import csv
import pytz
import dateutil.parser
from django.core.management.base import BaseCommand
from e_shop_app.models import Product, Promotion, ProductPromotion, Order, Customer, Vendor, OrderLine, Commission


class Command(BaseCommand):
    help = 'Script to automatically load the CSV \
        data into a relational database'

    def add_arguments(self, parser):
        parser.add_argument(
            'files_path',
            type=str,
            help='csv name to load into database'
        )

    def handle(self, *args, **options):
        files_path = options['files_path']

        commissions_csv = f'{files_path}/commissions.csv'
        order_lines_csv = f'{files_path}/order_lines.csv'
        orders_csv = f'{files_path}/orders.csv'
        product_promotions_csv = f'{files_path}/product_promotions.csv'
        products_csv = f'{files_path}/products.csv'
        promotions_csv = f'{files_path}/promotions.csv'

        Product.objects.all().delete()
        Promotion.objects.all().delete()
        ProductPromotion.objects.all().delete()
        Order.objects.all().delete()
        Customer.objects.all().delete()
        Vendor.objects.all().delete()
        OrderLine.objects.all().delete()
        Commission.objects.all().delete()

        with open(products_csv) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            products = []

            for row in csv_reader:
                line_count += 1
                if line_count > 1:
                    products.append(Product(
                        id=row[0],
                        description=row[1]
                    ))
            Product.objects.bulk_create(products)

        with open(promotions_csv) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            promotions = []

            for row in csv_reader:
                line_count += 1
                if line_count > 1:
                    promotions.append(Promotion(
                        id=row[0],
                        description=row[1]
                    ))
            Promotion.objects.bulk_create(promotions)

        with open(product_promotions_csv) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            product_promotions = []

            for row in csv_reader:
                line_count += 1
                if line_count > 1:
                    product_promotions.append(ProductPromotion(
                        date=dateutil.parser.parse(row[0]).astimezone(pytz.UTC),
                        product_id=Product.objects.get(id=row[1]),
                        promotion_id=Promotion.objects.get(id=row[2])
                    ))
            ProductPromotion.objects.bulk_create(product_promotions)

        with open(commissions_csv) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            commissions = []

            for row in csv_reader:
                line_count += 1
                if line_count > 1:
                    Vendor.objects.get_or_create(id=row[1])
                    commissions.append(Commission(
                        date=dateutil.parser.parse(row[0]).astimezone(pytz.UTC),
                        vendor_id=Vendor.objects.get(id=row[1]),
                        rate=row[2]
                    ))
            Commission.objects.bulk_create(commissions)

        with open(orders_csv) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            orders = []

            for row in csv_reader:
                line_count += 1
                if line_count > 1:
                    created_at = dateutil.parser.parse(row[1]).astimezone(pytz.UTC)
                    Vendor.objects.get_or_create(id=row[2])
                    Customer.objects.get_or_create(id=row[3])
                    commission = Commission.objects.get(date__date=created_at.date(), vendor_id=row[2])
                    orders.append(Order(
                        id=row[0],
                        created_at=created_at,
                        vendor_id=Vendor.objects.get(id=row[2]),
                        customer_id=Customer.objects.get(id=row[3]),
                        commission_rate=commission.rate
                    ))
            Order.objects.bulk_create(orders)

        with open(order_lines_csv) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            order_lines = []

            for row in csv_reader:
                line_count += 1
                if line_count > 1:

                    order_lines.append(OrderLine(
                        order_id=Order.objects.get(id=row[0]),
                        product_id=Product.objects.get(id=row[1]),
                        product_description=row[2],
                        product_price=row[3],
                        product_vat_rate=row[4],
                        discount_rate=row[5],
                        quantity=row[6],
                        full_price_amount=row[7],
                        discounted_amount=row[8],
                        vat_amount=row[9],
                        total_amount=row[10]
                    ))

            OrderLine.objects.bulk_create(order_lines)

        return 'All products added to database!'
