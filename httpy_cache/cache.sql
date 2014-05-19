create table response (
    id                  integer primary key not null autoincrement,
    request_url         text,
    method              text,
    response_url        text,
    status              text,
    date                timestamp,
    headers             data,
    body                text,
    unique(request_url, method)
);