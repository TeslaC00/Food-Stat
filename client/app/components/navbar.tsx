import Link from "next/link";
import { Image } from "@nextui-org/image";

export default function Navbar() {
  return (
    <div className="bg-yellow-400 text-black p-2">
      <nav className="flex justify-end p-4bar text-lg">
        <ul className="flex space-x-12 ">
          <li>
            <Link legacyBehavior href="/">
              <a className="text-black hover:text-white">Home</a>
            </Link>
          </li>
          <li>
            <Link legacyBehavior href="/about">
              <a className="text-black hover:text-white">About us</a>
            </Link>
          </li>
          <li>
            <Link legacyBehavior href="/scan">
              <a className="text-black hover:text-white">Scan item</a>
            </Link>
          </li>
          <li>
            <Link legacyBehavior href="/contact">
              <a className="text-black hover:text-white">Contact us</a>
            </Link>
          </li>
          <li>
            <Link legacyBehavior href="/user">
              <a>
                <Image
                  src="https://cdn.pixabay.com/photo/2021/07/02/04/48/user-6380868_640.png"
                  alt="User"
                  width={30}
                  height={30}
                  className="rounded-full object-fit-cover mr-3"
                />
              </a>
            </Link>
          </li>
        </ul>
      </nav>
    </div>
  );
}
