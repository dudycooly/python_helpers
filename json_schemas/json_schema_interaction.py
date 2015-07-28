__author__ = 'jp'

from json_schema_generator import SchemaGenerator

input_file = "sample.json"
output_file = "sample.json_schema"

# Convert json to json schema
with open(input_file, 'r') as json_file:
    generator = SchemaGenerator.from_json(json_file.read())
    json_schema_data = generator.to_json(indent=4)

with open(output_file, 'w') as json_schema_file:
    json_schema_file.write(json_schema_data)

import json

with open("sample_ver_4.json_schema", 'r') as json_schema_file:
    json_schema_data = json.loads(json_schema_file.read())

# It generates json schema based on draft 3, if you want latest version use other tools
# Useful online tool to generate schema
# http://jsonschema.net/#/

# Create json schema objects

#Option 1
# import python_jsonschema_objects as pjs
# builder = pjs.ObjectBuilder(output_file)
# ns = builder.build_classes()

import warlock

Country = warlock.model_factory(json_schema_data)
print Country(address={"streetAddress": "21 2nd Street",
                       "city": "New York"},
              phoneNumber=[{"location": "home"}])
