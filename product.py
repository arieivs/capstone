import os
import csv
from peewee import (
    SqliteDatabase, Model, IntegrityError,
    IntegerField, FloatField, TextField, BooleanField
)
from playhouse.db_url import connect


###---   DATABASE   ---###
DB = connect(os.environ.get('DATABASE_URL') or 'sqlite:///retailz.db')

# Create the table
class Product(Model):
    sku = IntegerField(unique=True)
    structure_level_4 = IntegerField()
    structure_level_3 = IntegerField()
    structure_level_2 = IntegerField()
    structure_level_1 = IntegerField()

    class Meta:
        database = DB

DB.create_tables([Product], safe=True)

# Fill the table with data
def fill_product_table():
    with open(os.path.join('dev', 'product_structures.csv')) as p_fd:
        csv_reader = csv.reader(p_fd, delimiter=',')
        # headers: sku,structure_level_4,structure_level_3,structure_level_2,structure_level_1
        next(csv_reader, None) # skip headers
        for row in csv_reader:
            product = Product(sku=row[0], structure_level_4=row[1], structure_level_3=row[2], structure_level_2=row[3], structure_level_1=row[4])
            try:
                product.save()
            except IntegrityError:
                DB.rollback()
                print("Error: There's already an entry for this product.")
    print("Product table filled in.")

fill_product_table()