import { Card, CardBody, CardFooter } from "@nextui-org/card";
import { Image } from "@nextui-org/image";
import { FoodItemCategory } from "../lib/type";
import Link from "next/link";

interface FoodCardProps {
  food_item: FoodItemCategory;
  allergy_info?: string;
  recom: string;
  isPersonalised: boolean;
}

export default function FoodCard({
  food_item,
  allergy_info,
  recom,
  isPersonalised,
}: FoodCardProps) {
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
        {/* Render allergy and recommendation info only if personalized */}
        {isPersonalised && (
          <>
            {/* Allergy Info Label */}
            {allergy_info === "Yes" ? (
              <span className="ml-2 text-red-500 font-bold">Allergic</span>
            ) : allergy_info === "No" ? (
              <span className="ml-2 text-green-500 font-bold">
                Not Allergic
              </span>
            ) : null}

            {/* Recommendation Label */}
            <span
              className={`ml-2 font-bold ${
                recom === "Good"
                  ? "text-green-500"
                  : recom === "Ok"
                  ? "text-yellow-500"
                  : "text-red-500"
              }`}
            >
              {recom === "Bad" ? `Not Recommended` : `Recommended: ${recom}`}
            </span>
          </>
        )}
      </CardFooter>
    </Card>
  );
}
