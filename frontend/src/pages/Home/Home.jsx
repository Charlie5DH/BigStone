import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { createTransaction, getTransactions } from "../../actions/transactions";
import { ProgressSpinner } from "primereact/progressspinner";
import { Dialog } from "primereact/dialog";
import { getItems } from "../../actions/items";
import RecordsList from "../../components/List/RecordsList";
import Toolbar from "./components/Toolbar";
import { Card } from "../../components";
import { getKGPrice, updateKGPrice } from "../../actions/weight";
import moment from "moment";

const Home = () => {
  const options = ["24 horas", "48 horas", "Últimos 7 dias", "Últimos 30 dias"];

  const { transactions, isLoadingTransactions } = useSelector((state) => state.transactions);
  const { items, isLoadingItems } = useSelector((state) => state.items);
  const { kg_price, isLoadingKGPrice } = useSelector((state) => state.weight);
  const [option, setOption] = React.useState(options[1]);
  const [websocketData, setWebsocketData] = React.useState("");
  const [visible, setVisible] = React.useState(false);
  const [newPrice, setNewPrice] = React.useState(0);
  const [newTransactionDialogVisible, setNewTransactionDialogVisible] = React.useState(false);
  const [viewInsertProductDialog, setViewInsertProductDialog] = React.useState(false);
  const [filteredRecords, setFilteredRecords] = React.useState([]); // filtered records for the table
  const [recordsFilterQuery, setRecordsFilterQuery] = React.useState(""); // filter query for records
  const [transactionForm, setTransactionForm] = React.useState({
    client_id: "64d2f0cd47614dfdea47e246",
    rfid: "333907a32a974752869d7022183d6608",
    type: "sell",
    items: [],
    kg_price: kg_price,
    weight: 0,
    timestamp: moment().format(
      "YYYY-MM-DDTHH:mm:ss.SSSZ" // 2021-09-01T00:00:00.000Z
    ),
  });
  const dispatch = useDispatch();
  const [filterQuery, setFilterQuery] = React.useState(""); // filter query for items
  const [filteredItems, setFilteredItems] = React.useState([]);

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
    setNewPrice(kg_price);
  }, [kg_price]);

  React.useEffect(() => {
    dispatch(
      getTransactions(
        "sell",
        option === "24 horas"
          ? // at time 00:00:00
            new Date(new Date().getTime() - 24 * 60 * 60 * 1000).toISOString().split("T")[0] + "T00:00:00.000Z"
          : option === "48 horas"
          ? new Date(new Date().getTime() - 48 * 60 * 60 * 1000).toISOString().split("T")[0] + "T00:00:00.000Z"
          : option === "Últimos 7 dias"
          ? new Date(new Date().getTime() - 7 * 24 * 60 * 60 * 1000).toISOString().split("T")[0] + "T00:00:00.000Z"
          : new Date(new Date().getTime() - 30 * 24 * 60 * 60 * 1000).toISOString().split("T")[0] + "T00:00:00.000Z",
        new Date().toISOString().split("T")[0] + "T00:00:00.000Z"
      )
    );
    dispatch(getItems(true));
    dispatch(getKGPrice());
  }, []);

  React.useEffect(() => {
    dispatch(
      getTransactions(
        "sell",
        option === "24 horas"
          ? new Date(new Date().getTime() - 24 * 60 * 60 * 1000).toISOString().split("T")[0] + "T00:00:00.000Z"
          : option === "48 horas"
          ? new Date(new Date().getTime() - 48 * 60 * 60 * 1000).toISOString().split("T")[0] + "T00:00:00.000Z"
          : option === "Últimos 7 dias"
          ? new Date(new Date().getTime() - 7 * 24 * 60 * 60 * 1000).toISOString().split("T")[0] + "T00:00:00.000Z"
          : new Date(new Date().getTime() - 30 * 24 * 60 * 60 * 1000).toISOString().split("T")[0] + "T00:00:00.000Z",
        new Date().toISOString().split("T")[0] + "T00:00:00.000Z"
      )
    );
  }, [option]);

  React.useEffect(() => {
    if (transactions.length > 0) {
      setFilteredRecords(transactions);
    }
  }, [transactions]);

  React.useEffect(() => {
    if (items.length > 0) {
      setFilteredItems(items);
    }
  }, [items]);

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

  React.useEffect(() => {
    // WebSocket connection
    const socket = new WebSocket("ws://localhost:8003/ws/weight");

    socket.onmessage = (event) => {
      // Handle data received from WebSocket
      const data = JSON.parse(event.data);
      setWebsocketData(data);

      setTransactionForm({
        ...transactionForm,
        weight: data.weight,
        kg_price: kg_price,
      });

      if (data.message === "new_weight") {
        setNewTransactionDialogVisible(true);
      } else if (data.message === "cancel_weight") {
        setNewTransactionDialogVisible(false);
        setTransactionForm({
          ...transactionForm,
          weight: 0,
          kg_price: kg_price,
        });
      } else {
        setNewTransactionDialogVisible(false);
        setTransactionForm({
          ...transactionForm,
          weight: 0,
          kg_price: kg_price,
        });
      }
    };

    // Clean up WebSocket connection on unmount
    return () => {
      socket.close();
    };
  }, []);

  const handleCreateNewTransaction = () => {
    setNewTransactionDialogVisible(false);
    dispatch(createTransaction({ ...transactionForm, weight: websocketData.weight, kg_price: kg_price }));
    setTransactionForm({
      ...transactionForm,
      kg_price: kg_price,
      items: [],
    });
  };

  const handleFilterItems = (e) => {
    setFilterQuery(e.target.value);
    if (e.target.value === "") {
      setFilteredItems(items);
      return;
    }
    setFilteredItems(items.filter((item) => item.name.toLowerCase().includes(e.target.value.toLowerCase())));
  };

  const handleAddItemToTransactionForm = (produto) => {
    // add one to quantity of the item in the transaction form
    // if item is not in the transaction form, add it
    // if the number of items added from the product is equal to the number of items available (find the item in the items array and compare the quantity), do not add it

    const itemIndex = transactionForm.items.findIndex((item) => item.item_id === produto._id);
    const newItems = [...transactionForm.items];
    if (itemIndex === -1) {
      newItems.push({
        item_id: produto._id,
        name: produto.name,
        quantity: 1,
      });
    }
    if (itemIndex !== -1 && newItems[itemIndex].quantity < produto.quantity) {
      newItems[itemIndex].quantity += 1;
    }
    setTransactionForm({
      ...transactionForm,
      items: newItems,
    });
  };

  const handleRemoveItemFromTransactionForm = (produto) => {
    // remove one to quantity of the item in the transaction form
    // if quantity is 0, remove the item from the transaction form
    const itemIndex = transactionForm.items.findIndex((item) => item.item_id === produto._id);
    const newItems = [...transactionForm.items];
    if (newItems[itemIndex].quantity === 1) {
      newItems.splice(itemIndex, 1);
    } else {
      newItems[itemIndex].quantity -= 1;
    }
    setTransactionForm({
      ...transactionForm,
      items: newItems,
    });
  };

  // TODO: Adicionar paginação
  // TODO: Enviar usuario desde raspberry

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
          <Toolbar
            setVisible={setVisible}
            transactions={transactions}
            setFilteredRecords={setFilteredRecords}
            filterQuery={recordsFilterQuery}
            setFilterQuery={setRecordsFilterQuery}
            option={option}
            setOption={setOption}
            options={options}
          />
          <div
            className="flex flex-col items-center mt-2 border 
          bg-white shadow-indigo-100 shadow-md rounded-md p-3 max-w-full
          overflow-x-auto mx-2 my-2 overflow-y-scroll max-h-[82vh]"
          >
            <div className="flex flex-wrap lg:flex-nowrap items-stretch w-full lg:w-[90%] gap-2">
              <Card
                title={`$R ${
                  Number(
                    transactions
                      .filter((row) => row.timestamp.split("T")[0] === new Date().toISOString().split("T")[0])
                      .reduce((acc, row) => acc + row.total, 0)
                  ).toFixed(2) || 0
                }`}
                subtitle={"Total do dia"}
                titleCompare={
                  // compare today and yesterday
                  computeDifferenceBetweenCurrentAndPast("total") > 0
                    ? `+${Number(computeDifferenceBetweenCurrentAndPast("total").toFixed(2))} comparado a ontem`
                    : `${Number(computeDifferenceBetweenCurrentAndPast("total").toFixed(2))} comparado a ontem`
                }
                sign={"+"}
              />

              <Card
                title={
                  computeDifferenceBetweenCurrentAndPast("meal_price") > 0
                    ? `+$R ${Number(computeDifferenceBetweenCurrentAndPast("meal_price")).toFixed(2)}`
                    : `+$R ${Number(computeDifferenceBetweenCurrentAndPast("meal_price")).toFixed(2)}`
                }
                subtitle={"Total do dia em refeições"}
                titleCompare={
                  computeDifferenceBetweenCurrentAndPast("meal_price") > 0
                    ? `+${Number(computeDifferenceBetweenCurrentAndPast("meal_price")).toFixed(2)} comparado a ontem`
                    : `${Number(computeDifferenceBetweenCurrentAndPast("meal_price")).toFixed(2)} comparado a ontem`
                }
                sign={`${computeDifferenceBetweenCurrentAndPast("meal_price") > 0 ? "+" : ""}`}
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
            <RecordsList records={filteredRecords} produtos={items} />
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
          <Dialog
            header="Nova venda"
            visible={newTransactionDialogVisible}
            style={{ width: "100%", maxWidth: "50vw" }}
            onHide={() => setNewTransactionDialogVisible(false)}
            footer={
              <div className="flex justify-between items-center gap-1">
                <button
                  onClick={() => setViewInsertProductDialog(true)}
                  className="bg-emerald-500 hover:bg-emerald-400 text-white text-14 font-normal 
                  py-2 px-3 rounded-md duration-200 shadow-md shadow-emerald-200 active:scale-95
                  animate-pulse"
                >
                  + Adicionar produtos
                </button>
                <div className="flex justify-end items-center gap-1">
                  <button
                    onClick={() => setNewTransactionDialogVisible(false)}
                    className="bg-white hover:bg-red-400 hover:text-white text-slate-500 text-14 font-normal 
        py-2 px-3 rounded-md border duration-200 shadow-sm shadow-indigo-200 active:scale-95"
                  >
                    Cancelar
                  </button>
                  <button
                    onClick={() => handleCreateNewTransaction()}
                    className="bg-indigo-500 hover:bg-indigo-400 text-white text-14 font-normal 
                  py-2 px-3 rounded-md duration-200 shadow-md shadow-indigo-200 active:scale-95"
                  >
                    Confirmar
                  </button>
                </div>
              </div>
            }
          >
            <div className="flex flex-col items-center border rounded-md w-full my-3">
              <div className="grid grid-cols-4 w-full items-center justify-between p-2 bg-slate-100">
                <div className="flex items-center justify-center gap-1 text-slate-500 mb-4">
                  <span className="text-[13px] font-normal">Cliente</span>
                </div>
                <div className="flex items-center justify-center gap-1 text-slate-500 border-l mb-4">
                  <span className="text-[13px] font-normal">Peso registrado</span>
                </div>
                <div className="flex items-center justify-center gap-1 text-slate-500 border-l mb-4">
                  <span className="text-[13px] font-normal">Valor atual do Kg</span>
                </div>
                <div className="flex items-center justify-center gap-1 text-slate-500 border-l mb-4">
                  <span className="text-[13px] font-normal">Valor a pagar por prato</span>
                </div>

                <div className="flex items-center justify-center gap-1 text-slate-500">
                  <span className="text-16 font-semibold">client name</span>
                </div>

                <div className="flex items-center justify-center gap-1 text-slate-500">
                  <span className="text-16 font-semibold">{websocketData.weight} Kg</span>
                </div>

                <div className="flex items-center justify-center gap-1 text-slate-500">
                  <span className="text-16 font-semibold">R$ {kg_price}</span>
                </div>

                <div className="flex items-center justify-center gap-1 text-slate-500">
                  <span className="text-16 font-semibold">R$ {Number(websocketData.weight * kg_price).toFixed(2)}</span>
                </div>
              </div>
            </div>

            {transactionForm.items.length > 0 ? (
              <div className="flex flex-col gap-y-1 px-3 py-2 duration-200">
                <span className="text-14 font-medium text-slate-700">Produtos adicionados</span>
                <div className="flex flex-col items-center border rounded-md w-full my-1">
                  <div className="grid grid-cols-6 w-full items-center justify-between p-3 bg-slate-100">
                    <div className="flex items-start col-span-2 lg:col-span-3 xl:col-span-3">
                      <span className="flex items-center gap-2 text-[13px] font-normal text-slate-500">Nome</span>
                    </div>

                    <div
                      className="lg:flex hidden items-center justify-center gap-1 text-slate-500
           hover:text-slate-400 duration-200 cursor-pointer border-l"
                    >
                      <span className="text-[13px] font-normal">Preço</span>
                    </div>

                    <div className="flex items-center justify-center gap-1 text-slate-500 hover:text-slate-400 duration-200 cursor-pointer border-l">
                      <span className="text-[13px] font-normal">Quantidade adicionada</span>
                    </div>

                    <div className="flex items-center justify-center gap-1 text-slate-500 hover:text-slate-400 duration-200 cursor-pointer border-l">
                      <span className="text-[13px] font-normal">Valor total</span>
                    </div>
                  </div>

                  {transactionForm.items.length > 0 &&
                    transactionForm.items.map((item, index) => (
                      <div
                        key={index}
                        className="grid grid-cols-6 w-full items-center justify-between p-3 bg-slate-100 border-t"
                      >
                        <div className="flex items-start col-span-2 lg:col-span-3 xl:col-span-3">
                          <div className="flex items-center">
                            <img
                              src={`http://localhost:8003/api/get_image/${
                                items.find((produto) => produto._id === item.item_id).image
                              }`} //"https://placehold.co/600x400" ||
                              alt="item"
                              className="rounded-md shadow-sm w-16 h-16 object-cover"
                            />
                            <div className="flex flex-col gap-y-1 ml-4">
                              <span className="text-14 font-medium text-slate-700">{item.name}</span>
                              <span className="text-12 font-normal text-slate-500">
                                {items.find((produto) => produto._id === item.item_id).description}
                              </span>
                            </div>
                          </div>
                        </div>
                        <div className="flex items-center justify-center gap-1 text-slate-500 hover:text-slate-400 duration-200 border-l">
                          <span className="text-12 font-medium text-slate-500">
                            $R {items.find((produto) => produto._id === item.item_id).price}
                          </span>
                        </div>

                        <div className="flex items-center justify-center gap-1 text-slate-500 hover:text-slate-400 duration-200 border-l">
                          <span className="text-12 font-medium text-slate-500">{item.quantity}</span>
                        </div>

                        <div className="flex items-center justify-center gap-1 text-slate-500 hover:text-slate-400 duration-200 border-l">
                          <span className="text-12 font-medium text-slate-500">
                            $R{" "}
                            {Number(
                              item.quantity * items.find((produto) => produto._id === item.item_id).price
                            ).toFixed(2)}
                          </span>
                        </div>
                      </div>
                    ))}
                </div>
              </div>
            ) : (
              <div className="flex items-center gap-1 text-slate-500 mt-4">
                <span className="text-16 font-normal">Nenhum produto adicionado</span>
              </div>
            )}
            <div className="flex flex-col gap-y-2 mt-4">
              <span className="text-14 font-medium text-slate-700">
                Total em produtos: $R{" "}
                {transactionForm.items.reduce(
                  (acc, item) => acc + item.quantity * items.find((produto) => produto._id === item.item_id).price,
                  0
                ) || 0}
              </span>
              <span className="text-16 font-medium text-slate-700 mt-2">
                Total: $R{" "}
                {(
                  Number(websocketData.weight * kg_price) +
                  Number(
                    transactionForm.items.reduce(
                      (acc, item) => acc + item.quantity * items.find((produto) => produto._id === item.item_id).price,
                      0
                    )
                  )
                ).toFixed(2) || 0}
              </span>
            </div>
          </Dialog>

          <Dialog
            header="Adicionar produtos ao pedido"
            visible={viewInsertProductDialog}
            style={{ width: "50vw" }}
            onHide={() => setViewInsertProductDialog(false)}
          >
            <div className="flex items-center justify-between w-full mb-2 gap-1">
              <input
                className="relative w-1/2 h-10 cursor-text text-left font-light sm:text-14 dark:bg-secondary-dark-bg dark:text-white
              focus:outline-none bg-inherit focus-visible:border-1 focus-visible:ring-1 focus-visible:ring-white 
              focus-visible:ring-opacity-75 focus-visible:ring-offset-0 px-2 border rounded-md"
                name="filter_object"
                type="text"
                value={filterQuery}
                onChange={(e) => handleFilterItems(e)}
                placeholder={`filtrar produtos por nome`}
                autoComplete="off"
              ></input>

              <button
                onClick={() => {
                  // clean transaction form items
                  setTransactionForm({
                    ...transactionForm,
                    items: [],
                  });
                }}
                className="bg-white hover:bg-indigo-400 hover:text-white text-slate-500 text-14 font-normal
              py-2 px-3 rounded-md border duration-200 shadow-sm shadow-indigo-200 active:scale-95"
              >
                Limpar produtos adicionados
              </button>
            </div>

            {transactionForm.items.length > 0 ? (
              <div className="flex flex-wrap items-center w-full mb-2 gap-1 border rounded-md p-3">
                {transactionForm.items.map((item) => (
                  <div key={item.name} className="flex items-center px-3 py-1 border rounded-md bg-slate-50">
                    <span className="flex items-center gap-2 text-[13px] font-normal text-slate-500">{item.name}:</span>
                    <span className="flex items-center gap-2 text-[13px] font-semibold text-slate-600 ml-4">
                      {item.quantity}
                    </span>
                  </div>
                ))}
              </div>
            ) : (
              <div className="flex flex-wrap items-center w-full mb-2 gap-1 border rounded-md p-3">
                <span className="flex items-center gap-2 px-3 py-1 text-[13px] font-normal text-slate-500">
                  Nenhum produto adicionado
                </span>
              </div>
            )}

            <div className="flex flex-col w-full gap-y-1 max-h-[620px] overflow-y-scroll">
              <div className="flex flex-col items-center border rounded-md w-full my-1">
                <div className="grid grid-cols-6 w-full items-center justify-between p-3 bg-slate-100">
                  <div className="flex items-start col-span-2 lg:col-span-3 xl:col-span-3">
                    <span className="flex items-center gap-2 text-[13px] font-normal text-slate-500">Nome</span>
                  </div>

                  <div
                    className="lg:flex hidden items-center justify-center gap-1 text-slate-500
           hover:text-slate-400 duration-200 cursor-pointer border-l"
                  >
                    <span className="text-[13px] font-normal">Preço</span>
                  </div>

                  <div className="flex items-center justify-center gap-1 text-slate-500 hover:text-slate-400 duration-200 cursor-pointer border-l">
                    <span className="text-[13px] font-normal">Disponível</span>
                  </div>

                  <div className="flex items-center justify-center gap-1 text-slate-500 hover:text-slate-400 duration-200 cursor-pointer border-l">
                    <span className="text-[13px] font-normal">Ações</span>
                  </div>
                </div>
                {filteredItems.map((produto, index) => (
                  <div key={index} className="grid grid-cols-6 w-full items-center justify-between p-2 border-t">
                    <div className="flex items-start col-span-3 p-1">
                      <div className="flex flex-nowrap items-center">
                        <img
                          src={`http://localhost:8003/api/get_image/${produto.image}`} //"https://placehold.co/600x400" ||
                          alt="produto"
                          className="rounded-md shadow-sm w-12 h-12 object-cover"
                        />
                        <div className="flex flex-col gap-y-1 ml-4">
                          <span className="text-14 font-medium text-slate-700">{produto.name}</span>
                          <span className="text-12 font-normal text-slate-500">{produto.description}</span>
                        </div>
                      </div>
                    </div>
                    <div className="lg:flex hidden items-center justify-center gap-1 text-slate-500 hover:text-slate-400 duration-200 border-l">
                      <span className="text-14 font-normal text-slate-500">$R {produto.price}</span>
                    </div>
                    <div className="lg:flex hidden items-center justify-center gap-1 text-slate-500 hover:text-slate-400 duration-200 border-l">
                      <span className="text-14 font-normal text-slate-500">{produto.quantity}</span>
                    </div>
                    <div className="lg:flex hidden items-center justify-center gap-1 text-slate-500hover:text-slate-400 duration-200 border-l">
                      <button
                        onClick={() => handleAddItemToTransactionForm(produto)}
                        className="text-slate-100 font-display font-semibold text-14 w-7 h-7 rounded-md hover:scale-105 duration-150 border bg-emerald-500 active:scale-95"
                      >
                        +
                      </button>
                      <button
                        onClick={() => handleRemoveItemFromTransactionForm(produto)}
                        className="text-slate-100 font-display font-semibold text-14 w-7 h-7 rounded-md hover:scale-105 duration-150 border bg-slate-500 active:scale-95"
                      >
                        -
                      </button>
                    </div>
                  </div>
                ))}
              </div>
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
