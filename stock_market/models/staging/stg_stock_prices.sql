with source as (
    select * from {{ source('raw', 'stock_prices') }}
),

deduplicated as (
    select 
        *,
        -- Nadajemy numer wiersza dla każdej kombinacji tickera i daty
        row_number() over (
            partition by ticker, date 
            order by ticker, date
        ) as row_num
    from source
),

renamed as (
    select
        {{ dbt_utils.generate_surrogate_key(['ticker', 'date']) }} as stock_id,
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
    from deduplicated
    -- Wybieramy tylko pierwsze wystąpienie danego wiersza
    where row_num = 1
    and close is not null
)

select * from renamed