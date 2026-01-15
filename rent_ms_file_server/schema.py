from graphene import ObjectType
import graphene

from rent_ms_accounts.models import UsersProfiles
from rent_ms_dto.Enum import ProductTypeEnum
from rent_ms_dto.Files import FileAttachmentsResponseObject, FileAttachmentsObjects, OpenFileInputObjects, OpenRelatedFileInputObjects
from rent_ms_dto.Response import ResponseObject
from rent_ms_utils.FileUtils import UploadFile


class Query(ObjectType):
    open_file = graphene.Field(FileAttachmentsResponseObject, input=OpenFileInputObjects())
    open_related_file = graphene.Field(FileAttachmentsResponseObject, attachment_path=graphene.String())

    @staticmethod
    def resolve_open_file(root, info, input):

            if   input.product_type  == ProductTypeEnum.food_value_:
            #  product = VilcomFood.objects.filter(uuid=input.product_id,is_active=True).first()
            #  base64EncodedString = UploadFile.base64_file_data(product.food_photo)

            # elif input.product_type  == ProductTypeEnum.service_value_:
            #  product = VilcomService.objects.filter(uuid=input.product_id,is_active=True).first()
            #  base64EncodedString = UploadFile.base64_file_data(product.service_photo)

            # elif input.product_type  == ProductTypeEnum.package_value_:
            #   product = VilcomPackage.objects.filter(uuid=input.product_id,is_active=True).first()
            #   base64EncodedString = UploadFile.base64_file_data(product.package_photo)
           
            # elif input.product_type == ProductTypeEnum.user_value_:
            #  product = UsersProfiles.objects.filter(profile_unique_id=input.product_id,is_active=True).first()
            #  base64EncodedString = UploadFile.base64_file_data(product.profile_photo)
                
            return info.return_type.graphene_type(response=ResponseObject.get_response('1'), data=FileAttachmentsObjects(base64_string=base64EncodedString))


    @staticmethod
    def resolve_open_related_file(root, info, attachment_path):

        base64EncodedString = UploadFile.base64_file_data(attachment_path)

        return info.return_type.graphene_type(response=ResponseObject.get_response('1'), data=base64EncodedString)

