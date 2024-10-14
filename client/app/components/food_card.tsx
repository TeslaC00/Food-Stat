import { Card, CardBody, CardFooter } from "@nextui-org/card";
import { Image } from "@nextui-org/image";
import { FoodItem } from "../lib/type";

export default function FoodCard({ food_item }: { food_item: FoodItem }) {
  return (
    <Card>
      <CardBody>
        <Image
          alt={`picture of ${food_item.item_name}`}
          src={food_item.image_url}
          width={250}
          height={250}
        />
      </CardBody>
      <CardFooter className="flex flex-wrap justify-center">
        <p>{food_item.item_name}</p>
        {/* <p>Heatlh Rating:{food_item.health_impact_rating}</p>
        <p>Ingredient Rating:{food_item.ingredient_quality_rating}</p>
        <p>Nutritional Rating:{food_item.nutritional_content_rating}</p> */}
        <p>Final Rating:{food_item.final_rating}</p>
      </CardFooter>
    </Card>
  );
}
