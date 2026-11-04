{% set GOLD_PATH = var('GOLD_PATH', 'all') %}
{% set SILVER_PATH = var('SILVER_PATH', 'all') %}

{% set competition = var('competition', 'unknown') %}
{% set season = var('season', 'unknown') %}

{% set silver_glob = SILVER_PATH ~ '/player_stats/' ~ competition ~ '/' ~ season ~ '/**/*.json' %}

{% set gold_file = GOLD_PATH ~ '/player_stats/' ~ competition ~ '_' ~ season ~ '.parquet' %}

{{ config(
    materialized='external',
    location=gold_file,
    format='parquet'
) }}

SELECT *
FROM read_json_auto(
    '{{ silver_glob }}',
    union_by_name = true
)