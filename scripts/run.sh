# Delete
python3 ./manage.py delete order
python3 ./manage.py delete customer
python3 ./manage.py delete product
python3 ./manage.py delete company

# Delete Again freshly
python3 ./manage.py delete order
python3 ./manage.py delete customer
python3 ./manage.py delete product
python3 ./manage.py delete company

# Read
python3 ./manage.py read product setpart
python3 ./manage.py read customer customer-update
python3 ./manage.py read order
python3 ./manage.py read company

# Sync
python3 ./manage.py sync product
python3 ./manage.py sync variant
python3 ./manage.py sync customer
python3 ./manage.py sync company
python3 ./manage.py sync order
