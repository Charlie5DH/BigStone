/* eslint-disable react/prop-types */

import { Dialog } from "primereact/dialog";
import { getClients } from "../../../actions/clients";
import { ProgressSpinner } from "primereact/progressspinner";
import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { Checkbox } from "../../../components";

const SelectClientDialog = ({ visible, setVisible, setClient, transactionForm, setTransactionForm }) => {
  const { clients, isLoadingClients } = useSelector((state) => state.clients);
  const [filterQuery, setFilterQuery] = React.useState("");
  const [filteredClients, setFilteredClients] = React.useState(clients);
  const [selectedClient, setSelectedClient] = React.useState([]);
  const dispatch = useDispatch();

  React.useEffect(() => {
    dispatch(getClients());
  }, []);

  React.useEffect(() => {
    setFilteredClients(clients);
  }, [clients]);

  const footerContent = () => {
    return (
      <div className="flex justify-end items-center gap-1">
        <button
          onClick={() => setVisible(false)}
          className="bg-white hover:bg-red-400 hover:text-white text-slate-500 text-14 font-normal 
        py-2 px-3 rounded-md border duration-200 shadow-sm shadow-red-200 active:scale-95"
        >
          Cancelar
        </button>
        <button
          onClick={() => {
            setClient(selectedClient);
            setTransactionForm({
              ...transactionForm,
              client_id: selectedClient._id,
              rf_id: selectedClient.rfid,
              rfid: selectedClient.rfid,
            });
            setVisible(false);
          }}
          className={`bg-indigo-500 hover:bg-indigo-400 text-white text-14 font-normal border border-slate-300 
                  py-2 px-3 rounded-md duration-200 shadow-md shadow-indigo-200 active:scale-95`}
        >
          Confirmar
        </button>
      </div>
    );
  };

  const handleFilterClientsByName = (e) => {
    setFilterQuery(e.target.value);
    const query = e.target.value;
    const filteredClients = clients.filter((client) => client.name.toLowerCase().includes(query.toLowerCase()));
    setFilteredClients(filteredClients);
  };

  return (
    <Dialog
      header="Selecione um cliente"
      visible={visible}
      style={{ width: "30vw" }}
      onHide={() => setVisible(false)}
      footer={footerContent}
    >
      {isLoadingClients ? (
        <div className="flex items-center justify-center mt-10">
          <ProgressSpinner
            style={{ width: "80px", height: "80px" }}
            strokeWidth="4"
            fill="var(--surface-ground)"
            animationDuration="1.2s"
          />
        </div>
      ) : (
        <div className="flex flex-col gap-y-2">
          <div className="flex items-center border font-secondary border-slate-200 rounded-md w-full px-3 py-2 shadow-sm">
            <input
              onChange={(e) => handleFilterClientsByName(e)}
              autoComplete="off"
              security="off"
              className="text-slate-500 w-full font-normal text-14
          focus:outline-none focus:ring-0 focus:ring-slate-300 focus:border-transparent"
              type={"text"}
              value={filterQuery}
              placeholder={"Procurar cliente"}
            />
          </div>

          <div className="flex flex-col gap-y-1 p-3 border rounded-md shadow-sm">
            {filteredClients.map((client, index) => (
              <div className="flex items-center gap-x-3 border-b py-1" key={index}>
                <Checkbox
                  label={""}
                  rounded="rounded-full"
                  checked={selectedClient._id === client._id}
                  onChange={() => setSelectedClient(client)}
                  color="bg-indigo-400"
                  checkBoxSize="h-5 w-5"
                  disabled={false}
                  font="font-normal"
                  icon={undefined}
                />
                <div className="flex flex-col">
                  <span className="text-slate-500 text-14 font-normal">{client.name}</span>
                  <span className="text-slate-500 text-12 font-normal">{client.email}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </Dialog>
  );
};

export default SelectClientDialog;
