"use client";
import Link from "next/link";
import { cardProps } from "../lib/mock_data";
import Navbar from "../components/navbar";

export default function Home() {
  const list = cardProps;

  return (
    <>
      <Navbar />
      <div className="bg-white">
        <div className="bg-slate-500 pt-2 pb-2 mt-3 mb-3">
          <h1 className="text-4xl text-center text-white ">Food Category</h1>
        </div>

        <div className="bg-white gap-4 grid grid-cols-2 sm:grid-cols-4 pt-2 pl-2 pr-2 pb-2">
          {list.map((item) => (
            <div key={item._id} className="bg-white rounded-lg shadow-lg">
              <div className="overflow-hidden">
                {/* Make sure the image scales correctly /} */}
                <img
                  src={item.img}
                  alt={item.title}
                  className="w-full h-48 object-cover rounded-t-xl"
                />
              </div>
              {/* {/ Ensure footer sticks to the bottom */}
              <Link href={`/food_item/category/${item._id}`}>
                <div className="p-4 bg-cyan-400 text-white flex justify-between items-center rounded-b-xl">
                  <span className="font-bold">{item.title}</span>
                </div>
              </Link>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}
