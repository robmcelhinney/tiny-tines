import argparse
import json
import requests
import re

class FormatValue():
    def __format__(self, spec):
        return ""
    def __getitem__(self, name):
        # handle further nested item access
        return self

class formatting_dict(dict):
    def __getitem__(self, name):
        value = self.get(name)
		
        if isinstance(value, dict):
            # rewrap nested dictionaries to handle missing nested keys
            value = type(self)(value)
        return value if value is not None else FormatValue()

def main():
	# Parse predictor argument
	arg_par = argparse.ArgumentParser()
	arg_par.add_argument("-j", "--json", required=True,
			help="path to facial json of actions")
	args = vars(arg_par.parse_args())
	tines(args)


def tines(args):
	try:
		with open(args["json"], 'r') as f:
			data = f.read()
	except IOError as e:
		print(e)
	except Exception as e:
		print("Failed: ", e)

	try:
		obj = json.loads(data)
	except ValueError:
		print("Failed to decode json.")
		return
	events = {}

	for agent in obj["agents"]:
		if agent["type"] == "HTTPRequestAgent":
			http_request_agent(events, agent)
			
		elif agent["type"] == "PrintAgent":
			print_agent(events, agent)


def http_request_agent(events, agent):
	url = agent["options"]["url"]
	url = interpolate_option(events, url)

	try:
		res = requests.get(url)
	except requests.ConnectionError:
		print("failed to connect to url: ", url)
		return
	except Exception as e:
		print("Could not connect to url")
		return
	if not res.ok:
		print(f'status code: {res.status_code} outside of 2xx range')
		return

	try:
		res_text = json.loads(res.text)
	except ValueError:
		print("Failed to decode json.")
		return
	events[agent["name"]] = res_text

def print_agent(events, agent):
	message = agent["options"]["message"]
	message = interpolate_option(events, message)
	print(message)
	return


def interpolate_option(events, str):
	# Create array of values that are surrounded by '{{' '}}'
	bracket_values = [p.split('}}')[0] for p in str.split('{{') if '}}' in p]

	# If values are surrounded by brackets enter
	if len(bracket_values) > 0:
		converted_values = convert_dot_paran(bracket_values)
		str = add_conv_back(converted_values, str)

		print("interpolate_option str: ", str)

		# Use f strings to replace converted value with
		str = str.format_map(formatting_dict(events))
		
		# Need to escape any left over double parantheses so that it 
		# remains printed as is.
		str = escape_brackets(str)

	return str


def convert_dot_paran(bracket_values):
	# Convert dot notation to parantheses
	converted_values = []
	for value in bracket_values:
		value = value.replace(".", "[", 1)
		value = value.replace(".", "][")

		converted_values.append(value + "]")
	return converted_values


def add_conv_back(converted_values, str):
	# Loop through converted_values and replace originals one at a time
	regex = '\{{[^{]*?\}}'
	for conv_value in converted_values:
		# Substitute first {{value}} with {conv_value}
		str = re.sub(regex, "{" + conv_value + "}", str, 1)
	return str


def escape_brackets(str):
	# Add extra starting/closing bracket to any group of one or more 
	# starting/closing bracket
	start_matches = []
	def repl_start(m):
		start_matches.append(m.group())
		return ("{}{}").format(m.group(), "{")

	close_matches = []
	def repl_close(m):
		close_matches.append(m.group())
		return ("{}{}").format(m.group(), "}")

	# Escape starting brackets
	pattern = re.compile(r'\{{1,}')
	str = re.sub(pattern, repl_start, str)

	# Escape closing brackets
	pattern = re.compile(r'\}{1,}')
	str = re.sub(pattern, repl_close, str)

	return str


if __name__ == "__main__":
	main()
