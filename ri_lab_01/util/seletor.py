def get_value_by_selector(response, selector):
    """Get an list of values by specified selector
    :param response: the page response
    :param selector: the css selector
    """
    return response.css(selector)