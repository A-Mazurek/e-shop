from e_shop_app.models import OrderLine, Promotion
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Avg, Sum, Count, FloatField, Q
from statistics import mean
import dateutil.parser
import pytz
from decimal import Decimal


TWOPLACES = Decimal(10) ** -2


@api_view(['GET'])
def e_shop_day_summary(request, date):

    if request.method == 'GET':
        """
        endpoint requirements:

        1. The total number of items sold on that day.
        2. The total number of customers that made an order that day.
        3. The total amount of discount given that day.
        4. The average discount rate applied to the items sold that day.
        5. The average order total for that day
        6. The total amount of commissions generated that day.
        7. The average amount of commissions per order for that day.
        8. The total amount of commissions earned per promotion that day.
        """

        date = dateutil.parser.parse(date).astimezone(pytz.UTC)

        order_lines_on_day = OrderLine.objects.filter(order_id__created_at__date=date)

        order_total = []
        orders_id = [x for x in order_lines_on_day.values_list('order_id', flat=True).distinct()]
        for order_id in orders_id:
            order_total.append(list(order_lines_on_day.filter(
                order_id=order_id).aggregate(Avg('total_amount')).values())[0])

        promotions = {}
        promotions_q = Promotion.objects.all()
        for promotion in promotions_q:
            promotions[promotion.id] = \
                sum([(x.order_id.commission_rate * x.total_amount) for x in order_lines_on_day
                     if x.product_id.productpromotion_set.filter(
                        promotion_id_id=promotion.id)]).quantize(TWOPLACES)

        commissions_total = sum(list(promotions.values()))

        return Response({
            # 1 total number of items sold on that day.
            "items": sum(list(order_lines_on_day.values_list('quantity', flat=True))),
            # 2 total number of customers that made an order that day.
            "customers": order_lines_on_day.values_list('order_id__customer_id', flat=True).distinct().count(),
            # 3 total amount of discount given that day.
            "total_discount_amount": sum([x for x in order_lines_on_day.values_list('discounted_amount',
                                                                                    flat=True)]).quantize(TWOPLACES),
            # 4 average discount rate applied to the items sold that day.
            "discount_rate_avg": list(order_lines_on_day.aggregate(Avg('order_id__commission_rate'))
                                                                                    .values())[0].quantize(TWOPLACES),
            # 5 average order total for that day.
            "order_total_avg": mean(order_total).quantize(TWOPLACES),
            "commissions": {
                # 6 total amount of commissions generated that day.
                "total": commissions_total,
                # 7 average amount of commissions per order for that day.
                "order_average": (commissions_total/len(orders_id)).quantize(TWOPLACES),
                # 8 total amount of commissions earned per promotion that day.
                "promotions": promotions
            }
        })
