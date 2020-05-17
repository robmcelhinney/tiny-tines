import argparse
import json
import requests
import re


def main():
	# Parse predictor argument
	arg_par = argparse.ArgumentParser()
	arg_par.add_argument("-j", "--json", required=True,
			help="path to json file")
	args = vars(arg_par.parse_args())
	tines(args)


def tines(args):
	try:
		with open(args["json"], 'r') as f:
			data = f.read()
	except IOError as e:
		return "IOError. Error reading file."
	except Exception as e:
		print("Failed: ", e)
		return

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


def interpolate_option(events, option_str):
	# Create array of values that are surrounded by '{{' '}}'
	bracket_values = [p.split('}}')[0] for p in option_str.split('{{') if '}}' in p]

	# If values are surrounded by brackets enter
	if len(bracket_values) > 0:
		converted_values = convert_dot_paran(bracket_values)
		option_str = add_conv_back(converted_values, option_str, events)

	return option_str


def convert_dot_paran(bracket_values):
	# Convert dot notation to parantheses
	converted_values = []
	for value in bracket_values:
		value = value.split(".")

		converted_values.append(value)
	return converted_values


def add_conv_back(converted_values, option_str, events):
	# Loop through converted_values and replace originals one at a time
	# regex to find two starting brackets, anything inbetween, and two ending brackets.
	regex = '\{{[^{]*?\}}'
	for conv_value in converted_values:
		# get value pair from events, if it exists.
		temp = events
		for key in conv_value:
			try:
				temp = temp[key]
			except KeyError as ke:
				# print("KeyError ke: ", ke)
				temp = ""
				break
		temp = str(temp)

		# Substitute first {{value}} with {conv_value}
		option_str = re.sub(regex, temp, option_str, 1)
	return option_str

if __name__ == "__main__":
	main()
