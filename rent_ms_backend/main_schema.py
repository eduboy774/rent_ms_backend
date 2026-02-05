from graphene_federation import build_schema

from rent_ms_settings.views import Mutation as rent_ms_settings_mutation
from rent_ms_settings.schema import Query as   rent_ms_settings_query
from rent_ms_accounts.views import Mutation as rent_ms_accounts_mutation
from rent_ms_accounts.schema import Query as   rent_ms_accounts_query


class Query(rent_ms_settings_query,rent_ms_accounts_query):
    pass

class Mutation(rent_ms_settings_mutation,rent_ms_accounts_mutation):
    pass


schema = build_schema(query=Query, mutation=Mutation) 