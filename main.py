#!/usr/bin/python

import db
from mail_addresser import send_mail
from query_analyzer import get_query_result, check_query_result


SEARCH_URL = 'https://ak.api.onliner.by/search/apartments?'

QUERY_1 = ('rent_type%5B%5D=1_room&rent_type%5B%5D=2_rooms&rent_type%5B%5D=3_rooms&rent_type%5B%5D=4_rooms&rent_type%5B%5D=5_rooms&rent_type%5B%5D=6_rooms&bounds%5Blb%5D%5Blat%5D=53.95156887642234&bounds%5Blb%5D%5Blong%5D=27.660295717294208&bounds%5Brt%5D%5Blat%5D=53.958790384087116&bounds%5Brt%5D%5Blong%5D=27.669635711569363&page=1&v=0.25808833581239154')

QUERY_2 = ('rent_type%5B%5D=1_room&rent_type%5B%5D=2_rooms&rent_type%5B%5D=3_rooms&rent_type%5B%5D=4_rooms&rent_type%5B%5D=5_rooms&rent_type%5B%5D=6_rooms&bounds%5Blb%5D%5Blat%5D=53.950480595601505&bounds%5Blb%5D%5Blong%5D=27.664237194878083&bounds%5Brt%5D%5Blat%5D=53.96492273718283&bounds%5Brt%5D%5Blong%5D=27.682917183428426&page=1&v=0.7297880412518498')


query_list = [QUERY_1, QUERY_2]


def main():
    connection = db.connect_to_mysql()
    db.use_db(connection, 'onliner_rent')
    query_result = get_query_result(SEARCH_URL, *query_list)
    valid_results = check_query_result(connection, query_result)
    

    for properties in valid_results:
        send_mail(properties)
        
    connection.close()


if __name__ == "__main__":
    main()
