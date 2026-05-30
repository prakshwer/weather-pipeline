-- All readings for a city
SELECT * FROM raw_weather WHERE city = 'Mumbai' ORDER BY timestamp DESC;

-- Average temperature per city
SELECT city, ROUND(AVG(temp_celsius), 2) AS avg_temp
FROM raw_weather
GROUP BY city;

-- Hottest recorded temperatures
SELECT city, MAX(temp_celsius) AS max_temp, timestamp
FROM raw_weather
GROUP BY city
ORDER BY max_temp DESC;

-- High humidity alerts
SELECT city, humidity_pct, timestamp
FROM raw_weather
WHERE humidity_pct > 80
ORDER BY timestamp DESC;

-- Readings per day
SELECT DATE(timestamp) AS date, city, COUNT(*) AS readings
FROM raw_weather
GROUP BY DATE(timestamp), city;