import argparse
import json
import requests
import re

def main():
	# Parse predictor argument
	arg_par = argparse.ArgumentParser()
	arg_par.add_argument("-j", "--json", required=True,
			help="path to facial json of actions")
	args = vars(arg_par.parse_args())
	try:
		with open(args["json"], 'r') as f:
			data = f.read()
	except IOError as e:
		print(e)
	except Exception as e:
		print("Failed: ", e)

	obj = json.loads(data)

	# print(obj)

	agents = obj["agents"]

	events = {}

	for agent in agents:
		# print("agent: ", agent)
		# print("events: ", events)
		if agent["type"] == "HTTPRequestAgent":
			http_request_agent(events, agent)
			
		elif agent["type"] == "PrintAgent":
			print_agent(events, agent)


def http_request_agent(events, agent):
	url = agent["options"]["url"]
	url = options_interpolate(events, url)

	req = requests.get(url)
	response = json.loads(req.text)
	# print("response: ", response)
	events[agent["name"]] = response

def print_agent(events, agent):
	message = agent["options"]["message"]

	message = options_interpolate(events, message)
	print(message)
	return


def options_interpolate(events, str):
	# print("events: ", events, "\n")
	between_brackets = [p.split('}}')[0] for p in str.split('{{') if '}}' in p]
	# print("between_brackets!!!!!!: ", between_brackets)
	f_string_values = []
	if len(between_brackets) > 0:
		for value in between_brackets:
			value = value.replace(".", "[", 1)
			value = value.replace(".", "][")
			f_string_values.append(value + "]")
		# print("f_string_values: ", f_string_values)
		# print("1 str: ", str)
		for f_str in f_string_values:
			regex = '\{{.*?\}}'
			str = re.sub(regex, "{" + f_str + "}", str, 1)
		
		# print("2 str: ", str, "\n")

		str = str.format_map(events)
		# print("str: ", str)

	return str


if __name__ == "__main__":
	main()
