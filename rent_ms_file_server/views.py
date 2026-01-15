import base64
import mimetypes
import graphene
import magic

from rent_ms_accounts.models import UsersProfiles
from rent_ms_builders.SettingsBuilders import SettingsBuilders
from rent_ms_builders.UserAccountsBuilders import UserAccountBuilder
from rent_ms_dto.Files import Base64FileInputObjects, Base64StringInputObjects
from rent_ms_dto.Response import ResponseObject
from rent_ms_dto.Settings import VilcomFoodObject, VilcomServiceObject
from rent_ms_dto.UserAccounts import UserProfileObject
from rent_ms_settings.models import VilcomFood, VilcomPackage, VilcomService
from rent_ms_utils.FileUtils import UploadFile
from rent_ms_utils.UserUtils import UserUtils
from rent_ms_dto.Enum import ProductTypeEnum


class UploadFileMutation(graphene.Mutation):
    class Arguments:
        input = Base64FileInputObjects(required=True)
    response = graphene.Field(ResponseObject)

    if  input.product_type  == ProductTypeEnum.food_value_:
         data = graphene.Field(VilcomFoodObject)
    elif input.product_type  == ProductTypeEnum.service_value_:
         data = graphene.Field(VilcomServiceObject)
    elif input.product_type  == ProductTypeEnum.service_value_:
         data = graphene.Field(VilcomServiceObject)
    elif input.product_type  == ProductTypeEnum.user_value_:
         data = graphene.Field(UserProfileObject)


    @classmethod
    def mutate(self, root, info, input):
        
        if input.base64_string is None:
            return self(response=ResponseObject.get_response(id='4'), data=None)
        
        elif input.product_type is None:
             return self(response=ResponseObject.get_response(id='11'), data=None)
        
        allowed_images_for_upload = ["jpeg", "jpg", "png"]
        allowed_documents_for_upload = ["docs", "xls", "pdf","txt", "doc"]
        allowed_videos_for_upload = ["mp4", "webm", "gif"]
        
        decoded_data = base64.b64decode(input.base64_string)
        file_type = magic.from_buffer(decoded_data,mime=True)
        file_extension = mimetypes.guess_extension(file_type)

        if file_extension is None:
            return self(response=ResponseObject.get_response(id='12'), data=None)
        
        parent_folder="documents"
        if file_extension.replace('.','') in allowed_images_for_upload:
            parent_folder="images"

        elif file_extension.replace('.','') in allowed_documents_for_upload:
            parent_folder="documents"

        elif file_extension.replace('.','') in allowed_videos_for_upload:
            parent_folder="videos"
        else:
            return self(response=ResponseObject.get_response(id='4'), data=None)
        
        attachment_path = UploadFile.base64_handler(input,file_extension,parent_folder)


        if   input.product_type  == ProductTypeEnum.food_value_:
             product = VilcomFood.objects.filter(uuid=input.product_id,is_active=True).first()
             product.food_photo = attachment_path
             product.save()

             data=SettingsBuilders.get_vilcom_food_data(id=product.uuid)
             return info.return_type.graphene_type(response=ResponseObject.get_response('1'), data=data)

        elif input.product_type  == ProductTypeEnum.service_value_:
             product = VilcomService.objects.filter(uuid=input.product_id,is_active=True).first()
             product.service_photo = attachment_path
             product.save()

             data=SettingsBuilders.get_vilcom_service_data(id=product.uuid)
             return info.return_type.graphene_type(response=ResponseObject.get_response('1'), data=data)

        elif input.product_type  == ProductTypeEnum.package_value_:
             product = VilcomPackage.objects.filter(uuid=input.product_id,is_active=True).first()
             product.package_photo = attachment_path
             product.save()
            
             data=SettingsBuilders.get_vilcom_package_data(id=product.uuid)
             return info.return_type.graphene_type(response=ResponseObject.get_response('1'), data=data)

        elif input.product_type == ProductTypeEnum.user_value_:
             product = UsersProfiles.objects.filter(profile_unique_id=input.product_id,is_active=True).first()
             product.profile_photo = attachment_path
             product.save()

             data=UserAccountBuilder.get_user_profile_data(id=product.uuid)
             return info.return_type.graphene_type(response=ResponseObject.get_response('1'), data=data)



class UploadSingleFileMutation(graphene.Mutation):
    class Arguments:
        input = Base64StringInputObjects()

    response = graphene.Field(ResponseObject)
    attachment_path = graphene.String()

    @classmethod
    def mutate(self, root, info, input):
        response_by = UserUtils.__profile__(info.context.headers)
        if input.base64_string is None:
            return self(response=ResponseObject.get_response(id='4'), data=None)
        
        allowed_images_for_upload = ["jpeg", "jpg", "png"]
        allowed_documents_for_upload = ["docs", "xls", "pdf","txt", "doc"]
        allowed_videos_for_upload = ["mp4", "webm", "gif"]
        
        decoded_data = base64.b64decode(input.base64_string)
        file_type = magic.from_buffer(decoded_data,mime=True)
        file_extension = mimetypes.guess_extension(file_type)

        if file_extension is None:
            return self(response=ResponseObject.get_response(id='4'), data=None)
        
        parent_folder="documents"
        if file_extension.replace('.','') in allowed_images_for_upload:
            parent_folder="images"

        elif file_extension.replace('.','') in allowed_documents_for_upload:
            parent_folder="documents"

        elif file_extension.replace('.','') in allowed_videos_for_upload:
            parent_folder="videos"
        else:
            return self(response=ResponseObject.get_response(id='4'), data=None)
        
        attachment_path = UploadFile.base64_related(input,file_extension,parent_folder, response_by)

        return info.return_type.graphene_type(response=ResponseObject.get_response('1'), attachment_path=attachment_path)

        
        

class Mutation(graphene.ObjectType):
    upload_file=UploadFileMutation.Field()
    upload_related_file=UploadSingleFileMutation.Field()
