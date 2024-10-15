"use client"
import FoodCard from "../../../components/food_card";
import api from "../../../lib/api";
import { FoodItemCategory } from "../../../lib/type";
import { useEffect, useState } from "react";

async function getFoodItems(category: string, sortBy: string, sortOrder: string): Promise<FoodItemCategory[]> {
  if (category === "chocolate") {
    const [data1, data2] = await Promise.all([
      api.get("/food_items/category/chocolate").then((response) => response.data),
      api.get("/food_items/category/toffee").then((response) => response.data),
    ]);
    return [...data1, ...data2];
  }

  const res = await api
    .get(`/food_items/category/${category}`, {
      params: {
        sort_by: sortBy,
        sort_order: sortOrder,
      },
    })
    .then((response) => response.data);
  
  return res;
}

export default function CategoryPage({
  params: { category },
}: {
  params: { category: string };
}) {
  const [items, setItems] = useState<FoodItemCategory[]>([]);
  const [sortBy, setSortBy] = useState("item_name");
  const [sortOrder, setSortOrder] = useState("asc");

  useEffect(() => {
    async function fetchItems() {
      const items = await getFoodItems(category, sortBy, sortOrder);
      setItems(items);
    }
    fetchItems();
  }, [category, sortBy, sortOrder]);

  const handleSortChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSortBy(e.target.value);
  };

  const handleSortOrderChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSortOrder(e.target.value);
  };

  return (
    <div className="mt-5">
      <div className="flex justify-left mb-4 text-black">
        <a className=" rounded-md border border-black">
        <select value={sortBy} onChange={handleSortChange}>
          <option value="item_name">Nutrient</option>
          <option value="nutrition.protein">Protein</option>
          <option value="nutrition.energy">Energy</option>
          <option value="nutrition.sodium">Sodium</option>
          <option value="nutrition.total_sugar">Sugar</option>
          <option value="nutrition.fat">Fat</option>
          {/* Add more options as needed */}
        </select>
        </a>
        <a className="rounded-md border border-black">
        <select value={sortOrder} onChange={handleSortOrderChange}>
          <option value="asc">Ascending</option>
          <option value="desc">Descending</option>
        </select>
        </a>
      </div>
      <div className="grid grid-cols-4">
        {items.map((item) => (
          <FoodCard food_item={item} key={item._id}></FoodCard>
        ))}
      </div>
    </div>
  );
}