import { Outlet } from "react-router-dom";
import Navbar from "./components/Navbar";
const Layout = () => {
  return (
    // <div className="min-h-screen text-white flex flex-col">
    // className="flex-grow max-w-5xl w-full mx-auto px-4"
      <div>
        <Navbar/>
      <main >
        <Outlet />
      </main>
      </div>
    // </div>
  );
};

export default Layout;