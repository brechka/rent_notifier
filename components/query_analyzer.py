import requests
import json


def get_query_result(root_url, *query):
    """
    Gets the query result. Root_url is an immutable part of the url and query
    is a query string. Function returns a listed queries results.
    """
    
    query_result = []
    for q in query:
        get_result = requests.get(root_url + q)
        query_result.extend(json.loads(get_result.text)['apartments'][:])
    return query_result


def check_query_result(connection, apartments):
    """
    Checks if the following data exists in the database. If yes - skip the item,
    otherwise - calls create_apartment function.
    Connection is an argument responsible for connection.
    """
    
    for apartment in apartments:
        hash = str(apartment['id']) + apartment['created_at']
        cursor = connection.cursor()
        query = "SELECT * FROM apartments WHERE hash = %s"
        cursor.execute(query, (hash,))
        if cursor.fetchall() == []:
            num_rooms = apartment['rent_type'][0]
            location = apartment['location']['address']
            amount = apartment['price']['amount']
            currency = apartment['price']['currency']
            price = f'{amount} {currency}'
            photo = apartment['photo']
            url = apartment['url']
            create_apartment(connection, hash, url)
            
            yield (num_rooms, location, price, photo, url)
        else:
            continue


def create_apartment(connection, hash, url):
    """
    Create a new apartment id and inserts required properties to the database.
    """
    
    cursor = connection.cursor()
    sql = "INSERT INTO apartments (hash, url) VALUES (%s, %s)"
    cursor.execute(sql, (hash, url))
    connection.commit()
