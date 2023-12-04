/* eslint-disable no-unused-vars */
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
import NewSaleDialog from "./components/NewSaleDialog";
import AddProductToSaleDialog from "./components/AddProductToSaleDialog";
import ManualTransactionDialog from "./components/ManualTransactionDialog";
import CardsInBanner from "./components/CardsInBanner";
import { getClientUsingRFID } from "../../actions/clients";
import { getClientByRFID } from "../../apis";
import NotFoundClientDialog from "./components/NotFoundClientDialog";

const Home = () => {
  const options = ["24 horas", "48 horas", "Últimos 7 dias", "Últimos 30 dias"];

  const { transactions, isLoadingTransactions } = useSelector((state) => state.transactions);
  const { items, isLoadingItems } = useSelector((state) => state.items);
  const { kg_price, isLoadingKGPrice } = useSelector((state) => state.weight);
  const [option, setOption] = React.useState(options[1]);
  const [websocketData, setWebsocketData] = React.useState("");
  const [visible, setVisible] = React.useState(false);
  const [newPrice, setNewPrice] = React.useState(0);
  const [visibleNewManualTransaction, setVisibleNewManualTransaction] = React.useState(false);
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
    timestamp: new Date().toISOString(),
  });
  const [manualTransactionForm, setManualTransactionForm] = React.useState({
    client_id: "64d2f0cd47614dfdea47e246",
    rfid: "333907a32a974752869d7022183d6608",
    type: "sell",
    items: [],
    kg_price: kg_price,
    weight: 0,
    timestamp: new Date().toISOString(),
  });
  const dispatch = useDispatch();
  const [rfidValue, setRfidValue] = React.useState("");
  const [filterQuery, setFilterQuery] = React.useState(""); // filter query for items
  const [filteredItems, setFilteredItems] = React.useState([]);
  const [client, setClient] = React.useState({});
  const [loadingClient, setLoadingClient] = React.useState(false);
  const [clientError, setClientError] = React.useState(false);
  const [errorMessage, setErrorMessage] = React.useState("");

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
          ? // 24 hours from now (using moment)
            new Date(new Date().getTime() - 1 * 24 * 60 * 60 * 1000).toISOString()
          : option === "48 horas"
          ? new Date(new Date().getTime() - 2 * 24 * 60 * 60 * 1000).toISOString()
          : option === "Últimos 7 dias"
          ? new Date(new Date().getTime() - 7 * 24 * 60 * 60 * 1000).toISOString()
          : new Date(new Date().getTime() - 30 * 24 * 60 * 60 * 1000).toISOString(),
        new Date().toISOString()
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
          ? // at time 00:00:00
            new Date(new Date().getTime() - 1 * 24 * 60 * 60 * 1000).toISOString()
          : option === "48 horas"
          ? new Date(new Date().getTime() - 2 * 24 * 60 * 60 * 1000).toISOString()
          : option === "Últimos 7 dias"
          ? new Date(new Date().getTime() - 7 * 24 * 60 * 60 * 1000).toISOString()
          : new Date(new Date().getTime() - 30 * 24 * 60 * 60 * 1000).toISOString(),
        new Date().toISOString()
      )
    );
  }, [option]);

  React.useEffect(() => {
    setFilteredRecords(transactions);
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
        timestamp: data.timestamp,
      });

      if (data.message === "new_weight") {
        setNewTransactionDialogVisible(true);
      } else if (data.message === "cancel") {
        setNewTransactionDialogVisible(false);
        setTransactionForm({
          ...transactionForm,
          weight: 0,
          kg_price: kg_price,
          timestamp: data.timestamp,
        });
      } else {
        setNewTransactionDialogVisible(false);
        setTransactionForm({
          ...transactionForm,
          weight: 0,
          kg_price: kg_price,
          timestamp: data.timestamp,
        });
      }
    };

    // Clean up WebSocket connection on unmount
    return () => {
      socket.close();
    };
  }, []);

  React.useEffect(() => {
    // WebSocket connection
    const socket = new WebSocket("ws://localhost:8003/ws/rfid_to_client");

    socket.onmessage = (event) => {
      // Handle data received from WebSocket
      const data = JSON.parse(event.data);
      console.log(data);

      if (data.message === "rfid") {
        setRfidValue(data.value);
      } else {
        setRfidValue("");
      }
    };

    // Clean up WebSocket connection on unmount
    return () => {
      socket.close();
    };
  }, []);

  const fetchClient = async (rfid) => {
    setLoadingClient(true);

    try {
      const response = await getClientByRFID(rfid);
      setClient(response.data);
      setClientError(false);
      setErrorMessage("");

      if (websocketData.weight !== 0 && websocketData.weight && websocketData.weight) {
        setNewTransactionDialogVisible(true);
      }

      console.log(response);
    } catch (error) {
      setClient({});
      setClientError(true);
      setErrorMessage(error.response.data.message || "Erro ao buscar cliente");
      console.log(error);
    } finally {
      setLoadingClient(false);
      setRfidValue("");
    }
  };

  React.useEffect(() => {
    if (rfidValue !== "") {
      fetchClient(rfidValue);
    }
  }, [rfidValue]);

  const handleCreateNewTransaction = () => {
    setNewTransactionDialogVisible(false);

    console.log(transactionForm);

    dispatch(
      createTransaction({
        ...transactionForm,
        weight: websocketData.weight,
        kg_price: kg_price,
        client_id: client._id,
        rf_id: client.rfid,
        rfid: client.rfid,
      })
    );

    setTransactionForm({
      ...transactionForm,
      kg_price: kg_price,
      items: [],
      weight: 0,
      client_id: "",
      rf_id: "",
      rfid: "",
    });

    setClient({});
    setWebsocketData({});
  };

  React.useEffect(() => {
    setClient(client);
    setTransactionForm({
      ...transactionForm,
      client_id: client._id,
      rf_id: client.rfid,
      rfid: client.rfid,
    });
  }, [client]);

  const handleCreateNewManualTransaction = () => {
    setVisibleNewManualTransaction(false);

    dispatch(
      createTransaction({
        ...transactionForm,
        weight: 0,
        kg_price: kg_price,
        client_id: client._id,
        rf_id: client.rfid,
        rfid: client.rfid,
      })
    );
    setTransactionForm({
      ...transactionForm,
      kg_price: kg_price,
      items: [],
      weight: 0,
      client_id: "",
      rf_id: "",
      rfid: "",
    });
    setClient({});
    setWebsocketData({});
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
            setVisibleNewManualTransaction={setVisibleNewManualTransaction}
          />
          <div
            className="flex flex-col items-center mt-2 border 
          bg-white shadow-indigo-100 shadow-md rounded-md p-3 max-w-full
          overflow-x-auto mx-2 my-2 overflow-y-scroll max-h-[82vh]"
          >
            <CardsInBanner
              kg_price={kg_price}
              transactions={transactions}
              computeNumeroDeVendasHoje={computeNumeroDeVendasHoje}
              computeDifferenceBetweenCurrentAndPast={computeDifferenceBetweenCurrentAndPast}
            />
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

          <NewSaleDialog
            client={client}
            items={items}
            kg_price={kg_price}
            setClient={setClient}
            websocketData={websocketData}
            transactionForm={transactionForm}
            setWebsocketData={setWebsocketData}
            setTransactionForm={setTransactionForm}
            newTransactionDialogVisible={newTransactionDialogVisible}
            setNewTransactionDialogVisible={setNewTransactionDialogVisible}
            setViewInsertProductDialog={setViewInsertProductDialog}
            handleCreateNewTransaction={handleCreateNewTransaction}
          />

          <AddProductToSaleDialog
            filterQuery={filterQuery}
            filteredItems={filteredItems}
            transactionForm={transactionForm}
            handleFilterItems={handleFilterItems}
            setTransactionForm={setTransactionForm}
            viewInsertProductDialog={viewInsertProductDialog}
            setViewInsertProductDialog={setViewInsertProductDialog}
            handleAddItemToTransactionForm={handleAddItemToTransactionForm}
            handleRemoveItemFromTransactionForm={handleRemoveItemFromTransactionForm}
          />

          <ManualTransactionDialog
            items={items}
            client={client}
            setClient={setClient}
            kg_price={kg_price}
            websocketData={websocketData}
            transactionForm={transactionForm}
            setTransactionForm={setTransactionForm}
            handleCreateNewManualTransaction={handleCreateNewManualTransaction}
            setViewInsertProductDialog={setViewInsertProductDialog}
            visibleNewManualTransaction={visibleNewManualTransaction}
            setVisibleNewManualTransaction={setVisibleNewManualTransaction}
          />
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
