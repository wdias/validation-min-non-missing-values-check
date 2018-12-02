from flask import Blueprint, request, jsonify, json
from sqlalchemy import text as sql

from web import util

bp = Blueprint('aggregate_accumulative', __name__)

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
    from: "",
    to: "",
    token: ""
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

    extension['outputVariables'] = process_aggregate_accumulative(**extension)
    del extension['inputVariables']
    del extension['options']
    return jsonify(extension)


def process_aggregate_accumulative(inputVariables: list = [], outputVariables: list = [], options: object = {}, **kwargs):
    input_x = inputVariables[0]
    output_y = outputVariables[0]
    output_y['data'] = input_x['data']
    return [output_y]
