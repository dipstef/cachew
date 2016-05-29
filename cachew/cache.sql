create table if not exists response (
    id                  integer primary key autoincrement,
    request_url         text,
    method              text,
    response_url        text,
    status              text,
    date                timestamp,
    headers             data,
    body                text,
    unique(request_url, method)
);

create table if not exists history (
    id                  integer primary key autoincrement,
    request_url         text,
    method              text,
    sha1                text,
    response_url        text,
    status              text,
    date                timestamp,
    headers             data,
    body                text,
    unique(request_url, method, sha1)
);
