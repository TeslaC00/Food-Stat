import { Card, CardBody, CardFooter } from "@nextui-org/card";
import { Image } from "@nextui-org/image";
import { FoodItem } from "../lib/type";

export default function FoodCard({ food_item }: { food_item: FoodItem }) {
  return (
    
    <Card className="rounded-xl m-2 bg-slate-400 border-2 border-gray-400">
      <CardBody>
        <div className="">
        <Image
          alt={`picture of ${food_item.item_name}`}
          src={food_item.image_url}
          width={250}
          height={250}
          
        />
        </div>
      </CardBody>
      <CardFooter className="flex flex-wrap justify-center text-black">
        <a>{food_item.item_name}</a>
        {/* <p>Heatlh Rating:{food_item.health_impact_rating}</p>
        <p>Ingredient Rating:{food_item.ingredient_quality_rating}</p>
        <p>Nutritional Rating:{food_item.nutritional_content_rating}</p> */}
        <a className="">Rating: <span className="text-green-400">{food_item.final_rating}</span></a>
      </CardFooter>
    </Card>
    
  );
}
