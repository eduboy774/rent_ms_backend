from collections import defaultdict
import json
from graphql import validate, parse, visit
from graphene.validation import depth_limit_validator
from graphene.validation import DisableIntrospection




class ValidationsMiddleware:
    def resolve(self, next, root, info, **args):
        data_str = info.context.body.decode("utf-8")     
        jsn = json.loads(data_str)
        
        validation_errors = validate(
            schema=info.schema,
            document_ast=parse(jsn['query']),
            rules=(
                depth_limit_validator(max_depth=5),
                DisableIntrospection,
            ),
        )
        
        if len(validation_errors) > 0:
            return None

        return next(root, info, **args)
    
