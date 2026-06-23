def rewrite_query(query):

    return f"""
PCOS symptoms:
{query}

Retrieve relevant medical information related to:
- PCOS
- hormones
- insulin resistance
- menstrual cycle
- lifestyle
"""