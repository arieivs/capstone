import os
import json
import pickle
import joblib
import pandas as pd
import custom_transformer
from flask import Flask, jsonify, request
from peewee import (
    SqliteDatabase, Model, IntegrityError,
    IntegerField, FloatField, TextField, BooleanField
)
from playhouse.db_url import connect
from datetime import date


##---   1. DESERIALIZE   ---###
with open(os.path.join('dev', 'columns.json')) as c_fd:
    columns = json.load(c_fd)

with open(os.path.join('dev', 'dtypes.pickle'), 'rb') as t_fd:
    dtypes = pickle.load(t_fd)

pipelineA = joblib.load(os.path.join('dev', 'pipelineA.pickle'))
pipelineB = joblib.load(os.path.join('dev', 'pipelineB.pickle'))


###---   2. DATABASE   ---###
DB = connect(os.environ.get('DATABASE_URL') or 'sqlite:///retailz.db')

class Product(Model):
    sku = IntegerField(unique=True)
    structure_level_4 = IntegerField()
    structure_level_3 = IntegerField()
    structure_level_2 = IntegerField()
    structure_level_1 = IntegerField()

    class Meta:
        database = DB

class Prediction(Model):
    sku = TextField()
    time_key = IntegerField()
    pvp_is_competitorA = FloatField()
    pvp_is_competitorB = FloatField()
    pvp_is_competitorA_actual = FloatField(null=True)
    pvp_is_competitorB_actual = FloatField(null=True)

    class Meta:
        database = DB
        # for sku-time_key pairs to be unique
        indexes = ((('sku', 'time_key'), True),)

DB.create_tables([Prediction], safe=True)


###---   3. APP   ---###
app = Flask(__name__)

# 3.1 Auxiliary functions for input validation
def validate_keys(payload, expected_keys):
    expected_keys_set = set(expected_keys)
    payload_keys_set = set(payload.keys())
    if (expected_keys_set - payload_keys_set) or (payload_keys_set - expected_keys_set):
        return {'error': f'Incorrect input. Expecting {', '.join(expected_keys)}.'}, False
    return payload, True
    
def validate_time_key(payload):
    if type(payload['time_key']) is not int:
        return {'error': f'Incorrect input. Expecting time key in %Y%m%d format as an integer.'}, False
    if len(str(payload['time_key'])) != 8:
        return {'error': f'Incorrect input. Expecting time key in %Y%m%d format.'}, False
    try:
        time_key_date = date.fromisoformat(str(payload['time_key']))
    except ValueError:
        return {'error': f'Incorrect input. Expecting time key in %Y%m%d format.'}, False
    # there is no interest in forecasting for dates previous to the training data (which starts at 2023-01-01)
    # nor too much ahead, as the accuracy won't be significant, thus until 5 years after the training data (which ends at 2024-10-31)
    start_date = date.fromisoformat("20230101")
    end_date = date.fromisoformat("20291031")
    if time_key_date < start_date or time_key_date > end_date:
        return {'error': f'Incorrect input. A date from {start_date} to {end_date} is expected.'}, False
    return payload, True

def validate_sku(payload):
    # sku are company specific
    # on training data there are skus from 1128 to 4735... let's keep it between 1000 and 4999
    if type(payload['sku']) is not str:
        return {'error': 'Incorrect input. SKU must be a numeric code as a string.'}, False
    start_sku = 1000
    end_sku = 4999
    try:
        sku_int = int(payload['sku'])
    except ValueError:
        return {'error': 'Incorrect input. SKU must be a numeric code as a string.'}, False
    if sku_int < start_sku or sku_int > end_sku:
        return {'error': f'Incorrect input. SKU must be a numeric code from {start_sku} to {end_sku}.'}, False
    return payload, True

def validate_pvp(payload):
    if (type(payload['pvp_is_competitorA_actual']) is not float and type(payload['pvp_is_competitorA_actual']) is not int) \
        or (type(payload['pvp_is_competitorB_actual']) is not float and type(payload['pvp_is_competitorB_actual']) is not int):
        return {'error': 'Incorrect input. PVP must be a float.'}, False
    try:
        payload['pvp_is_competitorA_actual'] = float(payload['pvp_is_competitorA_actual'])
        payload['pvp_is_competitorB_actual'] = float(payload['pvp_is_competitorB_actual'])
    except ValueError:
        return {'error': 'Incorrect input. PVP must be a float.'}, False
    if payload['pvp_is_competitorA_actual'] < 0 or payload['pvp_is_competitorB_actual'] < 0:
        return {'error': 'Incorrect input. PVP must be a positive float.'}, False
    return payload, True

