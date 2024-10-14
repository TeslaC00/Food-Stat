"use client";
import Link from "next/link";
import { Image } from "@nextui-org/image";
import axios from "axios";
import { cardProps } from "./lib/mock_data";

async function fetchItem(url: string) {
  const data = await axios.get(url).then((response) => response.data);
  return data;
}

async function concation() {
  const [data1, data2] = await Promise.all([
    fetchItem("http://127.0.0.1:5000//api/food_items/chocolate"),
    fetchItem("http://127.0.0.1:5000//api/food_items/toffee"),
  ]);
  const chokielate = [...data1, ...data2];
  return chokielate;
}

export default function Home() {
  const vari = concation();
  console.log(vari);

  const list = cardProps;

  return (
    <div className="bg-white">
      <div className=" mt-0 mb-0 pt-0 pb-0 m-2">
        <Image
          src="/image2.jpg"
          alt="Image"
          width="100%"
          height={700}
          className="w-full rounded-xl mt-2"
          style={{ objectFit: "cover" }}
        />
      </div>

      <div className="bg-slate-500 pt-2 pb-2 mt-3 mb-3">
        <h1 className="text-4xl text-center text-white ">Food Category</h1>
      </div>

      <div className="bg-white gap-4 grid grid-cols-2 sm:grid-cols-4 pt-2 pl-2 pr-2 pb-2">
        {list.map((item, index) => (
          <div key={index} className="bg-white rounded-lg shadow-lg">
            <div className="overflow-hidden">
              {/* Make sure the image scales correctly */}
              <img
                src={item.img}
                alt={item.title}
                className="w-full h-48 object-cover rounded-t-xl"
              />
            </div>
            {/* Ensure footer sticks to the bottom */}
            <Link href={`/${item._id}`}>
              <div className="p-4 bg-cyan-400 text-white flex justify-between items-center rounded-b-xl">
                <span className="font-bold">{item.title}</span>
              </div>
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
}
