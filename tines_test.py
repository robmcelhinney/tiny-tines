'''Unit test for tines.py
'''

import unittest
import tines

class Tines(unittest.TestCase):
    events = {}
    events['location'] = {'ip': '89.126.4.253', 'success': True, 
            'type': 'IPv4', 'continent': 'Europe', 'continent_code': 'EU', 
            'country': 'Ireland', 'country_code': 'IE', 'country_flag': 
            'https://cdn.ipwhois.io/flags/ie.svg', 'country_capital': 
            'Dublin', 'country_phone': '+353', 'country_neighbours': 'GB', 
            'region': 'County Galway', 'city': 'Tuam', 'latitude': 
            '53.5141156', 'longitude': '-8.8565177',
            'currency': 'Euro', 'currency_code': 'EUR', 'currency_symbol': 
            '€', 'currency_rates': '0.924078', 'currency_plural': 'euros', 
            'completed_requests': 83}
    events['sunset'] = {'results': {'solar_noon': '8:22:20 AM'}, 
            'status': 'OK'}
    events["foo"] = {"bar": "World"}
    events["test"] = {"testing": "unit testing"}
    events["convert"] = {"me": "converted"}
    events["dot"] = {"not": "ation"}
    
    
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


    bracket_values = ((["test.testing"], [["test", "testing"]]),
                    (["dot.notation", "convert.me"], [["dot", "notation"], ["convert", "me"]]))
    def test_convert_dot_paran(self):
        for value, result in self.bracket_values:
            parantheses_result = tines.convert_dot_paran(value)
            self.assertEqual(result, parantheses_result)


    converted_options = (([['test', 'testing']], "domain/?a={{test.testing}}", "domain/?a=unit testing"),
            ([['convert', 'me'],["dot", "not"]], "domain/?a={{convert.me}}&b={{dot.not}}", "domain/?a=converted&b=ation"),
    )
    def test_add_conv_back(self):
        for conv_values, value_str, result in self.converted_options:
            conv_result = tines.add_conv_back(conv_values, value_str, 
                    self.events)
            self.assertEqual(result, conv_result)


    def test_fake_file(self):
        result = tines.tines({"json": "fake_file.json"})
        self.assertEqual("IOError. Error reading file.", result)


if __name__ == '__main__':
    unittest.main()
