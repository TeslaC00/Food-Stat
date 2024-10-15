import Navbar from "@/app/components/navbar";
import api from "@/app/lib/api";
import { FoodItem } from "@/app/lib/type";
import { Image } from "@nextui-org/image";

async function GetFoodItem(id: string): Promise<FoodItem> {
  const data = await api
    .get(`/food_items/${id}`)
    .then((response) => response.data);
  return data;
}

export default async function ItemPage({
  params: { item_id },
}: {
  params: { item_id: string };
}) {
  const foodItem = await GetFoodItem(item_id);

  return (
    <>
      <Navbar />
      <div>
        <div className="flex">
          <div>
            <Image
              src={foodItem.image_url}
              alt="Food Item Image"
              className="w-1/4 h-1/4"
            />
          </div>
          <div className="text-black">
            <h2 className="text-xl font-bold mb-2">{foodItem.item_name}</h2>
            <p>Category: {foodItem.item_category}</p>
            <p>Final Rating: {foodItem.final_rating}</p>
            <p>Health Impact Rating: {foodItem.health_impact_rating}</p>
            <p>
              Ingredient Quality Rating: {foodItem.ingredient_quality_rating}
            </p>
            <p>
              Nutritional Content Rating: {foodItem.nutritional_content_rating}
            </p>
            <div>
              <h3>Nutrition:</h3>
              {foodItem.nutrition ? (
                <ul>
                  {Object.keys(foodItem.nutrition).map((key) => (
                    <li key={key}>{`${key}: ${foodItem.nutrition[key]}`}</li>
                  ))}
                </ul>
              ) : (
                <p>None</p>
              )}
            </div>
            <div>
              <h3>Ingredients:</h3>
              <ul>
                {foodItem.ingredients.map((ingredient, index) => (
                  <li key={index}>{ingredient}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
        <div className="flex-1"></div>
      </div>
    </>
  );
}
