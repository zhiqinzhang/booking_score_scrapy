import googlemaps

KEY = ''


def get_google_results(address, api_key=KEY):
    gmaps = googlemaps.Client(key=api_key)
    results = gmaps.geocode(address)[0]
    print(results)

    # if there's no results or an error, return empty results.
    if len(results) == 0:
        output = {
            # "formatted_address": None,
            "latitude": None,
            "longitude": None,
            # "location_type": None,
        }
    else:
        output = {
            # "formatted_address": results['formatted_address'],
            "latitude": results['geometry']['location']['lat'],
            "longitude": results['geometry']['location']['lng'],
            # "location_type": results['geometry']['location_type'],
            # "google_place_id": answer.get("place_id"),
            # "type": ",".join(answer.get('types')),
            # "postcode": ",".join([x['long_name'] for x in answer.get('address_components')
            #                       if 'postal_code' in x.get('types')])
        }

    return output


if __name__ == '__main__':
    test_result = get_google_results(address="8 Whiteman Street, Southbank, 3006 Melbourne, Australia",
                                     api_key=KEY)
    # print(test_result['latitude'])
    # print(test_result['longitude'])
    # print(test_result['location_type'])
