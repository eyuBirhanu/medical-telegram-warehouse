with source as (
    select * from {{ source('raw', 'telegram_messages') }}
),
cleaned as (
    select
        message_id,
        channel_name,
        cast(message_date as timestamp) as message_date,
        message_text,
        coalesce(views, 0) as views,
        coalesce(forwards, 0) as forwards,
        has_media,
        image_path
    from source
    where message_date is not null
)
select * from cleaned