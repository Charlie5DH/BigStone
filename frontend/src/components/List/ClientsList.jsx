/* eslint-disable no-unused-vars */
/* eslint-disable react/prop-types */
import React from "react";
import { MdAccountBalanceWallet, MdOutlineKeyboardDoubleArrowDown } from "react-icons/md";
import Checkbox from "../Inputs/Checkbox";
import { TiArrowSortedDown, TiArrowSortedUp, TiArrowUnsorted } from "react-icons/ti";
import { AiFillDelete, AiFillEdit } from "react-icons/ai";
import { clearDebtOfClients, deleteClients, updateClient } from "../../actions/clients";
import { useDispatch, useSelector } from "react-redux";
import { Dialog } from "primereact/dialog";
import { Sidebar } from "primereact/sidebar";
import { SelectButton } from "primereact/selectbutton";
import { getTransactionsSummaryByClient } from "../../actions/transactions";
import { getItems } from "../../actions/items";
import { ProgressSpinner } from "primereact/progressspinner";
import TotalSummary from "../../pages/Records/components/TotalSummary";
import DailySummary from "../../pages/Records/components/DailySummary";
import { Accordion, AccordionTab } from "primereact/accordion";

const ClientsList = ({ clients, items }) => {
  const [sort, setSort] = React.useState(0);
  const [sortedClients, setSortedClients] = React.useState(clients);
  const [selected, setSelected] = React.useState([]);
  const [confirmDelete, setConfirmDelete] = React.useState(false);
  const [confirmClearDebt, setConfirmClearDebt] = React.useState(false);
  const [activeDropdown, setActiveDropdown] = React.useState({});
  const [visibleUserTransactionsDialog, setVisibleUserTransactionsDialog] = React.useState(false);
  const [selectedClientToViewTransactions, setSelectedClientToViewTransactions] = React.useState({});
  const [editClientDialog, setEditClientDialog] = React.useState(false);
  const dispatch = useDispatch();

  const options = ["Hoje", "Ontem", "Últimos 7 dias", "Últimos 30 dias", "3 Mêses", "Selecione um período"];
  const viewOptions = ["Total", "Diario"];

  const { isLoadingSummaryOfTransactions, transactionsSummaryByClient } = useSelector((state) => state.transactions);
  const [viewOption, setViewOption] = React.useState(viewOptions[0]);
  const [option, setOption] = React.useState(options[2]);
  const [formData, setFormData] = React.useState({});

  React.useEffect(() => {
    setSortedClients(clients);
  }, [clients]);

  React.useEffect(() => {
    dispatch(getTransactionsSummaryByClient(selectedClientToViewTransactions._id, option));
  }, [option, selectedClientToViewTransactions]);

  const handleDropDown = (e, submenuIndex) => {
    e.preventDefault();
    setActiveDropdown((prevState) => ({
      ...prevState,
      [submenuIndex]: !prevState[submenuIndex], // Toggle active state for the clicked submenu
    }));
  };

  const handleDropDownAll = (e) => {
    e.preventDefault();
    setActiveDropdown((prevState) => {
      const newState = {};
      for (let i = 0; i < clients.length; i++) {
        newState[i] = !prevState[i];
      }
      return newState;
    });
  };

  const handleDeleteClients = () => {
    // delete selected clients
    dispatch(deleteClients(JSON.stringify(selected)));
    setConfirmDelete(false);
    setSelected([]);
  };

  const handleClearDebt = () => {
    // clear debt of selected clients
    dispatch(clearDebtOfClients(JSON.stringify(selected)));
    setConfirmClearDebt(false);
    setSelected([]);
  };

  const handleUpdateClient = () => {
    // update client
    setEditClientDialog(false);
    dispatch(
      updateClient(formData._id, {
        name: formData.name,
        email: formData.email,
        cpf: formData.cpf,
        phone: formData.phone,
        address: formData.address,
        group: formData.group,
        cep: formData.cep,
        rfid: formData.rfid,
        balance: formData.balance,
        timestamp: new Date().toISOString(),
      })
    );
  };

  return (
    <div className="flex flex-nowrap items-center justify-center gap-2 w-full lg:w-[90%] font-display">
      <div className="flex flex-col items-center border rounded-md w-full my-3">
        <div
          className="grid grid-cols-3 sm:grid-cols-5 lg:grid-cols-8 xl:grid-cols-10 w-full items-center
           justify-between p-3 bg-slate-100"
        >
          <div className="flex items-start col-span-2 lg:col-span-2 xl:col-span-3">
            <div className="flex items-center">
              <div
                onClick={(e) => handleDropDownAll(e)}
                className="flex p-1 mr-2 rounded-full hover:bg-slate-200 duration-200 cursor-pointer"
              >
                <MdOutlineKeyboardDoubleArrowDown className={`text-slate-500 text-[18px] duration-200`} />
              </div>
              <div className="flex flex-wrap items-start gap-2">
                <Checkbox
                  label={`Selecionados: ${selected.length}`}
                  checked={selected.length === clients.length && selected.length !== 0 ? true : false}
                  onChange={() =>
                    setSelected(
                      selected.length === clients.length && selected.length !== 0 ? [] : clients.map((e) => e._id)
                    )
                  }
                  color="bg-indigo-400"
                  checkBoxSize="h-[18px] w-[18px]"
                  rounded="rounded-[4px]"
                  disabled={false}
                  size="small"
                  font="font-normal"
                  icon={undefined}
                />

                {selected.length !== 0 ? (
                  <div className="lg:flex grid grid-cols-1 items-center gap-3">
                    <span className="text-[13px] font-normal text-slate-500"></span>
                    <button
                      onClick={() => setConfirmDelete(true)}
                      className="flex items-center gap-1 text-white font-secondary font-normal text-12 
                      px-2 py-0.5 bg-red-400 hover:shadow-md hover:shadow-red-200 duration-200 rounded-full
                      active:scale-95"
                    >
                      <AiFillDelete className="text-16 " /> Eliminar
                    </button>
                    <button
                      onClick={() => setConfirmClearDebt(true)}
                      className="flex items-center gap-1 text-white font-secondary font-normal text-12 
                      px-2 py-0.5 bg-emerald-400 hover:shadow-md hover:shadow-emerald-200 duration-200 rounded-full
                      active:scale-95"
                    >
                      <MdAccountBalanceWallet className="text-16 " /> Zerar Divida
                    </button>
                  </div>
                ) : (
                  <span className="text-[13px] font-normal text-slate-500">Total: {clients.length}</span>
                )}
              </div>
            </div>
          </div>

          <div
            className="lg:flex hidden items-center justify-center gap-1 text-slate-500
             hover:text-slate-400 duration-200 cursor-pointer border-l"
          >
            <span className="text-[13px] font-normal">CPF</span>
          </div>

          <div className="sm:flex hidden items-center col-span-1 justify-center gap-1 text-slate-500 hover:text-slate-400 duration-200 cursor-pointer border-l">
            <span className="text-[13px] font-normal">Telefone</span>
          </div>

          {/* <div className="xl:flex hidden items-center justify-center gap-1 col-span-2 text-slate-500 hover:text-slate-400 duration-200 cursor-pointer border-l">
            <span className="text-[13px] font-normal">Endereço</span>
          </div> */}

          <div className="xl:flex hidden items-center justify-center gap-1 col-span-2 text-slate-500 hover:text-slate-400 duration-200 cursor-pointer border-l">
            <span className="text-[13px] font-normal">Barcode</span>
          </div>

          <div className="xl:flex hidden items-center justify-center gap-1 col-span-1 text-slate-500 hover:text-slate-400 duration-200 cursor-pointer border-l">
            <span className="text-[13px] font-normal">Grupo</span>
          </div>

          {/* <div className="xl:flex hidden items-center justify-center gap-1 col-span-1 text-slate-500 hover:text-slate-400 duration-200 cursor-pointer border-l">
            <span className="text-[13px] font-normal ml-1">CEP</span>
          </div> */}

          <div
            onClick={() => {
              if (sort === 0) {
                // sort by price
                setSortedClients(
                  [...clients].sort((a, b) => (b.balance < a.balance ? -1 : b.balance > a.balance ? 1 : 0))
                );
                setSort(1);
              } else if (sort === 1) {
                // sort by balance
                setSortedClients(
                  [...clients].sort((a, b) => (b.balance > a.balance ? -1 : b.balance < a.balance ? 1 : 0))
                );
                setSort(2);
              } else {
                // sort by id
                setSortedClients([...clients].sort((a, b) => a._id.localeCompare(b._id)));
                setSort(0);
              }
            }}
            className="xl:flex hidden items-center justify-center gap-1 col-span-1 text-slate-500 hover:text-slate-400 duration-200 cursor-pointer border-l"
          >
            <span className="text-[13px] font-normal">Balance</span>
            {sort === 0 ? (
              <TiArrowUnsorted className="text-16 font-normal" />
            ) : sort === 1 ? (
              <TiArrowSortedDown className="text-16 font-normal" />
            ) : (
              <TiArrowSortedUp className="text-16 font-normal" />
            )}
          </div>

          <div
            className="lg:flex hidden items-center justify-center gap-1 text-slate-500
             hover:text-slate-400 duration-200 border-l col-span-1"
          >
            <span className="text-slate-500 font-display font-light text-14">Ações</span>
          </div>
        </div>

        {sortedClients.map((client, index) => (
          <div key={index} className={`flex flex-col gap-y-1 w-full px-3 py-2 duration-200 border-t hover:bg-slate-50`}>
            <div className="grid grid-cols-3 sm:grid-cols-5 lg:grid-cols-8 xl:grid-cols-10 items-center justify-between">
              <div className="flex items-center col-span-2 lg:col-span-2 xl:col-span-3">
                <div
                  onClick={(e) => handleDropDown(e, index)}
                  className="flex p-1 mr-2 rounded-full hover:bg-slate-200 duration-200 cursor-pointer"
                >
                  <MdOutlineKeyboardDoubleArrowDown
                    className={`${activeDropdown[index] && "-rotate-90"} text-slate-500 text-[18px] duration-200`}
                  />
                </div>
                <Checkbox
                  label={""}
                  checked={selected.includes(client._id)}
                  onChange={() => {
                    if (selected.includes(client._id)) {
                      setSelected(selected.filter((e) => e !== client._id));
                    } else {
                      setSelected([...selected, client._id]);
                    }
                  }}
                  color="bg-indigo-400"
                  checkBoxSize="h-[18px] w-[18px]"
                  rounded="rounded-[4px]"
                  disabled={false}
                  font="font-normal"
                  icon={undefined}
                />
                <div
                  onClick={() => {
                    setSelectedClientToViewTransactions(client);
                    setVisibleUserTransactionsDialog(true);
                  }}
                  className="flex flex-col items-start w-full cursor-pointer"
                >
                  <span className="text-14 font-medium text-slate-700">{client.name}</span>
                  <span className="text-12 font-normal text-slate-500">{client.email}</span>
                </div>
              </div>

              <div className="lg:flex hidden items-center justify-center gap-1 text-slate-500 hover:text-slate-400 duration-200 border-l">
                <span className="text-slate-500 font-display font-light text-14">{client.cpf}</span>
              </div>

              <div className="lg:flex hidden items-center justify-center gap-1 text-slate-500 hover:text-slate-400 duration-200 border-l col-span-1">
                <span className="text-slate-500 font-display font-light text-14">{client.phone}</span>
              </div>
              {/* 
              <div className="lg:flex hidden items-center justify-center gap-1 text-slate-500 hover:text-slate-400 duration-200 border-l col-span-2">
                <span className="text-slate-500 font-display font-light text-14">{client.address}</span>
              </div> */}

              {/* <div
                className="lg:flex hidden items-center justify-center gap-1 text-slate-500
             hover:text-slate-400 duration-200 border-l col-span-1"
              >
                <span className="text-slate-500 font-display font-light text-14">{client.cep}</span>
              </div> */}

              <div className="lg:flex hidden items-center justify-center gap-1 text-slate-500 hover:text-slate-400 duration-200 border-l col-span-2">
                <span className="text-slate-500 font-display font-light text-14">{client.rfid}</span>
              </div>

              <div className="lg:flex hidden items-center justify-center gap-1 text-slate-500 hover:text-slate-400 duration-200 border-l col-span-1">
                <span className="text-slate-500 font-display font-light text-14">{client.group}</span>
              </div>

              <div
                className={`lg:flex hidden items-center justify-center gap-1 hover:text-slate-400 duration-200 border-l col-span-1 ${
                  client.balance < 0 ? "text-red-400 font-normal" : "text-emerald-500 font-medium"
                }`}
              >
                <span className="font-display text-14">$R {Number(client.balance).toFixed(2)}</span>
              </div>

              <div className="xl:flex hidden items-center justify-center gap-1 col-span-1 text-slate-500 hover:text-slate-400 duration-200 border-l">
                <button
                  onClick={() => {
                    setFormData(client);
                    setEditClientDialog(true);
                  }}
                  className="flex items-center gap-2 text-slate-500 font-secondary font-normal text-12 px-2 py-0.5 
                rounded-md hover:scale-105 duration-150 border bg-slate-200"
                >
                  <AiFillEdit className="text-[18px]" /> Editar
                </button>
              </div>
            </div>
            {activeDropdown[index] && (
              <div className="flex flex-col gap-y-1 px-3 py-2 duration-200 ml-6 border-t">
                <span className="text-14 font-medium text-slate-700">Ultimas compras</span>
              </div>
            )}
          </div>
        ))}
      </div>
      <Dialog
        header="Confirmar"
        visible={confirmDelete}
        style={{ width: "50vw" }}
        onHide={() => setConfirmDelete(false)}
        footer={
          <div className="flex items-center gap-1">
            <button
              onClick={() => setConfirmDelete(false)}
              className="bg-white hover:bg-red-400 hover:text-white text-slate-500 text-14 font-normal 
        py-1 px-3 rounded-md border duration-200 shadow-sm shadow-indigo-200 active:scale-95"
            >
              Cancelar
            </button>
            <button
              onClick={() => handleDeleteClients()}
              className="bg-indigo-500 hover:bg-indigo-400 text-white text-14 font-normal 
                  py-1 px-3 rounded-md duration-200 shadow-md shadow-indigo-200 active:scale-95"
            >
              Confirmar
            </button>
          </div>
        }
      >
        <div className="mx-2 flex overflow-hidden">
          <span className="text-slate-500 font-display font-normal text-14">
            Tem certeza que deseja eliminar os clientes selecionados?
          </span>
        </div>
      </Dialog>
      <Dialog
        header="Confirmar Limpar Divida"
        visible={confirmClearDebt}
        style={{ width: "50vw" }}
        onHide={() => setConfirmClearDebt(false)}
        footer={
          <div className="flex items-center gap-1">
            <button
              onClick={() => setConfirmClearDebt(false)}
              className="bg-white hover:bg-red-400 hover:text-white text-slate-500 text-14 font-normal 
        py-1 px-3 rounded-md border duration-200 shadow-sm shadow-indigo-200 active:scale-95"
            >
              Cancelar
            </button>
            <button
              onClick={() => handleClearDebt()}
              className="bg-indigo-500 hover:bg-indigo-400 text-white text-14 font-normal 
                  py-1 px-3 rounded-md duration-200 shadow-md shadow-indigo-200 active:scale-95"
            >
              Confirmar
            </button>
          </div>
        }
      >
        <div className="mx-2 flex overflow-hidden">
          <span className="text-slate-500 font-display font-normal text-14">
            Tem certeza que deseja zerar a divida dos clientes selecionados?
          </span>
        </div>
      </Dialog>

      <Dialog
        header="Editar informações do cliente"
        visible={editClientDialog}
        style={{ width: "50vw" }}
        onHide={() => setEditClientDialog(false)}
        footer={
          <div className="flex items-center gap-1">
            <button
              onClick={() => setEditClientDialog(false)}
              className="bg-white hover:bg-red-400 hover:text-white text-slate-500 text-14 font-normal 
        py-1 px-3 rounded-md border duration-200 shadow-sm shadow-indigo-200 active:scale-95"
            >
              Cancelar
            </button>
            <button
              onClick={() => handleUpdateClient()}
              className="bg-indigo-500 hover:bg-indigo-400 text-white text-14 font-normal 
                  py-1 px-3 rounded-md duration-200 shadow-md shadow-indigo-200 active:scale-95"
            >
              Confirmar
            </button>
          </div>
        }
      >
        <Accordion activeIndex={1} className="my-2">
          <AccordionTab header="Informações do cliente">
            <div className="flex flex-col gap-y-2 font-secondary">
              <div className="flex flex-col w-full mx-1">
                <span className="text-14 text-gray-500 font-normal">Nome do cliente</span>
                <input
                  className="relative w-full h-10 cursor-text text-left font-normal sm:text-14 dark:bg-secondary-dark-bg dark:text-white
              focus:outline-none bg-inherit focus-visible:border-1 focus-visible:ring-1 focus-visible:ring-white 
              focus-visible:ring-opacity-75 focus-visible:ring-offset-0 px-2 border rounded-md"
                  name="name_of_client"
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  placeholder={`Entre o nome do cliente`}
                  autoComplete="off"
                ></input>
              </div>

              <div className="flex flex-col w-full mx-1">
                <span className="text-14 text-gray-500 font-normal">email</span>
                <input
                  className="relative w-full h-10 cursor-text text-left font-normal sm:text-14 dark:bg-secondary-dark-bg dark:text-white
              focus:outline-none bg-inherit focus-visible:border-1 focus-visible:ring-1 focus-visible:ring-white 
              focus-visible:ring-opacity-75 focus-visible:ring-offset-0 px-2 border rounded-md"
                  name="email"
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  placeholder={`Entre um email válido`}
                  autoComplete="off"
                ></input>
              </div>

              <div className="flex flex-col w-full mx-1">
                <span className="text-14 text-gray-500 font-normal">CPF</span>
                <input
                  className="relative w-full h-10 cursor-text text-left font-normal sm:text-14 dark:bg-secondary-dark-bg dark:text-white
              focus:outline-none bg-inherit focus-visible:border-1 focus-visible:ring-1 focus-visible:ring-white 
              focus-visible:ring-opacity-75 focus-visible:ring-offset-0 px-2 border rounded-md"
                  name="cpf"
                  type="text"
                  value={formData.cpf}
                  onChange={(e) => setFormData({ ...formData, cpf: e.target.value })}
                  placeholder={`000.000.000-00`}
                  autoComplete="off"
                ></input>
              </div>

              <div className="flex flex-col w-full mx-1">
                <span className="text-14 text-gray-500 font-normal">Telefone</span>
                <input
                  className="relative w-full h-10 cursor-text text-left font-normal sm:text-14 dark:bg-secondary-dark-bg dark:text-white
              focus:outline-none bg-inherit focus-visible:border-1 focus-visible:ring-1 focus-visible:ring-white 
              focus-visible:ring-opacity-75 focus-visible:ring-offset-0 px-2 border rounded-md"
                  name="phone"
                  type="text"
                  value={formData.phone}
                  onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                  placeholder={`(00) 00000-0000`}
                  autoComplete="off"
                ></input>
              </div>

              <div className="flex flex-col w-full mx-1">
                <span className="text-14 text-gray-500 font-normal">Endereço</span>
                <input
                  className="relative w-full h-10 cursor-text text-left font-normal sm:text-14 dark:bg-secondary-dark-bg dark:text-white
              focus:outline-none bg-inherit focus-visible:border-1 focus-visible:ring-1 focus-visible:ring-white 
              focus-visible:ring-opacity-75 focus-visible:ring-offset-0 px-2 border rounded-md"
                  name="address"
                  type="text"
                  value={formData.address}
                  onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                  placeholder={`Rua, numero, bairro`}
                  autoComplete="off"
                ></input>
              </div>

              <div className="flex flex-col w-full mx-1">
                <span className="text-14 text-gray-500 font-normal">Grupo</span>
                <input
                  className="relative w-full h-10 cursor-text text-left font-normal sm:text-14 dark:bg-secondary-dark-bg dark:text-white
              focus:outline-none bg-inherit focus-visible:border-1 focus-visible:ring-1 focus-visible:ring-white 
              focus-visible:ring-opacity-75 focus-visible:ring-offset-0 px-2 border rounded-md"
                  name="group"
                  type="text"
                  value={formData.group}
                  onChange={(e) => setFormData({ ...formData, group: e.target.value })}
                  placeholder={`regular`}
                  autoComplete="off"
                ></input>
              </div>

              <div className="flex flex-col w-full mx-1">
                <span className="text-14 text-gray-500 font-normal">CEP</span>
                <input
                  className="relative w-full h-10 cursor-text text-left font-normal sm:text-14 dark:bg-secondary-dark-bg dark:text-white
              focus:outline-none bg-inherit focus-visible:border-1 focus-visible:ring-1 focus-visible:ring-white 
              focus-visible:ring-opacity-75 focus-visible:ring-offset-0 px-2 border rounded-md"
                  name="cep"
                  type="text"
                  value={formData.cep}
                  onChange={(e) => setFormData({ ...formData, cep: e.target.value })}
                  placeholder={`00000-000`}
                  autoComplete="off"
                ></input>
              </div>

              <div className="flex flex-col w-full mx-1">
                <span className="text-14 text-gray-500 font-normal">RFID</span>
                <textarea
                  className="relative w-full h-20 cursor-text text-left font-normal sm:text-14 dark:bg-secondary-dark-bg dark:text-white
              focus:outline-none bg-inherit focus-visible:border-1 focus-visible:ring-1 focus-visible:ring-white 
              focus-visible:ring-opacity-75 focus-visible:ring-offset-0 px-2 border rounded-md"
                  name="rfid"
                  value={formData.rfid}
                  onChange={(e) => setFormData({ ...formData, rfid: e.target.value })}
                  placeholder={`rfid do cartão do cliente`}
                  autoComplete="off"
                ></textarea>
              </div>
            </div>
          </AccordionTab>
          <AccordionTab header="Credito do cliente">
            <div className="flex flex-col w-full mx-1">
              <span className="text-14 text-gray-500 font-normal">Credito do cliente</span>
              <input
                className="relative w-full h-10 cursor-text text-left font-normal sm:text-14 dark:bg-secondary-dark-bg dark:text-white
              focus:outline-none bg-inherit focus-visible:border-1 focus-visible:ring-1 focus-visible:ring-white 
              focus-visible:ring-opacity-75 focus-visible:ring-offset-0 px-2 border rounded-md"
                name="balance"
                type="number"
                value={formData.balance}
                onChange={(e) => setFormData({ ...formData, balance: e.target.value })}
                placeholder={`0`}
                autoComplete="off"
              ></input>
            </div>
          </AccordionTab>
        </Accordion>
      </Dialog>

      <Sidebar
        visible={visibleUserTransactionsDialog}
        position="right"
        style={{ width: "100%", maxWidth: "70%" }}
        onHide={() => setVisibleUserTransactionsDialog(false)}
      >
        <div className="flex flex-col gap-y-2 w-full">
          <span className="text-20 font-medium text-slate-700">Ultimas compras</span>
          <div id="divider" className="w-full h-[1px] bg-slate-200"></div>

          <div className="flex flex-col border rounded-md shadow-sm p-3 gap-y-1">
            <div className="flex items-center justify-between">
              <span className="text-14 font-normal text-slate-500">
                Cliente: {selectedClientToViewTransactions.name}
              </span>
              <span className="text-14 font-normal text-slate-500">
                Email: {selectedClientToViewTransactions.email}
              </span>
            </div>

            <div id="divider" className="w-full h-[1px] bg-slate-200"></div>
            <span className="text-14 font-normal text-slate-500">
              Balance: {selectedClientToViewTransactions.balance}
            </span>
            <div id="divider" className="w-full h-[1px] bg-slate-200"></div>
            <span className="text-14 font-normal text-slate-500">Grupo: {selectedClientToViewTransactions.group}</span>
            <div id="divider" className="w-full h-[1px] bg-slate-200"></div>
            <span className="text-14 font-normal text-slate-500">CPF: {selectedClientToViewTransactions.cpf}</span>
            <div id="divider" className="w-full h-[1px] bg-slate-200"></div>
            <span className="text-14 font-normal text-slate-500">
              Telefone: {selectedClientToViewTransactions.phone}
            </span>
            <div id="divider" className="w-full h-[1px] bg-slate-200"></div>
            <span className="text-14 font-normal text-slate-500">
              Endereço: {selectedClientToViewTransactions.address}
            </span>
            <div id="divider" className="w-full h-[1px] bg-slate-200"></div>
            <span className="text-14 font-normal text-slate-500">CEP: {selectedClientToViewTransactions.cep}</span>
            <div id="divider" className="w-full h-[1px] bg-slate-200"></div>
            <span className="text-14 font-normal text-slate-500">RFID: {selectedClientToViewTransactions.rfid}</span>
          </div>

          {isLoadingSummaryOfTransactions ? (
            <div className="flex items-center justify-center mt-10">
              <ProgressSpinner
                style={{ width: "80px", height: "80px" }}
                strokeWidth="4"
                fill="var(--surface-ground)"
                animationDuration="1.2s"
              />
            </div>
          ) : (
            <div className="flex flex-col gap-y-2 w-full mt-4">
              <div className="flex flex-wrap gap-4 items-center justify-between w-full">
                <SelectButton value={option} onChange={(e) => setOption(e.value)} options={options} />
                <SelectButton value={viewOption} onChange={(e) => setViewOption(e.value)} options={viewOptions} />
              </div>

              <TotalSummary
                transactionsSummary={transactionsSummaryByClient}
                items={items}
                activateDropdown={false}
                width="w-full"
              />
              <DailySummary
                transactionsSummary={transactionsSummaryByClient}
                items={items}
                activateDropdown={false}
                width="w-full"
              />
            </div>
          )}
        </div>
      </Sidebar>
    </div>
  );
};

export default ClientsList;
