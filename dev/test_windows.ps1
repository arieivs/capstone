# FORECAST ENDPOINT
# correct
curl -Method POST -Uri http://localhost:5000/forecast_prices/ -ContentType 'application/json' -Body '{"sku": "2222", "time_key": 20250101}'
curl -Method POST -Uri http://localhost:5000/forecast_prices/ -ContentType 'application/json' -Body '{"sku": "2222", "time_key": 20250102}'
curl -Method POST -Uri http://localhost:5000/forecast_prices/ -ContentType 'application/json' -Body '{"sku": "2223", "time_key": 20250101}'
# incorrect keys
curl -Method POST -Uri http://localhost:5000/forecast_prices/ -ContentType 'application/json' -Body '{"sku": "2200", "time_key": 20250101, "extra": "extra"}'
curl -Method POST -Uri http://localhost:5000/forecast_prices/ -ContentType 'application/json' -Body '{"sku": "2200"}'
# incorrect data types
curl -Method POST -Uri http://localhost:5000/forecast_prices/ -ContentType 'application/json' -Body '{"sku": "2200", "time_key": "20250101"}'
curl -Method POST -Uri http://localhost:5000/forecast_prices/ -ContentType 'application/json' -Body '{"sku": 2200, "time_key": 20250101}'
# incorrect content
curl -Method POST -Uri http://localhost:5000/forecast_prices/ -ContentType 'application/json' -Body '{"sku": "2200", "time_key": 202501010}'
curl -Method POST -Uri http://localhost:5000/forecast_prices/ -ContentType 'application/json' -Body '{"sku": "2200", "time_key": 20252101}'
curl -Method POST -Uri http://localhost:5000/forecast_prices/ -ContentType 'application/json' -Body '{"sku": "2200", "time_key": -2025011}'
curl -Method POST -Uri http://localhost:5000/forecast_prices/ -ContentType 'application/json' -Body '{"sku": "2200", "time_key": 40250101}'
curl -Method POST -Uri http://localhost:5000/forecast_prices/ -ContentType 'application/json' -Body '{"sku": "1", "time_key": 20250101}'
curl -Method POST -Uri http://localhost:5000/forecast_prices/ -ContentType 'application/json' -Body '{"sku": "hello", "time_key": 20250101}'
curl -Method POST -Uri http://localhost:5000/forecast_prices/ -ContentType 'application/json' -Body '{"sku": "9999999999", "time_key": 20250101}'
# duplicated product-date pair
curl -Method POST -Uri http://localhost:5000/forecast_prices/ -ContentType 'application/json' -Body '{"sku": "2222", "time_key": 20250101}'
# ACTUAL ENDPOINT
# correct
curl -Method POST -Uri http://localhost:5000/actual_prices/ -ContentType 'application/json' -Body '{"sku": "2222", "time_key": 20250101, "pvp_is_competitorA_actual": 3.5, "pvp_is_competitorB_actual": 3.2}'
curl -Method POST -Uri http://localhost:5000/actual_prices/ -ContentType 'application/json' -Body '{"sku": "2222", "time_key": 20250102, "pvp_is_competitorA_actual": 3.3, "pvp_is_competitorB_actual": 3}'
# incorrect keys
curl -Method POST -Uri http://localhost:5000/actual_prices/ -ContentType 'application/json' -Body '{"sku": "2200", "time_key": 20250101, "pvp_is_competitorA_actual": 3.5, "pvp_is_competitorB_actual": 3.2, "extra": "extra"}'
curl -Method POST -Uri http://localhost:5000/actual_prices/ -ContentType 'application/json' -Body '{"sku": "2200", "time_key": 20250101, "pvp_is_competitorA_actual": 3.5}'
# incorrect data types
curl -Method POST -Uri http://localhost:5000/actual_prices/ -ContentType 'application/json' -Body '{"sku": "2200", "time_key": 20250101, "pvp_is_competitorA_actual": "3.5", "pvp_is_competitorB_actual": 3.2}'
# incorrect content
curl -Method POST -Uri http://localhost:5000/actual_prices/ -ContentType 'application/json' -Body '{"sku": "2200", "time_key": 20250101, "pvp_is_competitorA_actual": -3.5, "pvp_is_competitorB_actual": 3.2}'
# unexistent product-date pair
curl -Method POST -Uri http://localhost:5000/actual_prices/ -ContentType 'application/json' -Body '{"sku": "4222", "time_key": 20250101, "pvp_is_competitorA_actual": 3.5, "pvp_is_competitorB_actual": 3.2}'