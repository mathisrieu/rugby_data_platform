-- Case when this is the first global_stats file for this player (no file existing in the silver folder)
{% set BRONZE_PATH = var('BRONZE_PATH', 'all') %}
{% set SILVER_PATH = var('SILVER_PATH', 'all') %}

{% set is_the_first_file = var('is_the_first_file', 'all') %}

{% set player_name = var('target_player_name', 'all') %}
{% set team = var('team', 'all') %}
{% set match_label = var('match_label', 'all') %}
{% set bronze_folder = BRONZE_PATH~'/player_stats/'~team~'/'~player_name~'/'~player_name~'_global_stats.json' %}
{% set silver_folder = SILVER_PATH~'/player_stats/'~team~'/'~player_name~'/'~player_name~'_global_stats.json' %}


{{ config(
    enabled = (is_the_first_file == 1),
    materialized='external',
    location=silver_folder,
    format='json'
) }}

-- Extracting first basics metrics
WITH base_data AS (
    SELECT 
        (competition->>'rid')::INT AS competition_id,
        competition->>'name' AS competition_name,
        competition->'season'->>'label' AS season,
        player_url AS player_id,
        (competition->'stats'->'stats') AS stats_json
    FROM read_json_auto('{{bronze_folder}}')
)

-- Extracting metrics from stats_json
SELECT
    competition_id,
    competition_name,
    season,
    player_id,
    -- Retrieve player_id and team_id
    --(stats_json->>'player_id')::INT AS player_id,
    (stats_json->>'player_team_id')::INT AS player_team_id,
    (stats_json->>'total_games')::INT AS match_num,
    '{{match_label}}' AS match_label,
    -- For player stats, we load it into the field 'raw_stats' as a dictionary
    stats_json AS raw_stats
FROM base_data

