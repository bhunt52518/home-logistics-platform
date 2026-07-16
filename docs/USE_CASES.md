# Use Cases

## UC-001: Add Groceries from a Receipt

### Goal

Update household inventory by scanning a grocery receipt after a shopping trip.

### Primary Actor

Household User

### Trigger

The user returns from grocery shopping and chooses to scan a receipt.

### Preconditions

- The user belongs to a Household.
- The Household has at least one Pantry.
- The Pantry has one or more Locations.
- The receipt image is readable.

### Main Flow

1. The user selects **Scan Receipt**.
2. The user photographs or uploads the receipt.
3. The system extracts the purchased products, quantities, prices, and purchase date.
4. The system attempts to match each receipt line to an existing Item.
5. The system displays the interpreted receipt for review.
6. The user corrects any missing or incorrectly identified products.
7. The user selects a storage Location for each product.
8. The user optionally enters expiration dates or confirms suggested dates.
9. The user approves the import.
10. The system creates or updates Inventory Records.
11. The system records the purchase details.
12. The system displays a summary of the inventory changes.

### Split Location Flow

1. The system suggests a primary storage Location for each purchased Item.
2. The user may accept the suggested Location or choose **Split Across Locations**.
3. The user assigns a quantity and unit to each selected Location.
4. The system validates that the allocated quantities equal the purchased quantity.
5. The system creates a separate Inventory Record for each Location.
6. The inventory update is applied only after the user confirms the allocation.

### Success Criteria

- Purchased products are identified.
- The user reviews all changes before inventory is updated.
- Existing Items are reused when appropriate.
- New Items can be created when no match exists.
- Inventory Records are assigned to Locations.
- Quantities and purchase information are recorded.
- The original receipt can be referenced later.

### Alternative Flows

#### Receipt Cannot Be Read

The system informs the user that the receipt could not be processed and allows another image to be uploaded or the products to be entered manually.

#### Product Cannot Be Identified

The system marks the receipt line as unmatched and asks the user to select an existing Item or create a new Item.

#### Product Already Exists in the Location

The system either updates the existing Inventory Record or creates a separate record when expiration date, opened status, or purchase batch differs.

#### One Product Is Stored in Multiple Locations

The user splits the purchased quantity between two or more Locations before confirming the import.

### Questions

- Should the receipt image be stored?
- Should inventory changes always require user approval?
- How should abbreviated receipt names be matched to Items?
- Should expiration dates be entered manually, suggested, or omitted?
- Should taxes, discounts, and coupons be recorded?
- Should the system support returns and refunded products?
- Should shopping-list items be automatically marked complete?