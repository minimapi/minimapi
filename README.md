# MinimAPI

MinimAPI is a simple dynamic API backend.
Just define your model.json, then your API is ready

See usage examples [here](https://github.com/minimapi/minimapi-examples)

## Install

With pip :

```bash
pip3 install minimapi
```


or build with :

```bash
python -m build
pip3 install dist/minimapi-*.whl
```


## Model format

Minimalistic data structure definition format for dynamic API backend and interface front

filename: model.json

Example :
```json
{
    "user": {
        "name": {"type": "text"},
        "birthday": {"type": "date"},
        "password": {"type": "password", "tags":["unlistable"]},
        "city": {"type": "foreign", "show": "name"}
    },
    "city": {
        "name": {"type": "text", "tags":["required"]},
        "code": {"type": "number"}
    }
}
```


Data parameters availables :
```
- type : data value type [required]
- show : culumn to show client side for foreign key
- tags : array of options
```


Currently supported types (based on inputs types):
```
- text
- number
- password
- date
- email
- url
- foreign (property name must match another table name, value is foreign data id)
```


Currently supported tags :
```
- unlistable : cannot be returned on bulk, replaced by dash in this case
- encrypted : for client side encrypted data, type checking disabled server side
- required : mandatory field
```

