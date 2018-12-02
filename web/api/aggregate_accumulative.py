import requests
from flask import Blueprint, request, jsonify, json

from web import util

bp = Blueprint('aggregate_accumulative', __name__)
callback_url = f'{util.HOST_URL}/extension/transformation/aggregate-accumulative'

""" Transformation Structure:
{
    extensionId: "",
    extension: enum("Transformation", "Validation", "Interpolation"),
    function: "AggregateAccumulative",
    inputVariables: [
        {
            variableId: "",
            timeseriesId: "",
            data: [{
                time: "",
                value: ""
            }]
        }
    ],
    outputVariables: [
        {
            variableId: "",
            timeseriesId: ""
        }
    ],
    options: {},
    callback: "",

    start: "",
    end: "",
    token: "",
}
"""


@bp.route('/extension/transformation/aggregate-accumulative', methods=['POST'])
def extension_transformation_aggregate_accumulative():
    extension = request.get_json()
    print("Extension Transformation AggregateAccumulative:", extension)
    assert 'extensionId' in extension, f'extensionId should be provided'
    assert 'inputVariables' in extension and isinstance(extension['inputVariables'], list), \
        f'inputVariables should be provided'
    assert 'outputVariables' in extension and isinstance(extension['outputVariables'], list), \
        f'outputVariables should be provided'

    trigger_data = {
        "output_variables": extension['outputVariables'],
        "input_variables": extension['inputVariables'],
        "options": extension['options'],
        'callback': extension['callback'],
        "token": request.args.get('token'),
        "start": request.args.get('from'),
        "end": request.args.get('end'),
    }
    process_aggregate_accumulative(**trigger_data)

    del extension['inputVariables']
    del extension['outputVariables']
    extension['callback'] = f'{util.HOST_URL}/extension/transformation/aggregate-accumulative',
    return jsonify(extension)


def process_aggregate_accumulative(input_variables=None, output_variables=None, options=None, **kwargs):
    if options is None:
        options = {}
    if output_variables is None:
        output_variables = []
    if input_variables is None:
        input_variables = []
    input_x = input_variables[0]
    output_y = output_variables[0]
    output_y['data'] = input_x['data']
    trigger_callback([output_y], kwargs.get('callback'), kwargs.get('token'))
    return [output_y]


def trigger_callback(output_variables, callback, token):
    print("Trigger callback", output_variables)
    callback_trigger = {
        "outputVariables": output_variables,
        "callback": callback_url,
    }
    res = requests.post(f'{callback}/{token}', json=callback_trigger)
    print(res.status_code, res.text)
    assert res.status_code is 200, f'Unable to update job completion token: {token} for {callback}'
    return
