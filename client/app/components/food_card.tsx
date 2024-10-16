import { Card, CardBody ,CardFooter} from "@nextui-org/card";
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
      <CardBody className="flex flex-col items-center justify-center">
        {/* Image Container */}
        <div className="bg-white flex justify-center items-center rounded-lg">
          <Link href={`/food_item/${food_item._id}`}>
            <Image
              alt={`picture of ${food_item.item_name}`}
              src={food_item.image_url}
              width={250}
              height={250}
              className="object-contain rounded-lg"
            />
          </Link>
        </div>
        {/* Text Content */}
        <div className="text-black text-center mt-2">
          <a className="font-bold text-lg">{food_item.item_name}</a>
        </div>
      </CardBody>
      <CardFooter className="flex flex-wrap justify-center text-black">
        
        <a className="font-semibold">
          Rating:{" "}
          <span className="text-black font-semibold">{food_item.final_rating}</span>
        </a>
        {/* Render allergy and recommendation info only if personalized */}
        {isPersonalised && (
          <>
            {/* Allergy Info Label */}
            {allergy_info === "Yes" ? (
              <span className="ml-2 text-red-900 font-bold">Allergic</span>
            ) : allergy_info === "No" ? (
              <span className="ml-2 text-green-900 font-bold">
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
