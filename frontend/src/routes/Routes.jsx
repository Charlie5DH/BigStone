import { Navigate, Route, Routes } from "react-router-dom";
import { Clients, Home, NotFound, Products, Records, Settings, User } from "../pages";

const PageRoutes = () => {
  return (
    <Routes>
      <Route exact path="/" element={<Navigate replace to="/home" />} />
      <Route path="/home" element={<Home />} />
      <Route path="/produtos" element={<Products />} />
      <Route path="/relatorios" element={<Records />} />
      <Route path="/clientes" element={<Clients />} />
      <Route path="/configuração" element={<Settings />} />
      <Route path="/perfil" element={<User />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
};

export default PageRoutes;
