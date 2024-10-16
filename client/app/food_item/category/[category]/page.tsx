"use client";
import Navbar from "@/app/components/navbar";
import FoodCard from "../../../components/food_card";
import api from "../../../lib/api";
import { FoodItemCategory, Profile } from "../../../lib/type";
import { useEffect, useState } from "react";

// Function to get food items based on the toggle state and sorting parameters
async function getFoodItems(
  category: string,
  sortBy: string,
  sortOrder: string,
  toggle: boolean
): Promise<FoodItemCategory[]> {
  const profileId = localStorage.getItem("user_profile_id");
  // Handle case for chocolate and toffee categories together
  if (category === "chocolate" || category === "toffee") {
    if (toggle) {
      const [chocolateData, toffeeData] = await Promise.all([
        api
          .get(`/food_items/category/chocolate/filter/${profileId}`, {
            params: { sort_by: sortBy, sort_order: sortOrder },
          })
          .then((response) => response.data),
        api
          .get(`/food_items/category/toffee/filter/${profileId}`, {
            params: { sort_by: sortBy, sort_order: sortOrder },
          })
          .then((response) => response.data),
      ]);
      return [...chocolateData, ...toffeeData];
    } else {
      const [chocolateData, toffeeData] = await Promise.all([
        api
          .get(`/food_items/category/chocolate`, {
            params: { sort_by: sortBy, sort_order: sortOrder },
          })
          .then((response) => response.data),
        api
          .get(`/food_items/category/toffee`, {
            params: { sort_by: sortBy, sort_order: sortOrder },
          })
          .then((response) => response.data),
      ]);
      return [...chocolateData, ...toffeeData];
    }
  } else {
    // Handle all other categories
    if (toggle) {
      const res = await api
        .get(`/food_items/${category}/filter/${profileId}`, {
          params: {
            sort_by: sortBy,
            sort_order: sortOrder,
          },
        })
        .then((response) => response.data);
      return res;
    } else {
      const res = await api
        .get(`/food_items/category/${category}`, {
          params: {
            sort_by: sortBy,
            sort_order: sortOrder,
          },
        })
        .then((response) => response.data);
      return res;
    }
  }
}

async function getUserProfile(): Promise<Profile | null> {
  const user_id = localStorage.getItem("user_profile_id");
  if (user_id) {
    const data = await api
      .get(`/profiles/${user_id}`)
      .then((response) => response.data);
    return data;
  }
  return null;
}

async function ifAllergic(
  food_item: FoodItemCategory,
  is_personalised: boolean
): Promise<string | undefined> {
  const user_profile = await getUserProfile();
  if (!is_personalised || !user_profile) {
    return undefined;
  }
  const allergy_info = user_profile.allergy_info;
  for (const allergy of allergy_info || []) {
    if (food_item.allergy_info?.includes(allergy)) {
      return "Yes"; // Return "Yes" if allergic
    }
  }
  return "No";
}

function isRecom(item: FoodItemCategory) {
  if (item.personalised_score > 3.5) {
    return "Good";
  } else if (item.personalised_score > 2) {
    return "Ok";
  } else {
    return "Bad";
  }
}

export default function CategoryPage({
  params: { category },
}: {
  params: { category: string };
}) {
  const [items, setItems] = useState<FoodItemCategory[]>([]);
  const [sortBy, setSortBy] = useState("item_name");
  const [sortOrder, setSortOrder] = useState("asc");
  const [isPersonalized, setIsPersonalized] = useState(false); // Toggle state
  const [allergyInfo, setAllergyInfo] = useState<{
    [key: string]: string | undefined;
  }>({});

  useEffect(() => {
    async function fetchAllergyInfo() {
      if (isPersonalized) {
        const info: { [key: string]: string | undefined } = {};
        for (const item of items) {
          info[item._id] = await ifAllergic(item, isPersonalized);
        }
        setAllergyInfo(info);
      } else {
        setAllergyInfo({}); // Clear allergy info when not personalized
      }
    }

    fetchAllergyInfo();
  }, [items, isPersonalized]);

  useEffect(() => {
    async function fetchItems() {
      const items = await getFoodItems(
        category,
        sortBy,
        sortOrder,
        isPersonalized
      );
      setItems(items);
    }
    fetchItems();
  }, [category, sortBy, sortOrder, isPersonalized]);

  // Handler for sort change
  const handleSortChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSortBy(e.target.value);
  };

  // Handler for sort order change
  const handleSortOrderChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSortOrder(e.target.value);
  };

  // Handler for toggle change
  const handleToggleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setIsPersonalized(e.target.checked);
  };

  return (
    <>
      <Navbar />
      <div className="mt-5">
        <div className="flex justify-left mb-4 text-black m-2">
          {/* Sort By Dropdown */}
          <a className="rounded-md border border-black m-1 bg-amber-200">
            <select value={sortBy} onChange={handleSortChange}>
              <option value="item_name">Nutrient</option>
              <option value="nutrition.protein">Protein</option>
              <option value="nutrition.energy">Energy</option>
              <option value="nutrition.sodium">Sodium</option>
              <option value="nutrition.carbohydrates">Carbohydrates</option>
              <option value="nutrition.total_sugar">Sugar</option>
              <option value="nutrition.fat">Fat</option>
              {/* Add more options as needed */}
            </select>
          </a>

          {/* Sort Order Dropdown */}
          <a className="rounded-md border border-black m-1 bg-amber-200">
            <select value={sortOrder} onChange={handleSortOrderChange}>
              <option value="asc">Ascending</option>
              <option value="desc">Descending</option>
            </select>
          </a>

          {/* Toggle for personalized API */}
          <a className="rounded-md border border-black m-1 bg-amber-200 flex items-center">
            <label htmlFor="personalizedToggle" className="ml-1 mr-1">
              Personalized
            </label>
            <input
              id="personalizedToggle"
              type="checkbox"
              checked={isPersonalized}
              onChange={handleToggleChange}
            />
          </a>
        </div>

        {/* Display Food Items */}
        <div className="grid grid-cols-4">
          {items.map((item) =>
            !isPersonalized ? (
              <FoodCard
                food_item={item}
                key={item._id}
                allergy_info=""
                recom=""
                isPersonalised={isPersonalized}
              ></FoodCard>
            ) : (
              <FoodCard
                food_item={item}
                key={item._id}
                isPersonalised={isPersonalized}
                allergy_info={
                  isPersonalized ? allergyInfo[item._id] : undefined
                }
                recom={isPersonalized ? isRecom(item) : "Not Applicable"}
              ></FoodCard>
            )
          )}
        </div>
      </div>
    </>
  );
}
