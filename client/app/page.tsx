"use client"
import Link from "next/link";
import { Card, CardHeader, CardBody, CardFooter } from "@nextui-org/card";
import { cardProp, fetchy } from "./type";
// import Image from "next/image";
import {Image} from "@nextui-org/image";
import { useEffect, useState } from "react";
import axios from "axios";

async function fetchItem(url:string){
  const data=await axios.get(url).then((response)=>response.data)
  return data
}

async function concation(){
  const[data1,data2]=await Promise.all([fetchItem("http://127.0.0.1:5000//api/food_items/chocolate"),fetchItem("http://127.0.0.1:5000//api/food_items/toffee")])
  const chokielate=[...data1,...data2]
  return chokielate
}



export default function Home() {

  const vari=concation()
  console.log(vari)

  // const[data1,data2]=await Promise.all([fetchItem("http://127.0.0.1:5000//api/food_items/chocolate"),fetchItem("http://127.0.0.1:5000//api/food_items/toffee")])
  
  const list: cardProp[] = [
    {
      _id: "PROTEIN POWDER",
      title: "Protein Powder",
      img: "/protein.jpg",
    },
    {
      _id: "PEANUT BUTTER",
      title: "Peanut Butter",
      img: "/peanut.jpg",
    },
    {
      title: "Baby Food",
      img: "/baby.jpg",
      _id: "BABY FOOD"
    },
    {
      title: "Chips",
      img: "/chips.jpg",
      _id: "CHIPS"
    },
    {
      title: "Packeted Juice",
      img: "/packetjuice.jpg",
      _id: "PACKETED JUICE"
    },
    {
      title: "Biscuits",
      img: "/biscuit.jpg",
      _id: "biscuit"
    },
    {
      title: "Namkeen",
      img: "/namkeen.jpg",
      _id: "namkeen"
    },
    {
      title: "Packeted Coffee/Lassi/Milkshake",
      img: "/beverages.jpg",
      _id: "coffee"
    },
    {
      title: "Protein Bars",
      img: "/bar.jpg",
      _id: "protein_bar"
    },
    {
      title: "Chocolate",
      img: "/chocolate.jpg",
      _id: "chocolate"
    },
    {
      title: "Toffee",
      img: "/chocolate.jpg",
      _id: "toffee"
    },
    {
      title: "Instant Noodles",
      img: "/noodles.jpg",
      _id: "INSTANT NOODLES"
    },
    {
      title: "Bread",
      img: "/bread.jpg",
      _id: "BREAD"
    },
    {
      title: "Breakfast Spreads",
      img: "/spread.jpg",
      _id: "BREAKFAST SPREADS"
    },
    {
      title: "Bournvita / Horlicks",
      img: "/bournvita.jpg",
      _id: "MILK FLAVOURING"
    },
    {
      title: "Corn Flakes / Muesli",
      img: "/museli.jpg",
      _id: "CORN FLAKES"
    },
  ];
  
  return (
    <div className="bg-white">
      
      <div className="w-screen mt-0 mb-0 pt-0 pb-0">
        <Image
          src="/image2.jpg"
          alt="Image"
          width="100%"
          height={700}
          className="w-full"
          style={{ objectFit: "cover" }}
        />
      </div>

      <div className="bg-slate-500 pt-2 pb-2 mt-3 mb-3">
        <h1 className="text-4xl text-center ">Food Category</h1>
      </div>

        <div className="bg-white gap-4 grid grid-cols-2 sm:grid-cols-4 pt-2 pl-2 pr-2 pb-2">
          {list.map((item, index) => (
            <div key={index} className="bg-gray-900 rounded-lg shadow-lg">
              <div className="overflow-hidden">
                {/* Make sure the image scales correctly */}
                <img
                  src={item.img}
                  alt={item.title}
                  className="w-full h-48 object-cover"
                />
              </div>
              {/* Ensure footer sticks to the bottom */}
              <Link href={{pathname:"/items",query:{ title: item.title },}}>
              <div className="p-4 bg-cyan-400 text-white flex justify-between items-center">
                <span className="font-bold">{item.title}</span>
              </div>
              </Link>
            </div>
          ))}
        </div>
      

    </div>
  );
}
