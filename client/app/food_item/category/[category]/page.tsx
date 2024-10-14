import FoodCard from "../../../components/food_card";
import api from "../../../lib/api";
import { FoodItemCategory } from "../../../lib/type";

async function getFoodItems(category: string): Promise<FoodItemCategory[]> {
  if (category == "chocolate" || category == "toffee") {
    const [data1, data2] = await Promise.all([
      await api
        .get("/food_items/category/chocolate")
        .then((response) => response.data),
      await api
        .get("/food_items/category/toffee")
        .then((response) => response.data),
    ]);
    return [...data1, ...data2];
  }
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
