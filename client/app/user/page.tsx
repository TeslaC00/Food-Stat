import Link from "next/link";
import { Image } from "@nextui-org/image";
import {DatePicker} from "@nextui-org/date-picker";

export default function About() {
  return (
    <div className="bg-white">


      {/* Profile container */}
      <div className="max-w-7xl mx-auto p-6 mt-3 mb-3 flex flex-col md:flex-row bg-gray-100 rounded-lg shadow-md">
        {/* Left Side - Profile Info */}
        <div className="md:w-1/3  h-fit flex flex-col items-center">
          {/* Profile Image */}
          <Image
            src="https://cdn.pixabay.com/photo/2021/07/02/04/48/user-6380868_640.png" // Replace with your image path
            alt="Profile Picture"
            width={120}
            height={120}
            className="rounded-full border-4 border-white shadow-lg"
          />

          {/* Personal Info Details */}
          <div className="bg-white p-4 rounded-md shadow-md mt-4">
            <h3 className="text-lg font-medium text-gray-700 mb-2">Personal Info</h3>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">First Name</label>
                <input
                  type="text"
                  className="mt-1 block w-full rounded-md border-gray-300 text-teal-300 shadow-sm"
                  defaultValue="Arthur"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Last Name</label>
                <input
                  type="text"
                  className="mt-1 block w-full rounded-md border-gray-300 text-teal-300 shadow-sm"
                  defaultValue="Nancy"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4 mt-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Email</label>
                <input
                  type="email"
                  className="mt-1 block w-full rounded-md border-gray-300 text-teal-300 shadow-sm"
                  defaultValue="bradley.ortiz@gmail.com"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Phone</label>
                <input
                  type="tel"
                  className="mt-1 block w-full rounded-md border-gray-300 text-teal-300 shadow-sm"
                  defaultValue="477-046-1827"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4 mt-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Gender</label>
                <select className="mt-1 block w-full rounded-md border-gray-300 text-black shadow-sm">
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="other">Other</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-black">Birth</label>
                <DatePicker className="max-w-[284px] text-black" />
              </div>
            </div>
          </div>
        </div>

        {/* Right Side - Other Details */}
        <div className="md:w-2/3 p-4">
          <div className="bg-white p-4 rounded-md shadow-md">
            <h3 className="text-lg font-medium text-gray-700 mb-2">Other Details</h3>

            <div className="grid grid-cols-2 gap-4 mt-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Address</label>
                <input
                  type="text"
                  className="mt-1 block w-full rounded-md border-gray-300 text-teal-300 shadow-sm"
                  defaultValue="116 Jaskolski Stravenue Suite 883"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Nation</label>
                <input
                  type="text"
                  className="mt-1 block w-full rounded-md border-gray-300 text-teal-300 shadow-sm"
                  defaultValue="Colombia"
                />
              </div>
            </div>

            <div className="grid grid-cols -2 gap-4 mt-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Language</label>
                <select className="mt-1 block w-full rounded-md border-gray-300 shadow-sm">
                  <option value="English">English</option>
                  {/* Add more languages */}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">Slogan</label>
                <input
                  type="text"
                  className="mt-1 block w-full rounded-md border-gray-300 text-teal-300 shadow-sm"
                  defaultValue="Land acquisition Specialist"
                />
              </div>
            </div>

            {/* Social Media Links */}
            <div className="grid grid-cols-2 gap-4 mt-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Twitter</label>
                <input
                  type="text"
                  className="mt-1 block w-full rounded-md border-gray-300 text-teal-300 shadow-sm"
                  defaultValue="twitter.com/envato"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">LinkedIn</label>
                <input
                  type="text"
                  className="mt-1 block w-full rounded-md border-gray-300 text-teal-300 shadow-sm"
                  defaultValue="linkedin.com/envato"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4 mt-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Facebook</label>
                <input
                  type="text"
                  className="mt-1 block w-full rounded-md border-gray-300 text-teal-300 shadow-sm"
                  defaultValue="facebook.com/envato"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Google</label>
                <input
                  type="text"
                  className="mt-1 block w-full rounded-md border-gray-300 text-teal-300 shadow-sm"
                  defaultValue="zachary Ruiz"
                />
              </div>
            </div>

            {/* Payment Methods */}
            <div className="mt-6">
              <h3 className="text-lg font-medium text-gray-700 mb-2">Payment Method</h3>
              <div className="flex space-x-4">
                <div className="bg-white p-4 rounded-md shadow-md">
                  <p className="text-sm text-gray-700">Visa .... 8314</p>
                  <p className="text-xs text-gray-500">Expires 06/21</p>
                </div>
                <div className="bg-white p-4 rounded-md shadow-md">
                  <p className="text-sm text-gray-700">Master .... 8314</p>
                  <p className="text-xs text-gray-500">Expires 07/19</p>
                </div>
              </div>
              <button className="text-green-600 text-sm mt-4">Add Payment Method</button>
            </div>
          </div>
        </div>
      </div>

    </div>
  )
}