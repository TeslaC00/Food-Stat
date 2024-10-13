export interface CardProp {
  _id: string;
  title: string;
  img: string;
}

export interface Fetchy {
  _id: string;
  item_category: string;
  item_name: string;
  image_url: string;
}
export interface FoodItem {
  _id: string;
  item_name: string;
  item_category: string;
  image_url: string;
  final_rating: number;
  health_impact_rating: number;
  ingredient_quality_rating: number;
  nutritional_content_rating: number;
}