def validate_payload_forecast(payload):
    expected_keys = ['sku', 'time_key']
    response, is_valid = validate_keys(payload, expected_keys)
    if not is_valid:
        return response, is_valid
    response, is_valid = validate_time_key(response)
    if not is_valid:
        return response, is_valid
    response, is_valid = validate_sku(response)
    if not is_valid:
        return response, is_valid
    return response, True

def validate_payload_actual(payload):
    expected_keys = ['sku', 'time_key', 'pvp_is_competitorA_actual', 'pvp_is_competitorB_actual']
    response, is_valid = validate_keys(payload, expected_keys)
    if not is_valid:
        return response, is_valid
    response, is_valid = validate_time_key(response)
    if not is_valid:
        return response, is_valid
    response, is_valid = validate_sku(response)
    if not is_valid:
        return response, is_valid
    response, is_valid = validate_pvp(response)
    if not is_valid:
        return response, is_valid
    return response, True

# 3.2 Forecast Prices Endpoint
""" Input:
{
    "sku": <string>,
    "time_key": <integer>,
}
Output:
{
    "sku": <string>,
    "time_key": <integer>,
    "pvp_is_competitorA": <double>,
    "pvp_is_competitorB": <double>,
}
Input data incorrectly formatted -> return a response with HTTP status code 422.
Pairs of product identifiers and dates should be unique. """

@app.route('/forecast_prices/', methods=['POST'])
def forecast_prices():
    # get input
    payload = request.get_json()

    # verify input
    response, is_valid = validate_payload_forecast(payload)
    if not is_valid:
        return jsonify(response), 422

    # verify it's a new sku, time_key pair
    try:
        prediction_obj = Prediction.get(sku=response['sku'], time_key=response['time_key'])
        return jsonify({'error': "There's already an entry for this product-date pair."}), 422
    except Prediction.DoesNotExist:
        pass

    # predict
    product_obj = Product.get(sku=response['sku'])
    prediction_body = response.copy()
    try:
        prediction_body['structure_level_2'] = product_obj.structure_level_2
    except Product.DoesNotExist:
        # TO THINK - another option is simply to say this SKU is unknown and return an error
        prediction_body['structure_level_2'] = 0
    prediction_df = pd.DataFrame([prediction_body], columns=columns).astype(dtypes)
    pvp_is_competitorA = pipelineA.predict(prediction_df)[0]
    pvp_is_competitorB = pipelineB.predict(prediction_df)[0]

    # store in database
    prediction = Prediction(sku=response['sku'], time_key=response['time_key'], pvp_is_competitorA=pvp_is_competitorA, pvp_is_competitorB=pvp_is_competitorB)
    try:
        prediction.save()
    # contingency plan
    except IntegrityError:
        DB.rollback()
        return jsonify({'error': "There's already an entry for this product-date pair."}), 422
    
    # return a positive answer (default HTTP code)
    response['pvp_is_competitorA'], response['pvp_is_competitorB'] = pvp_is_competitorA, pvp_is_competitorB
    return jsonify(response)

# 3.3 Actual prices endpoint
""" Input:
{
    "sku": <string>,
    "time_key": <integer>,
    "pvp_is_competitorA_actual": <double>,
    "pvp_is_competitorB_actual": <double>,
}
Output:
{
    "sku": <string>,
    "time_key": <integer>,
    "pvp_is_competitorA": <double>,
    "pvp_is_competitorB": <double>,
    "pvp_is_competitorA_actual": <double>,
    "pvp_is_competitorB_actual": <double>,
}
If product-date pair is not in the local database or is incorrectly formatted -> return a response with HTTP status code 422."""

@app.route('/actual_prices/', methods=['POST'])
def actual_prices():
    # get input
    payload = request.get_json()

    # verify input
    response, is_valid = validate_payload_actual(payload)
    if not is_valid:
        return jsonify(response), 422

    # update the database
    try:
        prediction_obj = Prediction.get(sku=response['sku'], time_key=response['time_key'])
        prediction_obj.pvp_is_competitorA_actual = response['pvp_is_competitorA_actual']
        prediction_obj.pvp_is_competitorB_actual = response['pvp_is_competitorB_actual']
        prediction_obj.save()

    except Prediction.DoesNotExist:
        return jsonify({'error': f"No entry in the database for product {response['sku']} on {response['time_key']}."}), 422
    
    # return a positive answer (default HTTP code)
    response['pvp_is_competitorA'] = prediction_obj.pvp_is_competitorA
    response['pvp_is_competitorB'] = prediction_obj.pvp_is_competitorB
    return jsonify(response)


# 3.X Run the App
# Important to add host='0.0.0.0' (or a specific IP if the app is running on a fixed IP)
# else one cannot reach it from the outside
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)
