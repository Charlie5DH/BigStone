import { Link } from "react-router-dom";
import { links } from "../../../constants/links";
import { BsFillCartFill } from "react-icons/bs";
import { useLocation } from "react-router-dom";
import Tooltip from "@mui/material/Tooltip";
import { Badge } from "@mui/material";
// import logotext4 from "../../../assets/logotext4.svg";

const DesktopMenu = () => {
  // get current location path with react-router-dom
  const location = useLocation();
  const { pathname } = location;
  const splitLocation = pathname.split("/");
  const currentLocation = splitLocation[1];

  return (
    <div className="flex items-center justify-between mx-5 gap-1 w-full font-secondary">
      {/* <img src={logotext4} className="w-32 h-12" alt="logo" /> */}
      <span className="text-28 text-indigo-500 font-semibold font-display">Cantina</span>

      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2">
          {links.map((link, index) => (
            <Link
              key={index}
              to={link.path}
              className={`flex items-center text-gray-300 text-14 font-normal py-1 px-3 
            hover:bg-slate-600 hover:rounded-md hover:text-white transition-all hover:shadow-sm
            ease-in-out duration-200 cursor-pointer h-9 ${
              currentLocation === link.path.split("/")[1] ? "bg-slate-600 rounded-md shadow-sm" : ""
            }`}
            >
              <Tooltip title={link.label} arrow>
                <div className="flex items-center gap-2">
                  <span className="text-20 text-gray-300">{link.icon}</span>
                  <span className="capitalize">{link.label}</span>
                </div>
              </Tooltip>
            </Link>
          ))}
        </div>

        <div className="flex items-center gap-2 border-l border-slate-600 px-3">
          <Tooltip title={"Compras"} arrow>
            <div className="cursor-pointer text-gray-300 hover:text-slate-600 p-1 duration-150">
              <Badge badgeContent={4} color="secondary">
                <BsFillCartFill className="text-20" />
              </Badge>
            </div>
          </Tooltip>

          <Link to={`/profile`} className="text-gray-300 hover:text-white transition-all ease-in-out duration-150">
            <Tooltip title={"Usuario"} arrow>
              <img
                src="https://images.pexels.com/photos/2379004/pexels-photo-2379004.jpeg?auto=compress&cs=tinysrgb&w=1600"
                alt="profile"
                className="ml-4 w-8 h-8 rounded-full object-cover cursor-pointer"
              />
            </Tooltip>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default DesktopMenu;
