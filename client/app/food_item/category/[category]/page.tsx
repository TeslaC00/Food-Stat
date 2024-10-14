import FoodCard from "../../../components/food_card";
import api from "../../../lib/api";
import { FoodItemCategory } from "../../../lib/type";

async function getFoodItems(category: string): Promise<FoodItemCategory[]> {
  const res = await api
    .get(`/food_items/category/${category}`)
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
    <div className=" mt-5">
      <div className="grid grid-cols-4 ">
        {items.map((item) => (
          <FoodCard food_item={item} key={item._id}></FoodCard>
        ))}
      </div>
    </div>
  );
}
