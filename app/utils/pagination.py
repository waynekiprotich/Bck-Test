from flask import request


def paginate(query, schema):
    """
    Generic pagination helper.

    Usage:
        query = User.query.order_by(User.points.desc())
        return jsonify(paginate(query, users_schema))

    Query params accepted:
        ?page=1&per_page=20
    """
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    per_page = min(per_page, 100)   # hard cap — never let clients request all rows

    result = query.paginate(page=page, per_page=per_page, error_out=False)

    return {
        "data": schema.dump(result.items),
        "pagination": {
            "page": result.page,
            "per_page": result.per_page,
            "total": result.total,
            "total_pages": result.pages,
            "has_next": result.has_next,
            "has_prev": result.has_prev,
        },
    }
