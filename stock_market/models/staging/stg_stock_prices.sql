with source as (
    select * from {{ source('raw', 'stock_prices') }}
),

renamed as (
    select
        date,
        ticker,
        close,
        high,
        low,
        open,
        volume,
        daily_return,
        moving_avg_7d,
        year,
        month
    from source
    where close is not null
)

select * from renamed