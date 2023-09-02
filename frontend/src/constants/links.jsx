import { AiFillHome, AiFillSetting } from "react-icons/ai";
import { BiSolidShoppingBag } from "react-icons/bi";
import { MdAttachMoney } from "react-icons/md";
import { HiUsers } from "react-icons/hi";

export const links = [
  {
    label: "Home",
    path: "/home",
    icon: <AiFillHome />,
  },
  {
    label: "Produtos",
    path: "/produtos",
    icon: <BiSolidShoppingBag />,
  },
  {
    label: "Relatorios",
    path: "/relatorios",
    icon: <MdAttachMoney />,
  },
  {
    label: "Clientes",
    path: "/clientes",
    icon: <HiUsers />,
  },
  // {
  //   label: "Configurações",
  //   path: "/configuração",
  //   icon: <AiFillSetting />,
  // },
];
