import enum
import graphene

class UserProfileInum(enum.Enum):
    ADMIN_PROFILE = 'ADMIN_PROFILE',
    NORMAL_PROFILE = 'NORMAL_PROFILE'

UserProfileEnum = graphene.Enum.from_enum(UserProfileInum)

class GenderTypeInum(enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    NONE = "NONE"

GenderEnum = graphene.Enum.from_enum(GenderTypeInum)

class ProfileLevelInum(enum.Enum):
    REGION = "REGION"
    DISTRICT = "DISTRICT"

ProfileLevelEnum = graphene.Enum.from_enum(ProfileLevelInum)

class RelationShipInum(enum.Enum):
    Mother  = 'Mother'
    Father = 'Father'
    Auncle  = 'Auncle'
    Aunt = 'Aunt'
    Brother = 'Brother'
    Sister ='Sister'

RelationShipEnum = graphene.Enum.from_enum(RelationShipInum)

class VehicleTypeInum(enum.Enum):
    Cars ='Cars'
    ThreeWheelers ='ThreeWheelers'
    Motorcycles ='Motorcycles'

VehicleTypeEnum = graphene.Enum.from_enum(VehicleTypeInum)

class TransmissionCategoryInum(enum.Enum):
    Automatic = 'Automatic'
    Manual = 'Manual'

TransmissionCategoryEnum = graphene.Enum.from_enum(TransmissionCategoryInum)

class VehicleUsageCategoryInum(enum.Enum):
    Personal = 'Personal'
    Commercial = 'Commercial'

VehicleUsageCategoryEnum = graphene.Enum.from_enum(VehicleUsageCategoryInum)

class VehicleClassificationInum(enum.Enum):
    Passengers = 'Passengers'
    Goods = 'Goods'

VehicleClassificationEnum = graphene.Enum.from_enum(VehicleClassificationInum)

class OrderStatusInum(enum.Enum):
    Pending = "Pending"
    Confirmed = "Confirmed"
    Preparing = "Preparing"
    Out_For_Delivery = "Out_For_Delivery"
    Delivered = "Delivered"
    Cancelled = "Cancelled"

OrderStatusEnum = graphene.Enum.from_enum(OrderStatusInum)

class PaymentStatusInum(enum.Enum):
    Pending = "Pending"
    Completed = "Completed"
    Failed = "Failed"
    Refunded = "Refunded"

PaymentStatusEnum = graphene.Enum.from_enum(PaymentStatusInum)

class PaymentMethodInum(enum.Enum):
    Cash = "Cash"
    Card = "Card"
    MobileMoney = "MobileMoney"
    Online = "Online"

PaymentMethodEnum = graphene.Enum.from_enum(PaymentMethodInum)

class PaymentTypeInum(enum.Enum):
    Full = "Full"
    Partial = "Partial"
      
PaymentTypeEnum = graphene.Enum.from_enum(PaymentTypeInum)

class SmsDeliveryStatusInum(enum.Enum):
    ENROUTE = "ENROUTE"
    DELIVERED = "DELIVERED"
    ACCEPTED = "ACCEPTED"

SmsDeliveryStatusEnum = graphene.Enum.from_enum(SmsDeliveryStatusInum)

class SystemTypeInum(enum.Enum):
    HUDUMA_SMS = "HUDUMA_SMS"
    VILCOM = "VILCOM"
      
SystemTypeEnum = graphene.Enum.from_enum(SystemTypeInum)


