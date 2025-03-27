import { useState } from "react";
import api from "../lib/api";

export default function Form() {
  const [nutrition, setNutrition] = useState({
    "NUTRITION.ENERGY": 0,
    "NUTRITION.PROTEIN": 0,
    "NUTRITION.CARBOHYDRATE": 0,
    "NUTRITION.TOTAL_SUGARS": 0,
    "NUTRITION.ADDED_SUGARS": 0,
    "NUTRITION.TOTAL_FAT": 0,
    "NUTRITION.SATURATED_FAT": 0,
    "NUTRITION.FIBER": 0,
    "NUTRITION.SODIUM": 0,
  });

  const [rating, setRating] = useState<number>(0); // Add this line to store the rating

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setNutrition({ ...nutrition, [name]: parseFloat(value) });
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    await api
      .post("/food_items/rating", nutrition) // Make a POST request to the API
      .then((response) => {
        setRating(response.data.Rating); // Update the rating state
      })
      .catch((error) => {
        console.error(error);
      });
  };

  return (
    <div className="text-black ">
      <div className="flex justify-center">
        <h2 className="font-semibold mb-2">NUTRITION FORM</h2>
      </div>
      <div className="grid grid-cols-2 gap-4">
        <form onSubmit={handleSubmit} className="space-y-4 col-span-2">
          <div className="grid grid-cols-2 gap-4">
            <div className="flex flex-col">
              <label>Energy(Kcal)</label>
              <input
                type="text"
                name="NUTRITION.ENERGY"
                value={nutrition["NUTRITION.ENERGY"]}
                onChange={handleInputChange}
                step="any"
                className="border border-gray-400 p-1"
              />
            </div>
            <div className="flex flex-col">
              <label>Protein(g)</label>
              <input
                type="text"
                name="NUTRITION.PROTEIN"
                value={nutrition["NUTRITION.PROTEIN"]}
                onChange={handleInputChange}
                step="any"
                className="border border-gray-400 p-1"
              />
            </div>
            <div className="flex flex-col">
              <label>Carbohydrate(g)</label>
              <input
                type="text"
                name="NUTRITION.CARBOHYDRATE"
                value={nutrition["NUTRITION.CARBOHYDRATE"]}
                onChange={handleInputChange}
                step="any"
                className="border border-gray-400 p-1"
              />
            </div>
            <div className="flex flex-col">
              <label>Total Sugars(g)</label>
              <input
                type="text"
                name="NUTRITION.TOTAL_SUGARS"
                value={nutrition["NUTRITION.TOTAL_SUGARS"]}
                onChange={handleInputChange}
                step="any"
                className="border border-gray-400 p-1"
              />
            </div>
            <div className="flex flex-col">
              <label>Added Sugars(g)</label>
              <input
                type="text"
                name="NUTRITION.ADDED_SUGARS"
                value={nutrition["NUTRITION.ADDED_SUGARS"]}
                onChange={handleInputChange}
                step="any"
                className="border border-gray-400 p-1"
              />
            </div>
            <div className="flex flex-col">
              <label>Total Fat(g)</label>
              <input
                type="text"
                name="NUTRITION.TOTAL_FAT"
                value={nutrition["NUTRITION.TOTAL_FAT"]}
                onChange={handleInputChange}
                step="any"
                className="border border-gray-400 p-1"
              />
            </div>
            <div className="flex flex-col">
              <label>Saturated Fat(g)</label>
              <input
                type="text"
                name="NUTRITION.SATURATED_FAT"
                value={nutrition["NUTRITION.SATURATED_FAT"]}
                onChange={handleInputChange}
                step="any"
                className="border border-gray-400 p-1"
              />
            </div>
            <div className="flex flex-col">
              <label>Fiber(g)</label>
              <input
                type="text"
                name="NUTRITION.FIBER"
                value={nutrition["NUTRITION.FIBER"]}
                onChange={handleInputChange}
                step="any"
                className="border border-gray-400 p-1"
              />
            </div>
            <div className="flex flex-col">
              <label>Sodium(mg)</label>
              <input
                type="text"
                name="NUTRITION.SODIUM"
                value={nutrition["NUTRITION.SODIUM"]}
                onChange={handleInputChange}
                step="any"
                className="border border-gray-400 p-1"
              />
            </div>
          </div>
          <button
            type="submit"
            className="mt-4 bg-blue-500 text-white p-2 rounded"
          >
            Submit
          </button>
        </form>
      </div>
      {rating && ( // Display the rating below the form
        <div className="text-lg font-bold mt-4">Rating: {rating.toFixed(2)}/5.0</div>
      )}
    </div>
  );
}
