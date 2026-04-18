select
    date,
    ticker,
    high,
    low
from {{ ref('stg_stock_prices') }}
where high < low