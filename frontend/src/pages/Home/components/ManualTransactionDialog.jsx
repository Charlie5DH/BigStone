/* eslint-disable react/prop-types */
import { Dialog } from "primereact/dialog";
import SelectClientDialog from "./SelectClientDialog";
import { useState } from "react";

const ManualTransactionDialog = ({
  items,
  client,
  setClient,
  transactionForm,
  setTransactionForm,
  handleCreateNewManualTransaction,
  setViewInsertProductDialog,
  visibleNewManualTransaction,
  setVisibleNewManualTransaction,
}) => {
  const [selectClientDialogVisible, setSelectClientDialogVisible] = useState(false);

  return (
    <Dialog
      header={
        <div className="flex items-center gap-5 border-b pb-2">
          <span className="text-20 font-semibold text-slate-600">Nova transação manual para: </span>

          {client.name ? (
            <span className="text-20 font-medium font-secondary text-slate-600 px-3 py-1 border bg-slate-50 rounded-md">
              {client.name}
            </span>
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
      }
      visible={visibleNewManualTransaction}
      style={{ width: "100%", maxWidth: "50vw" }}
      onHide={() => setVisibleNewManualTransaction(false)}
      footer={
        client.name &&
        transactionForm.items.length !== 0 && (
          <div className="flex justify-between items-center gap-1">
            <button
              onClick={() => {
                setVisibleNewManualTransaction(false);
                setTransactionForm({ ...transactionForm, items: [] });
                setClient({});
              }}
              className="bg-white hover:bg-red-400 hover:text-white text-slate-500 text-14 font-normal 
        py-2 px-3 rounded-md border duration-200 shadow-sm shadow-indigo-200 active:scale-95"
            >
              Cancelar
            </button>
            <div className="flex justify-end items-center gap-1">
              <button
                onClick={() => handleCreateNewManualTransaction()}
                className="bg-indigo-500 hover:bg-indigo-400 text-white text-14 font-normal 
                  py-2 px-3 rounded-md duration-200 shadow-md shadow-indigo-200 active:scale-95"
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

      {transactionForm.items.length > 0 ? (
        <div className="flex flex-col gap-y-1  py-2 duration-200">
          <div className="flex items-center gap-3 text-slate-500">
            <span className="text-14 font-medium text-slate-700">Produtos adicionados</span>
            <button
              onClick={() => setViewInsertProductDialog(true)}
              className="bg-emerald-500 hover:bg-emerald-400 text-white text-14 font-normal 
                  h-8 w-8 rounded-full duration-200 shadow-md shadow-emerald-200 active:scale-95"
            >
              +
            </button>
          </div>
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
        <div className="flex items-center gap-1 text-slate-500">
          <span className="text-16 font-normal">Adicionar produtos</span>
          <button
            onClick={() => setViewInsertProductDialog(true)}
            className="bg-emerald-500 hover:bg-emerald-400 text-white text-14 font-normal 
                  h-8 w-8 rounded-full duration-200 shadow-md shadow-emerald-200 active:scale-95"
          >
            +
          </button>
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
          {Number(
            transactionForm.items.reduce(
              (acc, item) => acc + item.quantity * items.find((produto) => produto._id === item.item_id).price,
              0
            )
          ).toFixed(2) || 0}
        </span>
      </div>
    </Dialog>
  );
};

export default ManualTransactionDialog;
