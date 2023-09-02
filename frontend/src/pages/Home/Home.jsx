import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { getTransactions } from "../../actions/transactions";
import { ProgressSpinner } from "primereact/progressspinner";
import { Dialog } from "primereact/dialog";
import { getItems } from "../../actions/items";
import RecordsList from "../../components/List/RecordsList";
import Toolbar from "./components/Toolbar";
import { Card } from "../../components";
import { getKGPrice, updateKGPrice } from "../../actions/weight";

const Home = () => {
  const { transactions, isLoadingTransactions } = useSelector((state) => state.transactions);
  const { items, isLoadingItems } = useSelector((state) => state.items);
  const { kg_price, isLoadingKGPrice } = useSelector((state) => state.weight);
  const [visible, setVisible] = React.useState(false);
  const [newPrice, setNewPrice] = React.useState(0);
  const dispatch = useDispatch();

  const footerContent = (
    <div>
      <button
        onClick={() => setVisible(false)}
        className="bg-white hover:bg-red-400 hover:text-white text-slate-500 text-14 font-normal 
        py-1 px-3 rounded-md border duration-200 shadow-sm shadow-indigo-200 active:scale-95"
      >
        Cancelar
      </button>
      <button
        onClick={() => handleUpdateKGPrice()}
        className="bg-indigo-500 hover:bg-indigo-400 text-white text-14 font-normal 
                  py-1 px-3 rounded-md duration-200 shadow-md shadow-indigo-200 active:scale-95"
      >
        Confirmar
      </button>
    </div>
  );

  React.useEffect(() => {
    dispatch(getTransactions());
    dispatch(getItems(true));
    dispatch(getKGPrice());
  }, []);

  const handleUpdateKGPrice = () => {
    dispatch(updateKGPrice(newPrice));
    setVisible(false);
  };

  const computeDifferenceBetweenCurrentAndPast = (key) => {
    // difference between today and yesterday for a given key

    const today = transactions.filter((row) => row.timestamp.split("T")[0] === new Date().toISOString().split("T")[0]);
    const yesterday = transactions.filter(
      (row) => row.timestamp.split("T")[0] === new Date(new Date().getTime() - 24 * 60 * 60 * 1000)
    );

    return today.reduce((acc, row) => acc + row[key], 0) - yesterday.reduce((acc, row) => acc + row[key], 0);
  };

  const computeNumeroDeVendasHoje = () => {
    // difference between today and yesterday for a given key

    const today = transactions.filter((row) => row.timestamp.split("T")[0] === new Date().toISOString().split("T")[0]);
    const yesterday = transactions.filter(
      (row) => row.timestamp.split("T")[0] === new Date(new Date().getTime() - 24 * 60 * 60 * 1000)
    );

    return today.length - yesterday.length;
  };

  return (
    <div>
      {isLoadingTransactions || isLoadingItems || isLoadingKGPrice ? (
        <div className="flex items-center justify-center mt-10 mx-4 my-2">
          <ProgressSpinner
            style={{ width: "80px", height: "80px" }}
            strokeWidth="4"
            fill="var(--surface-ground)"
            animationDuration="1.2s"
          />
        </div>
      ) : (
        <div className="flex flex-col gap-y-2 w-full">
          <Toolbar setVisible={setVisible} transactions={transactions} />
          <div
            className="flex flex-wrap items-center mt-2 border 
          bg-white shadow-indigo-100 shadow-md rounded-md p-3 max-w-full
          overflow-x-auto mx-2 my-2 justify-center"
          >
            <div className="flex flex-wrap lg:flex-nowrap items-stretch w-full lg:w-[90%] gap-2">
              <Card
                title={
                  transactions
                    .filter((row) => row.timestamp.split("T")[0] === new Date().toISOString().split("T")[0])
                    .reduce((acc, row) => acc + row.total, 0) || 0
                }
                subtitle={"Total do dia"}
                titleCompare={
                  // compare today and yesterday
                  computeDifferenceBetweenCurrentAndPast("total") > 0
                    ? `+${computeDifferenceBetweenCurrentAndPast("total")} comparado a ontem`
                    : `${computeDifferenceBetweenCurrentAndPast("total")} comparado a ontem`
                }
                sign={"+"}
              />
              <Card
                title={"110"}
                subtitle={"Media da semana"}
                titleCompare={"-10 comparado semana passada"}
                sign={"-"}
              />
              <Card
                title={
                  transactions.filter((row) => row.timestamp.split("T")[0] === new Date().toISOString().split("T")[0])
                    .length || 0
                }
                subtitle={"# de vendas hoje"}
                titleCompare={
                  computeNumeroDeVendasHoje() > 0
                    ? `+${computeNumeroDeVendasHoje()} comparado a ontem`
                    : `${computeNumeroDeVendasHoje()} comparado a ontem`
                }
                sign={"+"}
              />
              <Card title={`$R ${kg_price}`} subtitle={"Preço atual do KG"} />
            </div>
            <RecordsList records={transactions} produtos={items} />
          </div>

          <Dialog
            header="Atualizar preço do Kg"
            visible={visible}
            style={{ width: "50vw" }}
            onHide={() => setVisible(false)}
            footer={footerContent}
          >
            <div className="mx-2 flex overflow-hidden">
              <input
                className="relative w-full h-12 cursor-text text-left font-light sm:text-14 dark:bg-secondary-dark-bg dark:text-white
              focus:outline-none bg-inherit focus-visible:border-1 focus-visible:ring-1 focus-visible:ring-white 
              focus-visible:ring-opacity-75 focus-visible:ring-offset-0 px-2 mx-1 border rounded-md"
                name="filter_query"
                type="number"
                value={newPrice}
                onChange={(e) => setNewPrice(e.target.value)}
                placeholder={`Preço atual: R$ 30,00`}
                autoComplete="off"
              ></input>
            </div>
          </Dialog>
        </div>
      )}
    </div>
  );
};

export default Home;

/*
<div className="flex md:grid grid-cols-4 items-stretch gap-2">
            <Card
              title={
                transactions
                  .filter((row) => row.timestamp.split("T")[0] === new Date().toISOString().split("T")[0])
                  .reduce((acc, row) => acc + row.meal_price, 0) || 0
              }
              subtitle={"Total do dia"}
              titleCompare={"+30 comparado a ontem"}
              sign={"+"}
            />
            <Card title={"110"} subtitle={"Media da semana"} titleCompare={"-10 comparado semana passada"} sign={"-"} />
            <Card
              title={
                transactions.filter((row) => row.timestamp.split("T")[0] === new Date().toISOString().split("T")[0])
                  .length || 0
              }
              subtitle={"# de vendas hoje"}
              titleCompare={`${
                // difference between today and yesterday
                transactions.filter((row) => row.timestamp.split("T")[0] === new Date().toISOString().split("T")[0])
                  .length -
                transactions.filter(
                  (row) => row.timestamp.split("T")[0] === new Date(new Date().getTime() - 24 * 60 * 60 * 1000)
                ).length
              } comparado a ontem`}
              sign={"+"}
            />
            <Card
              title={"R$ 30"}
              subtitle={"Preço atual do KG"}
              footer={
                <div className="flex items-center justify-end">
                  <button
                    onClick={() => setVisible(true)}
                    className="bg-indigo-500 hover:bg-indigo-400 text-white text-12 font-normal 
                  py-1 px-3 rounded-md duration-200 shadow-sm shadow-indigo-200 active:scale-95"
                  >
                    Atualizar preço do Kg
                  </button>
                </div>
              }
            />
          </div>
 */
