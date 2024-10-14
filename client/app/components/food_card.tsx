import { Card, CardBody, CardFooter } from "@nextui-org/card";
import { Image } from "@nextui-org/image";
import { FoodItemCategory } from "../lib/type";
import Link from "next/link";

export default function FoodCard({
  food_item,
}: {
  food_item: FoodItemCategory;
}) {
  console.log(food_item._id);

  return (
    <Card className="rounded-xl m-2 bg-slate-400 border-2 border-gray-400">
      <CardBody>
        <div className="">
          <Link href={`/food_item/${food_item._id}`}>
            <Image
              alt={`picture of ${food_item.item_name}`}
              src={food_item.image_url}
              width={250}
              height={250}
            />
          </Link>
        </div>
      </CardBody>
      <CardFooter className="flex flex-wrap justify-center text-black">
        <a>{food_item.item_name}</a>
        <a className="">
          Rating:{" "}
          <span className="text-green-400">{food_item.final_rating}</span>
        </a>
      </CardFooter>
    </Card>
  );
}
