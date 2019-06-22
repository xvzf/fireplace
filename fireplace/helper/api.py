from functools import wraps
from sanic.response import text
from sanic_openapi import doc

def query_arg(name, convert_func, error_handler_predef=None, description: str = "Not documented."):
    """ Helper wrapper for converting query arguments and passing them to the function as
    keyword argument

    @param name: Query argument name
    @param convert_func: Function to convert string to desired datatype
    @praram description: Description for openapi
    """

    async def error_handler(request, *args, **kwargs):
        return text(f"Query parameter {name} is not found or invalid.", status=400)

    def decorator(f):

        @wraps(f)
        @doc.consumes({name: doc.String(description)})
        async def wrapper(request, *args, **kwargs):
            # Try to parse the query parameter. If not possible, return error handler
            try:
                val = convert_func(request.args.get(name))
                return await f(request, *args, **{**kwargs, name: val})
            except ValueError as e:
                return await (error_handler_predef or error_handler)(request, *args, **kwargs)
            except Exception as e:
                raise e
        return wrapper

    return decorator