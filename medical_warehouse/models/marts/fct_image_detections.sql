with raw_detections as (
    select * from {{ source('raw', 'image_detections') }}
),

messages as (
    select * from {{ ref('stg_telegram_messages') }}
)

select
    d.message_id,
    -- Generate the same channel key to link tables
    {{ dbt_utils.generate_surrogate_key(['d.channel_name']) }} as channel_key,
    d.detected_class,
    d.confidence,
    d.image_path,
    m.message_date
from raw_detections d
left join messages m 
    on d.message_id = m.message_id 
    and d.channel_name = m.channel_name