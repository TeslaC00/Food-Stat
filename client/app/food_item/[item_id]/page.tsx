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
          {/* Image div with equal width */}
          <div className="flex-1 bg-red-200 content-center ">
            <Image
              src={foodItem.image_url}
              alt="Food Item Image"
              className="w-1/2 h-1/2 object-cover m-10"
            />
          </div>

          {/* Content div with equal width */}
          <div className="flex-1 text-black p-10">
            <h2 className="text-2xl font-extrabold mb-4">{foodItem.item_name}</h2>
            <div className="grid grid-cols-2 gap-4 mb-2">
              <p>
                <a className="font-semibold">Final Rating: {foodItem.final_rating}</a>
              </p>
              <p>
                <a className="font-semibold">Health Impact Rating: {foodItem.health_impact_rating}</a>
              </p>
              <p>
                <a className="font-semibold">
                  Ingredient Quality Rating:{" "}
                  {foodItem.ingredient_quality_rating}
                </a>
              </p>
              <p>
                <a className="font-semibold">
                  Nutritional Content Rating:{" "}
                  {foodItem.nutritional_content_rating}
                </a>
              </p>
            </div>
            <div className="mb-2">
              <h3 className="font-semibold mb-2">Nutrition:</h3>
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
              <h3 className="font-semibold">Ingredients:</h3>
              <ul>
                {foodItem.ingredients.map((ingredient, index) => (
                  <li key={index}>{ingredient}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
