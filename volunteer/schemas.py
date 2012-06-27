from colander import Schema, SchemaNode, String, Integer, DateTime

class SmsSchema(Schema):
    username = SchemaNode(String())
    password = SchemaNode(String())
    type = SchemaNode(String())
    to = SchemaNode(String())
    network_code = SchemaNode(String())
    message_id = SchemaNode(String())
    message_timestamp = SchemaNode(DateTime())
    text = SchemaNode(String())
    concat = SchemaNode(String())
    concat_ref = SchemaNode(String())
    concat_total = SchemaNode(Integer())
    concat_part = SchemaNode(Integer())
