/* eslint-disable no-unused-vars */
import React from "react";
import { getClients } from "../../actions/clients";
import { useDispatch, useSelector } from "react-redux";
import Toolbar from "./components/Toolbar";
import { getItems } from "../../actions/items";
import { ProgressSpinner } from "primereact/progressspinner";
import { Card } from "../../components";
import ClientsList from "../../components/List/ClientsList";

const Clients = () => {
  const { clients, isLoadingClients } = useSelector((state) => state.clients);
  const { items, isLoadingItems } = useSelector((state) => state.items);
  const dispatch = useDispatch();

  React.useEffect(() => {
    dispatch(getClients());
    dispatch(getItems(true));
  }, []);

  // TODO: Pay an amount of debt to client

  return (
    <div className="flex flex-col">
      <Toolbar />

      {isLoadingClients || isLoadingItems ? (
        <div className="flex items-center justify-center mt-10">
          <ProgressSpinner
            style={{ width: "80px", height: "80px" }}
            strokeWidth="4"
            fill="var(--surface-ground)"
            animationDuration="1.2s"
          />
        </div>
      ) : (
        <div
          className="flex flex-col items-center mt-2 border gap-y-1
          bg-white shadow-indigo-100 shadow-md rounded-md p-3 max-w-full
          overflow-x-auto mx-1 mb-3 max-h-[82vh] justify-center overflow-y-scroll"
        >
          <div className="flex flex-wrap lg:flex-nowrap items-stretch w-full lg:w-[90%] gap-2">
            <Card
              title={clients.filter((row) => Number(row.balance) < 0).length}
              subtitle={"Clientes com dividas"}
              titleCompare={undefined}
              sign={"+"}
            />
            <Card
              title={`$R ${Number(
                clients.filter((row) => Number(row.balance) < 0).reduce((acc, row) => acc + Number(row.balance), 0)
              ).toFixed(2)}`}
              subtitle={"Total em pagamentos pendentes"}
              titleCompare={undefined}
              sign={"+"}
            />
            <Card
              title={`$R ${Number(
                clients.filter((row) => Number(row.balance) > 0).reduce((acc, row) => acc + Number(row.balance), 0)
              ).toFixed(2)}`}
              subtitle={"Total sem dividas"}
              titleCompare={undefined}
              sign={"+"}
            />
            <Card
              title={`$R ${Number(clients.reduce((acc, row) => acc + Math.abs(Number(row.balance)), 0)).toFixed(2)}`}
              subtitle={"Total somando pagamentos pendentes"}
              titleCompare={undefined}
              sign={"+"}
            />
          </div>
          <ClientsList clients={clients} items={items} />
        </div>
      )}
    </div>
  );
};

export default Clients;
