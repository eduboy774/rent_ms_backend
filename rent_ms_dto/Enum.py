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

class MediumInum(enum.Enum):
    SMS = "Sms"
    EMAIL = "Email"

MediumEnum = graphene.Enum.from_enum(MediumInum)


class SmsStatusInum(enum.Enum):
    PENDING = "Pending"
    SENT = "Sent"
    FAILED = "Failed"

SmsStatusEnum = graphene.Enum.from_enum(SmsStatusInum)



class ContractStatusInum(enum.Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    TERMINATED = "TERMINATED"


ContractStatusEnum = graphene.Enum.from_enum(ContractStatusInum)


class DurationInum(enum.Enum):
    THREE_MONTHS = 3
    SIX_MONTHS = 6
    TWELVE_MONTHS = 12


DurationEnum = graphene.Enum.from_enum(DurationInum)
