
def render_entity(entity_type, entity_data):
    renderer = __import__('chembl_slack.templates.{0}_template'.format(entity_type.lower()), globals(), locals(), ['render'], -1)
    return renderer.render(entity_data)
