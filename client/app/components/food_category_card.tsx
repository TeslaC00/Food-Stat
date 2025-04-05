import { Card, CardBody, CardFooter, Image } from "@heroui/react";
import Link from "next/link";

interface FoodCategoryCardProps {
  categoryTitle: string;
  categoryImg: string;
  categoryId: string;
}

export default function FoodCategoryCard({
  categoryTitle,
  categoryImg,
  categoryId,
}: FoodCategoryCardProps) {
  return (
    <Card>
      <CardBody className="p-0">
        <Image
          alt={categoryTitle}
          className="object-cover h-48 rounded-t-lg"
          src={categoryImg}
          shadow="lg"
          width="100%"
        />
      </CardBody>
      <Link href={`/food_item/category/${categoryId}`}>
        <CardFooter className="text-base pl-4 pt-2 pb-3 rounded-b-xl bg-cyan-500 text-wrap">
          <b>{categoryTitle}</b>
        </CardFooter>
      </Link>
    </Card>
  );
}
