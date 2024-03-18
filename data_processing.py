from datetime import datetime
import json

def processData(YEAR_TARGET):
    with open(f'data_{YEAR_TARGET}.json', 'r') as file:
        json_data = file.read()

    # Parse to JSON
    parsed_data = json.loads(json_data)

    final_data = []

    for item in parsed_data['lista']:
        parsed_json = json.loads(item['json'])
        data = datetime.fromtimestamp(
            item['dtProcessamento']).strftime('%d/%m/%Y')
        parsed_year = str(datetime.fromtimestamp(
            item['dtProcessamento'])).split(' ')[0].split('-')[0]

        if (int(parsed_year) == int(YEAR_TARGET)) and item['indSituacao'] == '1':
            if len(final_data) == 0:
                final_data.append({
                    "numeroDoc": parsed_json['ide']['nNF'],
                    "data": data,
                    "total_value": float(parsed_json['total']['ICMSTotal']['vNF'].replace(',', '.')),
                    "destinatario": parsed_json['dest']['xNome'],
                })
            else:
                for i in final_data:
                    if i['numeroDoc'] == parsed_json['ide']['nNF']:
                        break
                else:
                    final_data.append({
                        "numeroDoc": parsed_json['ide']['nNF'],
                        "data": data,
                        "total_value": float(parsed_json['total']['ICMSTotal']['vNF'].replace(',', '.')),
                        "destinatario": parsed_json['dest']['xNome'],
                    })

    return final_data