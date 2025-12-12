curl -X POST http://localhost:5000/forecast_prices/ -H "Content-Type:application/json" -d '{"sku": "2121", "time_key": 20250101}'

# FORECAST ENDPOINT
# correct
curl -X POST http://localhost:5000/forecast_prices/ -H "Content-Type:application/json" -d '{"sku": "2222", "time_key": 20250101}'
curl -X POST http://localhost:5000/forecast_prices/ -H "Content-Type:application/json" -d '{"sku": "2222", "time_key": 20250102}'
curl -X POST http://localhost:5000/forecast_prices/ -H "Content-Type:application/json" -d '{"sku": "2223", "time_key": 20250101}'
# incorrect keys
curl -X POST http://localhost:5000/forecast_prices/ -H "Content-Type:application/json" -d '{"sku": "2200", "time_key": 20250101, "extra": "extra"}'
curl -X POST http://localhost:5000/forecast_prices/ -H "Content-Type:application/json" -d '{"sku": "2200"}'
# incorrect data types
curl -X POST http://localhost:5000/forecast_prices/ -H "Content-Type:application/json" -d '{"sku": "2200", "time_key": "20250101"}'
curl -X POST http://localhost:5000/forecast_prices/ -H "Content-Type:application/json" -d '{"sku": 2200, "time_key": 20250101}'
# incorrect content
curl -X POST http://localhost:5000/forecast_prices/ -H "Content-Type:application/json" -d '{"sku": "2200", "time_key": 202501010}'
curl -X POST http://localhost:5000/forecast_prices/ -H "Content-Type:application/json" -d '{"sku": "2200", "time_key": 20252101}'
curl -X POST http://localhost:5000/forecast_prices/ -H "Content-Type:application/json" -d '{"sku": "2200", "time_key": -2025011}'
curl -X POST http://localhost:5000/forecast_prices/ -H "Content-Type:application/json" -d '{"sku": "2200", "time_key": 40250101}'
curl -X POST http://localhost:5000/forecast_prices/ -H "Content-Type:application/json" -d '{"sku": "1", "time_key": 20250101}'
curl -X POST http://localhost:5000/forecast_prices/ -H "Content-Type:application/json" -d '{"sku": "hello", "time_key": 20250101}'
curl -X POST http://localhost:5000/forecast_prices/ -H "Content-Type:application/json" -d '{"sku": "9999999999", "time_key": 20250101}'
# duplicated product-date pair
curl -X POST http://localhost:5000/forecast_prices/ -H "Content-Type:application/json" -d '{"sku": "2222", "time_key": 20250101}'
# ACTUAL ENDPOINT
# correct
curl -X POST http://localhost:5000/actual_prices/ -H "Content-Type:application/json" -d '{"sku": "2222", "time_key": 20250101, "pvp_is_competitorA_actual": 3.5, "pvp_is_competitorB_actual": 3.2}'
curl -X POST http://localhost:5000/actual_prices/ -H "Content-Type:application/json" -d '{"sku": "2222", "time_key": 20250102, "pvp_is_competitorA_actual": 3.3, "pvp_is_competitorB_actual": 3}'
# incorrect keys
curl -X POST http://localhost:5000/actual_prices/ -H "Content-Type:application/json" -d '{"sku": "2200", "time_key": 20250101, "pvp_is_competitorA_actual": 3.5, "pvp_is_competitorB_actual": 3.2, "extra": "extra"}'
curl -X POST http://localhost:5000/actual_prices/ -H "Content-Type:application/json" -d '{"sku": "2200", "time_key": 20250101, "pvp_is_competitorA_actual": 3.5}'
# incorrect data types
curl -X POST http://localhost:5000/actual_prices/ -H "Content-Type:application/json" -d '{"sku": "2200", "time_key": 20250101, "pvp_is_competitorA_actual": "3.5", "pvp_is_competitorB_actual": 3.2}'
# incorrect content
curl -X POST http://localhost:5000/actual_prices/ -H "Content-Type:application/json" -d '{"sku": "2200", "time_key": 20250101, "pvp_is_competitorA_actual": -3.5, "pvp_is_competitorB_actual": 3.2}'
# unexistent product-date pair
curl -X POST http://localhost:5000/actual_prices/ -H "Content-Type:application/json" -d '{"sku": "4222", "time_key": 20250101, "pvp_is_competitorA_actual": 3.5, "pvp_is_competitorB_actual": 3.2}'