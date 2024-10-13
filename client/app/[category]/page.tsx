import FoodCard from "../components/food_card";
import api from "../lib/api";
import { FoodItem } from "../lib/type";

async function getFoodItems(category: string): Promise<FoodItem[]> {
  const res = await api
    .get(`/food_items/${category}`)
    .then((response) => response.data);
  return res;
}

export default async function CategoryPage({
  params: { category },
}: {
  params: { category: string };
}) {
  const items = await getFoodItems(category);

  return (
    <div className="">
      <div className="grid grid-cols-4">
        {items.map((item) => (
          <FoodCard food_item={item} key={item._id}></FoodCard>
        ))}
      </div>
    </div>
  );
}
