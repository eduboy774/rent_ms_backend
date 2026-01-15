import json
from django.contrib.sessions.models import Session

from rent_ms_dto.Response import ResponseObject


def has_mutation_access(permissions=[]):
    """
    This function validates the access for the given user.
    From the request header, it takes parmission that was obteained from UAA service
    and validate against give permissions that guard the access to specific endpoint.
    """
    
    def decorator(view_func):
        def wrap(info, *args, **kwargs):
            try:              
                if not permissions:
                    info.response = ResponseObject(id="46")
                    return info

                _, headers_part = args 

                user_data = json.loads(headers_part.context.headers['User'])
                has_give_permissions = any(permision in user_data['user_permissions'] for permision in permissions)

                if has_give_permissions:
                    return view_func(info, *args, **kwargs)
                else:
                    info.response = ResponseObject(id="46")
                    try:
                        info.data = None
                    except:
                        pass
                    return info
            except:
                info.response = ResponseObject(id="46")
                try:
                    info.data = None
                except:
                    pass
                return info
        return wrap

    return decorator


def has_query_access(permissions=[]):
    """
    This function validates the access for the given user.
    From the request header, it takes parmission that was obteained from UAA service
    and validate against give permissions that guard the access to specific endpoint.
    """
    
    def decorator(view_func):
        def wrap(info, *args, **kwargs):
            try:
                if not permissions:
                    return responseObject(response=ResponseObject(id="46"), data=None)

                headers_part = args[0] 
                responseObject = headers_part.return_type.graphene_type

                user_data = json.loads(headers_part.context.headers['User'])
                has_give_permissions = any(permision in user_data['user_permissions'] for permision in permissions)

                if has_give_permissions:
                    return view_func(info, *args, **kwargs)
                else:
                    return responseObject(response=ResponseObject(id="46"), data=None)
            except:
                return responseObject(response=ResponseObject(id="46"), data=None)
        return wrap

    return decorator
