create table if not exists metrics (
  time        TIMESTAMPTZ       NOT NULL,
  name        TEXT              NOT NULL,
  temperature DOUBLE PRECISION  NULL
);

select create_hypertable('metrics', 'time', if_not_exists => TRUE);
