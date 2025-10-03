# Iran National ID
A lightweight Python utility for generating and validating Iranian national IDs with correct control digits.

## Features
- Generate valid national IDs (random or with custom city-code prefixes)
- Validate existing national IDs for control-digit correctness

## How the algorithm works
The utility implements the official control-digit checksum used in Iranian national IDs.
It multiplies each of the first 9 digits by a weight (10 down to 2), sums them, and checks the remainder against the control digit to ensure validity.

## Installation
Clone the repository:
```bash
git clone https://github.com/DevAmirSaman/iran-national-id
cd iran-national-id
```

## Usage
**Generate National IDs**
```python
from app.generator.generator import generate_national_id
from app.city_codes.city_codes import get_codes_for_city

# Generate 5 random valid IDs
ids = generate_national_id(quantity=5)
print(ids)  # list of valid IDs

# Generate with specific prefixes
ids = generate_national_id(city_code_prefixes=('001', '002'), quantity=3)
print(ids)

# Get codes for a specific city (example: Tehran)
prefixes = get_codes_for_city('تهران')
ids = generate_national_id(prefixes)
print(ids)
```
Note: for some reason the `city_code_prefixes` parameter except for a tuple.

**Validate National IDs**
```python
from app.generator.generator import generate_national_id
from app.validator.validator import is_national_id_valid

national_id = generate_national_id(quantity=1)[0]
print(is_national_id_valid(national_id)) # True
```

## License
MIT License – feel free to use it in your own projects.
