import uuid
import names

from datetime import datetime

portion_amounts = {
    "L": 0.5,
    "N": 1,
    "D": 2,
}

def generate_list_of_entrees(csv_row, portion_type, default_portions):
    quantity = (
        int(csv_row["Quantity"])
        if csv_row["Quantity"].isnumeric() and int(csv_row["Quantity"]) > 0
        else 1
    )

    order_number = csv_row["Order No."]
    # The ingredients specific in the CSV has the ingredient name followed by a
    # numeric value that represents the ID of the ingredient.

    csv_ingredients = []
    for key, item in csv_row.items():
        if "Order No." in key or "Quantity" in key:
            continue
        # No portion amount provided for the ingredient
        if item == "" or item is None:
            continue

        if key.count("-") < 1:
            print(
                f"Ingredient {key} does not follow the format of ingredientName-externalId so we are skipping that ingredient."
            )
            continue

        [name, external_id] = key.split("-", 1)

        if portion_type == "multiplier":
            if item.upper() not in portion_amounts:
                print(
                    f"The portion amount of {item} given for ingredient {key} in order number {order_number} is not valid. The portion amount should either be N, D, or L."
                )
                continue
            multiplier = portion_amounts[item.upper()]
        if portion_type == "portion":
            try:
                desired_portion = int(item)
            except ValueError:
                print(
                    f"The portion amount of {item} given for ingredient {key} in order number {order_number} is not valid. The portion amount should be a number."
                )
                continue
            ## Find the default portion for the ingredient
            ingredient_default_portion = next(
                (
                    portion
                    for portion in default_portions
                    if portion["ingredient_id"] == external_id
                ),
                None,
            )
            if ingredient_default_portion is None:
                print(
                    f"No default portion found for ingredient {external_id}. Please provide a default portion for this ingredient."
                )
                continue
            multiplier = round(desired_portion / ingredient_default_portion["default_portion"], 3)

        csv_ingredients.append(
            {
                "externalIngredientId": external_id,
                "name": {
                    "full": name,
                },
                "multiplier": multiplier,
            }
        )

    order_items = []
    external_recipe_id = str(uuid.uuid4())

    # Calculate the current time in milliseconds
    now_date = datetime.utcnow() - datetime(1970, 1, 1)
    seconds = now_date.total_seconds()
    milliseconds = round(seconds * 1000)
    for i in range(quantity):
        order_items.append(
            {
                "externalOrderId": order_number,
                "externalRecipeId": external_recipe_id,
                "externalEntreeId": str(uuid.uuid4()),
                "name": {
                    "full": f"Bowl {i+1}-{order_number}",
                },
                "customerName": names.get_full_name(),
                "promiseTimeMs": milliseconds,
                "ingredients": csv_ingredients,
            }
        )

    return order_items