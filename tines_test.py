'''Unit test for tines.py
'''

import unittest
import tines

class Tines(unittest.TestCase):
    events = {}
    events['location'] = {'ip': '89.126.4.253', 'success': True, 'type': 'IPv4', 'continent': 'Europe', 'continent_code': 'EU', 'country': 'Ireland', 'country_code': 'IE', 'country_flag': 'https://cdn.ipwhois.io/flags/ie.svg', 'country_capital': 'Dublin', 'country_phone': '+353', 'country_neighbours': 'GB', 'region': 'County Galway', 'city': 'Tuam', 'latitude': '53.5141156', 'longitude': '-8.8565177', 'asn': 'AS25441', 'org': 'IBIS', 'isp': 'Imagine Communications Group Limited', 'timezone': 'Europe/Dublin', 'timezone_name': 'Greenwich Mean Time', 'timezone_dstOffset': '0', 'timezone_gmtOffset': '0', 'timezone_gmt': 'GMT 0:00', 'currency': 'Euro', 'currency_code': 'EUR', 'currency_symbol': '€', 'currency_rates': '0.924078', 'currency_plural': 'euros', 'completed_requests': 83}
    events['sunset'] = {'results': {'sunrise': '12:22:00 AM', 'sunset': '4:22:39 PM', 'solar_noon': '8:22:20 AM', 'day_length': '16:00:39', 'civil_twilight_begin': '11:36:46 PM', 'civil_twilight_end': '5:07:54 PM', 'nautical_twilight_begin': '10:31:27 PM', 'nautical_twilight_end': '6:13:13 PM', 'astronomical_twilight_begin': '12:00:01 AM', 'astronomical_twilight_end': '12:00:01 AM'}, 'status': 'OK'}
    events["foo"] = { "bar": "World" }
    
    options = (("https://www.robmcelhinney.com/?continent={{location.continent}}&money={{location.currency_plural}}", "https://www.robmcelhinney.com/?continent=Europe&money=euros"),
            ("https://www.robmcelhinney.com/?noon={{sunset.results.solar_noon}}&ipType={{location.type}}", "https://www.robmcelhinney.com/?noon=8:22:20 AM&ipType=IPv4"),
            ("Hello {{foo.bar}}!", "Hello World!"),
            ("Hello {{foo.bar}!", "Hello {{foo.bar}!"),
            ("Hello {{foo.bar}} }}!", "Hello World }}!"),
            ("Hello {{ {{foo.bar}}!", "Hello {{ World!"),
            ("Hello {{foo.qux}}!", "Hello !"))


    def test_interpolate_option(self):
        for option, result in self.options:
            result_inter = tines.interpolate_option(self.events, option)
            self.assertEqual(result, result_inter)


    bracket_values = ((["test.testing"], ["test[testing]"]),
                    (["dot.notation", "convert.me"], ["dot[notation]", "convert[me]"]))

    def test_convert_dot_paran(self):
        for value, result in self.bracket_values:
            parantheses_result = tines.convert_dot_paran(value)
            self.assertEqual(result, parantheses_result)

    converted_options = ((["test[testing]"], "domain/?a={{test.testing}}", "domain/?a={test[testing]}"),
            (["convert[me]", "dot[not]"], "domain/?a={{convert.me}}&b={{dot.not}}", "domain/?a={convert[me]}&b={dot[not]}"),
    )
    def test_add_conv_back(self):
        for conv_values, value_str, result in self.converted_options:
            conv_result = tines.add_conv_back(conv_values, value_str)
            self.assertEqual(result, conv_result)
   
    escape_brackets = (("{test}", "{{test}}"),
            ("test", "test"),
            ("{ test", "{{ test"),
            ("{ test }} }", "{{ test }}} }}"))

    def test_escape_brackets(self):
        for str, result in self.escape_brackets:
            result_escape = tines.escape_brackets(str)
            self.assertEqual(result, result_escape)


if __name__ == '__main__':
    unittest.main()
