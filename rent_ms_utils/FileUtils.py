import base64
import datetime
import logging
import os
import uuid
from base64 import b64decode

from django.conf import settings
from .models import LocationSpacialUnit, SpacialUnit, SpacialUnitTransaction


logger = logging.getLogger(__name__)


class UploadFile:
    @staticmethod
    def base64_handler(input,file_extension,parent_folder):
        # TODO: separate folders by: department, location, or locality
        land_file = SpacialUnit.objects.filter(uuid=input.land_unique_id, is_active=True).first()
        bytes = b64decode(input.base64_string, validate=True)


        land = f"RegNo.{land_file.reg_plan_no}-PlotNo.{land_file.plot_no}-Block.{ None if land_file.block_no is None else land_file.block_no.block_number}-{land_file.locality.locality_name}"

        location_scan = LocationSpacialUnit.objects.filter(spacial_unit=land_file).first()

        new_folder = str(parent_folder)+"/"+location_scan.location.location_region.reginal_name+"/"+ "-" if location_scan.location.location_district is None else location_scan.location.location_district.district_name+"/"+location_scan.location.location_department.department_name+"/"+datetime.datetime.now().strftime("%Y-%m-%d")+"/"+land+"/"+"MANDATORY"
        location = ""

        try:
            os.makedirs(os.path.join(str(settings.MEDIA_ROOT) +"/"+new_folder))
        except:
            pass
        finally:
            location = str(settings.MEDIA_ROOT)+"/"+new_folder

        sting_name = uuid.uuid4()
        absolute_file_path = "{}/{}{}".format(location, sting_name, file_extension)
        relative_file_path = "/{}/{}{}".format(new_folder,sting_name,file_extension)

        new_file = open(str(absolute_file_path), 'wb')
        new_file.write(bytes)
        new_file.close()


        return relative_file_path
    
    def base64_related(input,file_extension,parent_folder, response_by):
        # Get the current date and time
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

        # TODO: separate folders by: department, location, or locality
        spatial = SpacialUnit.objects.filter(uuid=input.spatial_uuid, is_active=True).first()
        
        bytes = b64decode(input.base64_string, validate=True)

        land = f"RegNo.{None if spatial.reg_plan_no is None else spatial.reg_plan_no}-PlotNo.{None if spatial.plot_no is None else spatial.plot_no}-Block.{None if spatial.block_no is None else spatial.block_no.block_number}-{spatial.locality.locality_name}"
        
        location_scan = LocationSpacialUnit.objects.filter(spacial_unit=spatial).first()

        transaction = SpacialUnitTransaction.objects.filter(spatial_unit=spatial).first()
        if transaction is not None:
            transaction.scanning_created_by = response_by
            transaction.scanning_created_at = formatted_time
            transaction.save()
        
        new_folder = str(parent_folder)+"/"+location_scan.location.location_region.reginal_name+"/"+ "-" if location_scan.location.location_district is None else location_scan.location.location_district.district_name+"/"+location_scan.location.location_department.department_name+"/"+datetime.datetime.now().strftime("%Y-%m-%d")+"/"+land+"/"+"OTHERS"
        location = ""

        try:
            os.makedirs(os.path.join(str(settings.MEDIA_ROOT) +"/"+new_folder))
        except:
            pass
        finally:
            location = str(settings.MEDIA_ROOT)+"/"+new_folder

        sting_name = uuid.uuid4()
        absolute_file_path = "{}/{}{}".format(location, sting_name, file_extension)
        relative_file_path = "/{}/{}{}".format(new_folder,sting_name,file_extension)

        new_file = open(str(absolute_file_path), 'wb')
        new_file.write(bytes)
        new_file.close()


        return relative_file_path
    
    def base64_file_data(file_path):
        try:
            logger.info(f"Fetching Attachment/File at {file_path}")
            file_path = "{}{}".format(settings.MEDIA_ROOT, file_path)
            file_read = open(file_path, "rb").read()

            base64_data = base64.b64encode(file_read).decode("utf-8")
            data = '%s' % (base64_data)
            return data

        except Exception as e:
            logger.error(f"Error Occurred in Encoding File to Base64 {e}")
            return None