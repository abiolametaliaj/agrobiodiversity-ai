-- Pyetje leximi (Java 2). Çdo pyetje fillon me "-- Qn: titulli".

-- Q1: Të gjitha vëzhgimet (kolonat kryesore)
SELECT observation_id, class_label, label_status, plot_id, date_time, data_origin
FROM observations
ORDER BY date_time;

-- Q2: Filtër sipas datës (3–6 nëntor 2026)
SELECT observation_id, class_label, plot_id, date_time
FROM observations
WHERE date_time >= '2026-11-03' AND date_time < '2026-11-07'
ORDER BY date_time;

-- Q3: Filtër sipas parcelës (P02)
SELECT observation_id, class_label, date_time
FROM observations
WHERE plot_id = 'P02'
ORDER BY date_time;

-- Q4: Filtër sipas klasës (Syrphidae)
SELECT observation_id, plot_id, date_time
FROM observations
WHERE class_label = 'Syrphidae';

-- Q5: Numri i vëzhgimeve për klasë (NULL = pa etiketë)
SELECT COALESCE(class_label, '(pa etiketë)') AS class_label, COUNT(*) AS n
FROM observations
GROUP BY class_label
ORDER BY n DESC;

-- Q6: Vëzhgimet me burimin dhe licencën (JOIN)
SELECT o.observation_id, s.source_name, s.author, s.license, s.consent_status
FROM observations o
JOIN image_sources s ON s.source_id = o.source_id
ORDER BY o.observation_id;

-- Q7: Demo kundrejt vëzhgimeve reale
SELECT data_origin, COUNT(*) AS n
FROM observations
GROUP BY data_origin;
