with stg_messages as (
    select * from {{ ref('stg_telegram_messages') }}
)

select
    message_id,
    -- Foreign Key to dim_channels
    {{ dbt_utils.generate_surrogate_key(['channel_name']) }} as channel_key,
    message_date,
    message_text,
    views,
    forwards,
    has_media,
    image_path
from stg_messages