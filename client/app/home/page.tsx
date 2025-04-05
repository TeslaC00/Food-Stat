"use client";
import { cardProps } from "../lib/mock_data";
import Navbar from "../components/navbar";
import FoodCategoryCard from "../components/food_category_card";

export default function Home() {
  const cardList = cardProps;

  return (
    <div>
      <Navbar />
      <h1 className="text-center text-white text-4xl mt-2 pt-3 pb-3 bg-slate-400">
        Food Category
      </h1>
      <div className="text-black grid grid-cols-4 gap-4 pt-3 pl-3 pr-3">
        {cardList.map(function (cardItem, index) {
          return (
            <FoodCategoryCard
              key={index}
              categoryId={cardItem._id}
              categoryImg={cardItem.img}
              categoryTitle={cardItem.title}
            />
          );
        })}
      </div>
    </div>
  );
}
