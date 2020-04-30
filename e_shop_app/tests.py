from django.test import TestCase, Client
from django.core.management import call_command


class APITestCase(TestCase):
    def setUp(self):
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0')

        call_command('csv_load', 'dummy_data')

    def test_if_response_of_end_point_api_is_working_properly(self):
        # checking for incorrect url, it should be status 404
        error_response = self.client.get('api/summary/2019-08-01')
        self.assertEqual(error_response.status_code, 404)
        # checking for correct url, it should be status 200
        response = self.client.get('/api/summary/2019-08-01')
        self.assertEqual(response.status_code, 200)

    def test_if_json_of_end_point_api_contain_right_data(self):
        response = self.client.get('/api/summary/2019-08-01')
        json = response.json()

        # 1 total number of items sold on that day.
        self.assertEqual(json['items'], 6)

        # 2 total number of customers that made an order that day.
        self.assertEqual(json['customers'], 3)

        # 3 total amount of discount given that day.
        self.assertEqual(json['total_discount_amount'], 120.0)

        # 4 average discount rate applied to the items sold that day.
        self.assertEqual(json['discount_rate_avg'], 0.2)

        # 5 average order total for that day.
        self.assertEqual(json['order_total_avg'], 120)

        # 6 total amount of commissions generated that day.
        self.assertEqual(json['commissions']['total'], 144.0)

        # 7 average amount of commissions per order for that day.
        self.assertEqual(json['commissions']['order_average'], 48.0)

        # 8 total amount of commissions earned per promotion that day.
        self.assertEqual(json['commissions']['promotions']['1'], 44.0)
        self.assertEqual(json['commissions']['promotions']['2'], 48.0)
        self.assertEqual(json['commissions']['promotions']['3'], 52.0)
