import graphene
from graphene_file_upload.scalars import Upload
from rent_ms_dto.Enum import ProductTypeEnum
from rent_ms_dto.Response import ResponseObject


class FileInputObjects(graphene.InputObjectType):
    service_name = graphene.String()
    file = Upload()

class Base64FileInputObjects(graphene.InputObjectType):
    product_id = graphene.String(required=True)
    base64_string = graphene.String()
    product_type = ProductTypeEnum()

class Base64StringInputObjects(graphene.InputObjectType):
    base64_string = graphene.String()
    spatial_uuid = graphene.String()

class FileObjects(graphene.ObjectType):
    attachment_path = graphene.String()
    file_name = graphene.String()

class FileAttachmentsObjects(graphene.ObjectType):
    base64_string = graphene.String()


class OpenRelatedFileInputObjects(graphene.InputObjectType):
    product_id = graphene.String(required=True)

class OpenFileInputObjects(graphene.InputObjectType):
    product_id = graphene.String(required=True)
    product_type = ProductTypeEnum()

class FileAttachmentsResponseObject(graphene.ObjectType):
    data = graphene.Field(FileAttachmentsObjects)
    response = graphene.Field(ResponseObject)