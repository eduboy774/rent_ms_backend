# Rental Management System – Design Model

## 1. Domain (Logical) Model

### 1.1 Core Entities

**User**

* id (UUID)
* username
* email (unique)
* password_hash
* phone_number
* phone_verified
* role (user/admin)
* created_at, updated_at

**House**

* id (UUID)
* owner_id (FK → User)
* name, address, description
* created_at, updated_at

**Room**

* id (UUID)
* house_id (FK → House)
* name/number
* capacity
* price_per_night
* created_at, updated_at

**RoomRental (Short-term)**

* id (UUID)
* room_id (FK → Room)
* renter_id (FK → User)
* period (DATERANGE [start, end))
* status (booked/cancelled/completed)
* created_at

**HouseRental (Short-term)**

* id (UUID)
* house_id (FK → House)
* renter_id (FK → User)
* period (DATERANGE)
* status
* created_at

**Contract (Long-term)**

* id (UUID)
* house_id (FK → House)
* room_id (FK → Room, nullable)
* owner_id (FK → User)
* tenant_id (FK → User)
* period (DATERANGE)
* term_months
* monthly_rent
* deposit_amount
* billing_frequency
* auto_renew
* notice_period_days
* status (pending/active/expired/terminated)
* expired_at, terminated_at
* created_at

**Notification**

* id (UUID)
* user_id (FK → User)
* medium (sms/email)
* payload (JSONB)
* status (pending/sent/failed)
* attempts
* error_message
* created_at, sent_at

**Payment (Outline)**

* id (UUID)
* reference_type (contract/rental)
* reference_id
* amount, currency
* provider
* provider_ref
* status
* created_at

---

## 2. ER Model (Conceptual)

```
USERS ||--o{ HOUSES : owns
HOUSES ||--o{ ROOMS : has
ROOMS ||--o{ ROOM_RENTALS : booked
HOUSES ||--o{ HOUSE_RENTALS : booked
USERS ||--o{ ROOM_RENTALS : rents
USERS ||--o{ HOUSE_RENTALS : rents
HOUSES ||--o{ CONTRACTS : subject
ROOMS ||--o{ CONTRACTS : subject
USERS ||--o{ CONTRACTS : tenant
USERS ||--o{ NOTIFICATIONS : receives
```

---

## 3. Behavioral Models

### 3.1 Contract Lifecycle (State Model)

```
[Pending]
   |
   | activate
   v
[Active] ---- terminate ----> [Terminated]
   |
   | end_date reached (expire_contracts)
   v
[Expired]
```

Rules:

* Only **Active** contracts are checked for expiry.
* Expired contracts are immutable except for audit fields.

---

## 4. Sequence Diagrams (Key Flows)

### 4.1 Short-Term Room Booking

```
Renter -> API : POST /room-rentals
API -> DB : INSERT room_rental (transaction)
DB -> DB : EXCLUDE constraint check
DB --> API : success | conflict
API --> Renter : 201 Created | 409 Conflict
```

### 4.2 Long-Term Contract Creation

```
Tenant -> API : POST /contracts
API -> DB : BEGIN
API -> DB : check overlaps (trigger/exclusion)
DB --> API : ok
API -> DB : INSERT contract (status=active)
API -> DB : COMMIT
API --> Tenant : 201 Created
```

### 4.3 Contract Expiration & SMS

```
Scheduler -> DB : expire_contracts()
DB -> DB : UPDATE contracts SET status=expired
DB -> DB : INSERT notifications (pending)
Worker -> DB : SELECT notifications FOR UPDATE SKIP LOCKED
Worker -> SMS Provider : send SMS
SMS Provider --> Worker : success/failure
Worker -> DB : UPDATE notification status
```

---

## 5. Component (Deployment) Model

```
[ Web / Mobile Client ]
          |
          v
[ API Server ] -- JWT/Auth --> [ PostgreSQL DB ]
          |
          | enqueue
          v
[ Notification Worker ] --> [ SMS Provider ]

[ Scheduler / Cron ] --> calls expire_contracts()
```

---

## 6. Key Design Decisions

* **PostgreSQL DATERANGE + EXCLUDE constraints** for strong consistency.
* **Triggers** only enforce rules, never call external services.
* **Asynchronous notifications** via DB queue + worker.
* **Room vs House contracts** distinguished by nullable room_id.

---

## 7. Extension Points

* Add Email or WhatsApp notifications via medium enum.
* Add partitioning on contracts/notifications for scale.
* Integrate payment gateways without altering core booking logic.

---

## 8. Mapping to SRS

* FR-003 → RoomRental, HouseRental models + exclusion constraints
* FR-004 → Contract model + lifecycle state machine
* FR-006 → Scheduler + expire_contracts()
* FR-007 → Notification + Worker sequence

---

**This design model directly implements the SRS and is suitable for implementation, review, and architecture approval.**
