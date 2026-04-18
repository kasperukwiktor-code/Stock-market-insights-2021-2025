{{ config(
    materialized='table',
    schema='mart'
) }}

with staging as (
    select * from {{ ref('stg_stock_prices') }}
),

mart as (
    select
        -- Klucz główny: Ticker + Rok + Miesiąc
        {{ dbt_utils.generate_surrogate_key(['ticker', 'year', 'month']) }} as monthly_stock_id,
        ticker,
        -- Tworzymy pełną datę (np. 2024-01-01), ułatwi to życie w Power BI
        date_from_parts(year, month, 1) as report_month,
        year,
        month,
        round(avg(close), 2) as avg_close,
        round(min(close), 2) as min_close,
        round(max(close), 2) as max_close,
        round(avg(daily_return), 6) as avg_daily_return_pct,
        round(avg(moving_avg_7d), 2) as avg_moving_avg_7d,
        sum(volume) as total_volume
    from staging
    group by ticker, year, month
)

select * from mart
order by ticker, report_month desc