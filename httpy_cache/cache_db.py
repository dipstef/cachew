from quelo.query import get_row


def insert_response(cursor, request_url, method, response_url, status, updated, headers, body):
    cursor.execute('''insert into response(request_url, method, response_url, status, date, headers, body)
                         values(?,?,?,?,?,?,?) ''', (request_url, method, response_url, status, updated, headers, body))


def update_response(cursor, request_url, method, response_url, status, updated, headers, body):
    cursor.execute('''update response
                         set response_url = ?,
                             status = ?,
                             date = ? ,
                             body = ?,
                             headers = ?
                       where request_url = ?
                          and method =?''', (response_url, status, updated, body, headers, request_url, method))


def get_response(cursor, request_url, method):
    return get_row(cursor, '''select response_url,
                                     status,
                                     headers,
                                     body,
                                     date
                                from response
                               where request_url = ?
                                 and method = ? ''', (request_url, method))