# Copyright (C) 2022  Vamsi Korada
#
# This file is part of sacumen test.
#
# This piece of is for creating json and env file out of flat dictionary
# data from input based on either of the following - yaml, cfg or conf
# Software Foundation 1.0 of the License
#

"""
Imported Libraries
"""
import os, sys, configparser, yaml, json
from collections.abc import MutableMapping

def cfg_conf_dict_convertor(input_file):
	"""
	Converts a cfg or a conf file to flat dictionary	
	"""
	try:
		config = configparser.ConfigParser()
		config.read(input_file)
		cfg_conf_dict = {}
		for section in config.sections():
			cfg_conf_dict[section] = {}
			for option in config.options(section):
				cfg_conf_dict[section][option] = config.get(section, option)
		cfg_conf_flat_dict = flat_dict_convertor(cfg_conf_dict)
		print(cfg_conf_flat_dict)
		return cfg_conf_flat_dict
	except:
		error = "invalid input data"
		print(error)
		return error

def yaml_dict_convertor(input_file):
	"""
	Converts a yaml file to flat dictionary	
	"""
	with open(input_file, 'r') as f:
		try:
			yaml_dict=yaml.safe_load(f)
			print(yaml_dict)
			yaml_flat_dict = flat_dict_convertor(yaml_dict)
			print(yaml_flat_dict)
			return yaml_flat_dict
			f.close()
		except:
			error = "invalid input data"
			print(error)
			return error
			
def flat_dict_convertor(d: MutableMapping, parent_key: str = '', sep: str ='_') -> MutableMapping:
	"""
	Converts nested dictionary to flat dictionary	
	"""
	items = []
	for k, v in d.items():
		new_key = parent_key + sep + k if parent_key else k
		if isinstance(v, MutableMapping):
			items.extend(flat_dict_convertor(v, new_key, sep=sep).items())
		else:
			items.append((new_key, v))
	return dict(items)

def main():
	"""
	Main routine used for converting cfg, conf, yaml files to flat dictionary
	and save them to an output json and env file. OS environment is also
	updated while creating the env file.
	
	Validates the incoming input file and throws error if no input is provided.
	Checks for only valid file type inputs to be accepted.
	Output json and env file naming based on input file name.	
	"""
	try:
		input_file = sys.argv[1]
	except:
		error = "missing input file info"
		print(error)
		return error
	else:
		input_file = input_file.strip()
		if os.path.exists(input_file):
			
			file_pattern = input_file.split(".")[-1]
			
			if file_pattern == 'cfg' or file_pattern == 'conf':
				output = cfg_conf_dict_convertor(input_file)
			elif file_pattern == 'yaml':
				output = yaml_dict_convertor(input_file)
			else:
				error = "invalid file type"
				print(error)
				return error	

			if output == 'invalid input data':
				print(output)
				return output
			else:
				file_prefix = os.path.splitext(os.path.basename(input_file))[0]
				output_json_file = file_prefix + ".json"
				output_env_file = file_prefix + ".env"
				
				json_obj = json.dumps(output, indent = 4) 
				with open(output_json_file, "w") as f:
					f.write(json_obj)
				f.close()
				
				with open(output_env_file, "w") as f:
					for key, val in output.items():
						f.write(f"{key}={val}\n")
						os.environ[key] = val
				f.close()
				
				output = "output json and env files created"
				print(output)
				return output
				
		else:
			error = "invalid file"
			print(error)
			return error

main()
