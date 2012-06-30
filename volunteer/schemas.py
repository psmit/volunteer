from colander import Schema, SchemaNode, String, Integer, DateTime

class SmsSchema(Schema):
    username = SchemaNode(String(),missing=None)
    password = SchemaNode(String(),missing=None)
    type = SchemaNode(String(),missing=None)
    to = SchemaNode(String(),missing=None)
    msisdn = SchemaNode(String())
    network_code = SchemaNode(String(),missing=None)
    message_id = SchemaNode(String(),missing=None)
    message_timestamp = SchemaNode(DateTime(),missing=None)
    text = SchemaNode(String(),missing=None)
    concat = SchemaNode(String(),missing=None)
    concat_ref = SchemaNode(String(),missing=None)
    concat_total = SchemaNode(Integer(),missing=None)
    concat_part = SchemaNode(Integer(),missing=None)
