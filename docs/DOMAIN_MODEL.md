## Household

### Purpose

Represents a family or group of people sharing resources, inventory, meal plans, and household settings.

### Examples

- Brent's Family
- Smith Family
- Apartment 4B

### Relationships

Has many Users

Has many Locations

Has many Inventory Items

Has many Shopping Lists

Has many Recipes

### Questions

Should a user belong to more than one household?

Should households share recipes?

## User

### Purpose

Represents a person who interacts with the Home Logistics Platform.

### Examples

- Brent
- Amber
- Emma

### Relationships

Belongs to one Household

Can create Recipes

Can modify Inventory

Can generate Shopping Lists

Can create Meal Plans

### Questions

Can users have different permissions?

Can children view but not edit?

Can guests access shared recipes?


## Pantry

### Purpose

Represents a household-managed collection of food inventory.

A pantry is a logical inventory area rather than a single physical room. It may include items stored in cabinets, a refrigerator, a freezer, or other food-storage locations.

### Examples

- Main Household Pantry
- Garage Food Storage
- Emergency Food Supply

### Attributes

- Name
- Description
- Created Date
- Active Status

### Relationships

- Belongs to one Household
- Contains many Locations
- Consolidates inventory across its Locations

### Questions

- Can one household have multiple pantries?
- Should the refrigerator and freezer be separate pantries or storage locations?
- Can a pantry be archived without deleting its inventory history?


## Item

### Purpose

Represents a type of product or resource that a household may own.

### Examples

- Whole Milk
- Chicken Breast
- Paper Towels
- Dish Soap
- AA Batteries

### Attributes

- Name
- Description
- Default Unit
- Category
- Barcode
- Brand
- Nutritional Information
- Perishable Status

### Relationships

- Belongs to one Category
- Can appear in many Recipes
- Can have many Inventory Records
- Can have many Purchase Records

### Questions

- Can one item have multiple barcodes?
- Should brand-specific products be separate items?
- Should nutritional information come from an external provider?

## Inventory Record

### Purpose

Represents a specific quantity of an item currently owned by a household.

### Examples

- Half a gallon of whole milk in the refrigerator
- Two pounds of frozen chicken breast
- Six rolls of paper towels in the garage
- One opened bottle of dish soap under the sink

### Attributes

- Quantity
- Unit
- Expiration Date
- Purchase Date
- Purchase Price
- Opened Status
- Minimum Quantity
- Lot or Batch Identifier
- Notes

### Relationships

- Belongs to one Location
- References one Item

### Questions

- Can one record be split across locations?
- Should opening an item create a new record?
- Can quantity be fractional?
- Should identical purchases with different expiration dates remain separate?
- How should unknown quantities be represented?

## Recipe

### Purpose

Represents the instructions and ingredients required to prepare a meal or food item.

### Examples

- Lasagna
- Potato Soup
- Smoked Ribs

### Attributes

- Name
- Description
- Instructions
- Preparation Time
- Cooking Time
- Total Time
- Serving Size
- Difficulty
- Source
- Notes
- Favorite Status

### Relationships

- Belongs to one Household
- Has many Recipe Ingredients
- Can appear in many Meal Plans
- Can generate Shopping List Items
- Can be created or imported by a User

### Questions

- Should recipes be private to one household or shareable?
- Can users modify an imported recipe without changing the original?
- Should instructions be stored as one block of text or as ordered steps?
- Can recipes have optional ingredients?
- Should serving sizes automatically scale ingredient quantities?
- Should recipes support substitutions?

## Ingredient

### Purpose

Represents the quantity of an Item required by a Recipe.

### Examples

- 1 cup Chicken Stock
- 1 tbsp Paprika
- 16 oz Macaroni

### Attributes

- Quantity
- Unit
- Preparation Notes
- Optional
- Display Order

### Relationships

- Belongs to one Recipe
- References one Item

### Questions

- Should ingredients support "to taste"?
- Can ingredients be optional?
- Should preparation notes be stored?


## Location

### Purpose

Represents a physical place where household resources are stored.

### Examples

- Kitchen Pantry
- Refrigerator
- Garage Freezer
- Under the Kitchen Sink

### Attributes

- Name
- Description
- Location Type
- Active Status

### Relationships

- Belongs to one Pantry
- Contains many Inventory Records

### Questions

- Can locations contain smaller locations, such as shelves or bins?
- Can one location store both food and non-food items?
- Should inactive locations preserve inventory history?

## Category

### Purpose

Represents a classification used to organize Items.

### Examples

- Dairy
- Meat
- Produce
- Cleaning Supplies
- Household Goods

### Attributes

- Name
- Description
- Active Status

### Relationships

- Contains many Items
- May belong to one Household
- May have one parent Category

### Questions

- Should categories be global or household-specific?
- Should categories support subcategories?
- Can one Item belong to more than one Category?

Expiration
Purchase
Meal Plan
Shopping List
Shopping Item
Store
Barcode
