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
export interface FoodItemCategory {
  _id: string;
  item_name: string;
  item_category: string;
  image_url: string;
  final_rating: number;
  allergy_info: string[] | null;
  personalised_score: number;
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
  nutrition?: { [key: string]: number };
  ingredients: string[];
}

export interface Profile {
  _id: string;
  account_id: string;
  userType: string;
  profile_name: string;
  firstName: string;
  lastName: string;
  gender: string;
  weight: number;
  height: number;
  age: number;
  dietType: string;
  allergy_info: string[] | null;
  diseases: string[] | null;
}
