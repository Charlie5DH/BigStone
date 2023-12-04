/* eslint-disable react/prop-types */
import { Dialog } from "primereact/dialog";
import React, { useState } from "react";
import SelectClientDialog from "./SelectClientDialog";

const NewSaleDialog = ({
  items,
  client,
  kg_price,
  setClient,
  websocketData,
  transactionForm,
  setTransactionForm,
  setWebsocketData,
  newTransactionDialogVisible,
  setNewTransactionDialogVisible,
  setViewInsertProductDialog,
  handleCreateNewTransaction,
}) => {
  const [selectClientDialogVisible, setSelectClientDialogVisible] = useState(false);

  return (
    <Dialog
      header="Nova venda"
      visible={newTransactionDialogVisible}
      style={{ width: "100%", maxWidth: "60vw" }}
      onHide={() => {
        setNewTransactionDialogVisible(false);
        setWebsocketData({});
        setClient({});
        setTransactionForm({
          ...transactionForm,
          items: [],
        });
      }}
      footer={
        client.name && (
          <div className="flex justify-between items-center gap-1">
            <button
              onClick={() => setViewInsertProductDialog(true)}
              className="bg-emerald-500 hover:bg-emerald-400 text-white text-14 font-normal 
                  py-2 px-3 rounded-md duration-200 shadow-md shadow-emerald-200 active:scale-95"
            >
              + Adicionar produtos
            </button>

            <div className="flex justify-end items-center gap-1">
              <button
                onClick={() => {
                  setNewTransactionDialogVisible(false);
                  setWebsocketData({});
                  setClient({});
                  setTransactionForm({
                    ...transactionForm,
                    items: [],
                  });
                }}
                className="bg-white hover:bg-red-400 hover:text-white text-slate-500 text-14 font-normal 
        py-2 px-3 rounded-md border duration-200 shadow-sm shadow-red-200 active:scale-95"
              >
                Cancelar
              </button>
              <button
                onClick={() => handleCreateNewTransaction()}
                className={`bg-indigo-500 hover:bg-indigo-400 text-white text-14 font-normal border border-slate-300 
                  py-2 px-3 rounded-md duration-200 shadow-md shadow-indigo-200 active:scale-95`}
              >
                Confirmar
              </button>
            </div>
          </div>
        )
      }
    >
      <SelectClientDialog
        visible={selectClientDialogVisible}
        setVisible={setSelectClientDialogVisible}
        setClient={setClient}
        transactionForm={transactionForm}
        setTransactionForm={setTransactionForm}
      />

      <React.Fragment>
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
              {client.name ? (
                <span className="text-16 font-semibold">{client.name}</span>
              ) : (
                <button
                  onClick={() => setSelectClientDialogVisible(true)}
                  className="bg-indigo-500 hover:bg-indigo-400 text-white text-14 font-normal border border-slate-300 
                py-2 px-3 rounded-md duration-200 shadow-md shadow-indigo-200 active:scale-95"
                >
                  + Cliente
                </button>
              )}
            </div>

            <div className="flex items-center justify-center gap-1 text-slate-500">
              <span className="text-16 font-semibold">{websocketData.weight ? websocketData.weight : "0"} Kg</span>
            </div>

            <div className="flex items-center justify-center gap-1 text-slate-500">
              <span className="text-16 font-semibold">R$ {kg_price}</span>
            </div>

            <div className="flex items-center justify-center gap-1 text-slate-500">
              <span className="text-16 font-semibold">
                R$ {websocketData.weight ? Number(websocketData.weight * kg_price).toFixed(2) : 0}
              </span>
            </div>
          </div>
        </div>

        {transactionForm.items.length > 0 ? (
          <div className="flex flex-col gap-y-1 py-2 duration-200">
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
                        {Number(item.quantity * items.find((produto) => produto._id === item.item_id).price).toFixed(2)}
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
        <div className="flex flex-col gap-y-2 mt-4 border rounded-md shadow-sm bg-slate-50 p-4">
          <span className="text-16 font-medium text-slate-600">Resumo</span>
          <span className="text-16 font-medium text-slate-600 border-t py-1">
            Total em produtos: $R{" "}
            {transactionForm.items.reduce(
              (acc, item) => acc + item.quantity * items.find((produto) => produto._id === item.item_id).price,
              0
            ) || 0}
          </span>
          <span className="text-16 font-medium text-slate-600 border-t py-1">
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
      </React.Fragment>
    </Dialog>
  );
};

export default NewSaleDialog;
