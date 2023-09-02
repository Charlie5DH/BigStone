/* eslint-disable no-unused-vars */
/* eslint-disable react/prop-types */
import React from "react";
import { AiFillDelete, AiFillEdit, AiFillTags } from "react-icons/ai";
import { MdCategory } from "react-icons/md";
import { TiArrowSortedDown, TiArrowSortedUp, TiArrowUnsorted } from "react-icons/ti";
import { IoMdTime } from "react-icons/io";
import Checkbox from "../Inputs/Checkbox";
import { Dialog } from "primereact/dialog";
import ProductCard from "../Cards/ProductCard";
import { deleteManyItems, updateItemQuantity } from "../../actions/items";
import { useDispatch } from "react-redux";

const ProductsList = ({ products }) => {
  const [sort, setSort] = React.useState(0);
  const [sortedProducts, setSortedProducts] = React.useState(products);
  const [selected, setSelected] = React.useState([]);
  const [visibleProdutDialog, setVisibleProdutDialog] = React.useState(false);
  const [selectedProduct, setSelectedProduct] = React.useState({});
  const [visibleRestockDialog, setVisibleRestockDialog] = React.useState(false);
  const [confirmDelete, setConfirmDelete] = React.useState(false);
  const [quantity, setQuantity] = React.useState(0);

  const dispatch = useDispatch();

  React.useEffect(() => {
    setSortedProducts(products);
  }, [products]);

  const handleSelectedProduct = (product) => {
    setSelectedProduct(product);
    setQuantity(product.quantity);
    setVisibleProdutDialog(true);
  };

  const handleUpdateQuantity = () => {
    // update quantity of selected product
    dispatch(
      updateItemQuantity(selectedProduct._id, quantity, {
        name: "username",
        email: "useremail@email.com",
        _id: "99999999999",
      })
    );
    setVisibleRestockDialog(false);
  };

  const footerContent = (
    <div>
      <button
        onClick={() => setVisibleRestockDialog(false)}
        className="bg-white hover:bg-red-400 hover:text-white text-slate-500 text-14 font-normal 
        py-1.5 px-4 rounded-md border duration-200 shadow-sm shadow-indigo-200 active:scale-95"
      >
        Cancelar
      </button>
      <button
        onClick={() => handleUpdateQuantity()}
        className="bg-indigo-500 hover:bg-indigo-400 text-white text-14 font-normal 
                  py-1.5 px-4 rounded-md duration-200 shadow-md shadow-indigo-200 active:scale-95"
      >
        Confirmar
      </button>
    </div>
  );

  const handleDeleteClients = () => {
    // delete selected clients
    setConfirmDelete(false);
    dispatch(deleteManyItems(JSON.stringify(selected)));
    setSelected([]);
  };

  return (
    <div className="flex flex-nowrap items-center justify-center gap-2 w-full lg:w-[90%] font-display">
      <div className="flex flex-col items-center border rounded-md w-full my-3">
        <div
          className="grid grid-cols-3 sm:grid-cols-5 lg:grid-cols-9 xl:grid-cols-12 w-full items-center
         justify-between p-3 bg-slate-100"
        >
          <div className="flex items-start col-span-3 lg:col-span-5 xl:col-span-6">
            <div className="flex items-center gap-6">
              <Checkbox
                label={""}
                checked={selected.length === products.length && selected.length !== 0 ? true : false}
                onChange={() =>
                  setSelected(
                    selected.length === products.length && selected.length !== 0 ? [] : products.map((e) => e._id)
                  )
                }
                color="bg-indigo-400"
                checkBoxSize="h-[18px] w-[18px]"
                rounded="rounded-[4px]"
                disabled={false}
                font="font-normal"
                icon={undefined}
              />
              {selected.length !== 0 ? (
                <div className="lg:flex grid grid-cols-1 items-center gap-3">
                  <span className="text-[13px] font-normal text-slate-500">Selecionados: {selected.length}</span>
                  <button
                    onClick={() => setConfirmDelete(true)}
                    className="flex items-center gap-1 text-white font-secondary font-normal text-12 
                      px-2 py-0.5 bg-red-400 hover:shadow-md hover:shadow-red-200 duration-200 rounded-full
                      active:scale-95"
                  >
                    <AiFillDelete className="text-16 " /> Eliminar
                  </button>
                </div>
              ) : (
                <React.Fragment>
                  <span className="text-[13px] font-normal text-slate-500">Total: {sortedProducts.length}</span>
                  <span className="flex items-center gap-2 text-[13px] font-normal text-slate-500">
                    Zerado: {sortedProducts.filter((e) => e.quantity === 0).length}
                  </span>
                </React.Fragment>
              )}
            </div>
          </div>

          <div
            onClick={() => {
              if (sort === 0) {
                // sort by price
                setSortedProducts([...products].sort((a, b) => (b.price < a.price ? -1 : b.price > a.price ? 1 : 0)));
                setSort(1);
              } else if (sort === 1) {
                // sort by price
                setSortedProducts([...products].sort((a, b) => (b.price > a.price ? -1 : b.price < a.price ? 1 : 0)));
                setSort(2);
              } else {
                // sort by id
                setSortedProducts([...products].sort((a, b) => a.name.localeCompare(b.name)));
                setSort(0);
              }
            }}
            className="lg:flex hidden items-center justify-center gap-1 text-slate-500
           hover:text-slate-400 duration-200 cursor-pointer border-l"
          >
            <span className="text-[13px] font-normal">Preço</span>
            {sort === 0 ? (
              <TiArrowUnsorted className="text-16 font-normal" />
            ) : sort === 1 ? (
              <TiArrowSortedDown className="text-16 font-normal" />
            ) : (
              <TiArrowSortedUp className="text-16 font-normal" />
            )}
          </div>

          <div
            onClick={() => {
              if (sort === 0) {
                // sort by price
                setSortedProducts(
                  [...products].sort((a, b) => (b.quantity < a.quantity ? -1 : b.quantity > a.quantity ? 1 : 0))
                );
                setSort(1);
              } else if (sort === 1) {
                // sort by quantity
                setSortedProducts(
                  [...products].sort((a, b) => (b.quantity > a.quantity ? -1 : b.quantity < a.quantity ? 1 : 0))
                );
                setSort(2);
              } else {
                // sort by id
                setSortedProducts([...products].sort((a, b) => a.name.localeCompare(b.name)));
                setSort(0);
              }
            }}
            className="flex items-center justify-center gap-1 text-slate-500 hover:text-slate-400 duration-200 cursor-pointer border-l"
          >
            <span className="text-[13px] font-normal">Quantidade</span>
            {sort === 0 ? (
              <TiArrowUnsorted className="text-16 font-normal" />
            ) : sort === 1 ? (
              <TiArrowSortedDown className="text-16 font-normal" />
            ) : (
              <TiArrowSortedUp className="text-16 font-normal" />
            )}
          </div>

          <div className="sm:flex hidden items-center col-span-1 justify-center gap-1 text-slate-500 hover:text-slate-400 duration-200 cursor-pointer border-l">
            <span className="text-[13px] font-normal">Categoria</span>
          </div>

          <div
            onClick={() => {
              if (sort === 0) {
                // sort by price
                setSortedProducts(
                  [...products].sort((a, b) =>
                    b.sold_this_month < a.sold_this_month ? -1 : b.sold_this_month > a.sold_this_month ? 1 : 0
                  )
                );
                setSort(1);
              } else if (sort === 1) {
                // sort by sold_this_month
                setSortedProducts(
                  [...products].sort((a, b) =>
                    b.sold_this_month > a.sold_this_month ? -1 : b.sold_this_month < a.sold_this_month ? 1 : 0
                  )
                );
                setSort(2);
              } else {
                // sort by id
                setSortedProducts([...products].sort((a, b) => a.name.localeCompare(b.name)));
                setSort(0);
              }
            }}
            className="sm:flex hidden items-center col-span-1 justify-center gap-1 text-slate-500
             hover:text-slate-400 duration-200 cursor-pointer border-l"
          >
            <span className="text-[13px] font-normal">Vendas no mês</span>
            {sort === 0 ? (
              <TiArrowUnsorted className="text-16 font-normal" />
            ) : sort === 1 ? (
              <TiArrowSortedDown className="text-16 font-normal" />
            ) : (
              <TiArrowSortedUp className="text-16 font-normal" />
            )}
          </div>

          <div
            onClick={() => {
              if (sort === 0) {
                // sort by price
                setSortedProducts(
                  [...products].sort((a, b) =>
                    b.sold_this_week < a.sold_this_week ? -1 : b.sold_this_week > a.sold_this_week ? 1 : 0
                  )
                );
                setSort(1);
              } else if (sort === 1) {
                // sort by sold_this_week
                setSortedProducts(
                  [...products].sort((a, b) =>
                    b.sold_this_week > a.sold_this_week ? -1 : b.sold_this_week < a.sold_this_week ? 1 : 0
                  )
                );
                setSort(2);
              } else {
                // sort by id
                setSortedProducts([...products].sort((a, b) => a.name.localeCompare(b.name)));
                setSort(0);
              }
            }}
            className="lg:flex hidden items-center justify-center gap-1 text-slate-500 px-2
             hover:text-slate-400 duration-200 cursor-pointer border-l"
          >
            <span className="text-[13px] font-normal text-center">Na semana</span>
            {sort === 0 ? (
              <TiArrowUnsorted className="text-16 font-normal" />
            ) : sort === 1 ? (
              <TiArrowSortedDown className="text-16 font-normal" />
            ) : (
              <TiArrowSortedUp className="text-16 font-normal" />
            )}
          </div>

          <div
            onClick={() => {
              if (sort === 0) {
                // sort by price
                setSortedProducts(
                  [...products].sort((a, b) => (b.sold_today < a.sold_today ? -1 : b.sold_today > a.sold_today ? 1 : 0))
                );
                setSort(1);
              } else if (sort === 1) {
                // sort by sold_today
                setSortedProducts(
                  [...products].sort((a, b) => (b.sold_today > a.sold_today ? -1 : b.sold_today < a.sold_today ? 1 : 0))
                );
                setSort(2);
              } else {
                // sort by id
                setSortedProducts([...products].sort((a, b) => a.name.localeCompare(b.name)));
                setSort(0);
              }
            }}
            className="xl:flex hidden items-center justify-center gap-1 col-span-1 text-slate-500
           hover:text-slate-400 duration-200 cursor-pointer border-l"
          >
            <span className="text-[13px] font-normal">Vendas hoje</span>
            {sort === 0 ? (
              <TiArrowUnsorted className="text-16 font-normal" />
            ) : sort === 1 ? (
              <TiArrowSortedDown className="text-16 font-normal" />
            ) : (
              <TiArrowSortedUp className="text-16 font-normal" />
            )}
          </div>
        </div>

        {sortedProducts.map((product, index) => (
          <div
            key={index}
            className={`flex flex-col gap-y-1 w-full px-3 py-2 duration-200
          ${
            product.quantity === 0
              ? "border border-amber-100 bg-amber-50 hover:bg-yellow-50"
              : "border-t hover:bg-slate-50"
          }`}
          >
            <div
              key={index}
              className="grid grid-cols-3 sm:grid-cols-5 lg:grid-cols-9 xl:grid-cols-12 items-center justify-between"
            >
              <div className="flex items-center col-span-3 lg:col-span-5 xl:col-span-6 cursor-pointer">
                <Checkbox
                  label={""}
                  checked={selected.includes(product._id)}
                  onChange={() => {
                    if (selected.includes(product._id)) {
                      setSelected(selected.filter((e) => e !== product._id));
                    } else {
                      setSelected([...selected, product._id]);
                    }
                  }}
                  color="bg-indigo-400"
                  checkBoxSize="h-[18px] w-[18px]"
                  rounded="rounded-[4px]"
                  disabled={false}
                  font="font-normal"
                  icon={undefined}
                />
                <div onClick={() => handleSelectedProduct(product)} className="flex items-center w-full">
                  <img
                    src={`http://localhost:8003/api/get_image/${product.image}`} //"https://placehold.co/600x400" ||
                    alt="product"
                    className="rounded-md shadow-sm w-[72px] h-[72px] object-cover"
                  />
                  <div className="flex flex-col gap-y-1 ml-4">
                    <span className="text-14 font-medium text-slate-700">{product.name}</span>
                    <span className="text-12 font-normal text-slate-500">{product.description}</span>
                  </div>
                </div>
              </div>

              <div
                className="lg:flex hidden items-center justify-center gap-1 text-slate-500
           hover:text-slate-400 duration-200 border-l"
              >
                <span className="text-14 font-normal">$R {product.price}</span>
              </div>

              <div
                className="lg:flex lg:flex-col gap-y-1 hidden items-center justify-center gap-1 text-slate-500
           hover:text-slate-400 duration-200 border-l"
              >
                <span className="text-14 font-normal">{product.quantity}</span>
              </div>

              <div
                className="lg:flex hidden items-center justify-center gap-1 text-slate-500
           hover:text-slate-400 duration-200 border-l col-span-1"
              >
                <span className="text-slate-500 font-display font-light text-14">{product.category}</span>
              </div>

              <div
                className="lg:flex hidden items-center justify-center gap-1 text-slate-500
           hover:text-slate-400 duration-200 border-l col-span-1"
              >
                <span
                  className={`${
                    product.sold_this_month > 0 ? "text-emerald-500 font-medium" : "text-slate-500 font-normal"
                  } font-display text-14`}
                >
                  {product.sold_this_month}
                </span>
              </div>

              <div
                className="lg:flex hidden items-center justify-center gap-1 text-slate-500
           hover:text-slate-400 duration-200 border-l"
              >
                <span
                  className={`${
                    product.sold_this_week > 0 ? "text-emerald-500 font-medium underline" : "text-slate-500 font-normal"
                  } font-display text-14`}
                >
                  {product.sold_this_week}
                </span>
              </div>

              <div
                className="xl:flex hidden items-center justify-center gap-1 col-span-1 text-slate-500
           hover:text-slate-400 duration-200 border-l"
              >
                <span
                  className={`${
                    product.sold_today > 0 ? "text-emerald-500 font-medium underline" : "text-slate-500 font-normal"
                  } font-display text-14`}
                >
                  {product.sold_today}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>
      <Dialog
        header={`${selectedProduct?.name}`}
        visible={visibleProdutDialog}
        style={{ width: "640px" }}
        onHide={() => setVisibleProdutDialog(false)}
      >
        <div className="flex flex-col gap-y-1">
          <ProductCard
            product={products.find((e) => e._id === selectedProduct._id)}
            onButtonClick={() => setVisibleRestockDialog(true)}
          />
        </div>
      </Dialog>
      <Dialog
        header={`Modificar estoque de ${selectedProduct?.name}`}
        visible={visibleRestockDialog}
        style={{ width: "560px" }}
        onHide={() => setVisibleRestockDialog(false)}
        footer={footerContent}
      >
        <div className="flex flex-col gap-y-1">
          <div className="mx-2 flex overflow-hidden">
            <input
              className="relative w-full h-12 cursor-text text-left font-light sm:text-14 dark:bg-secondary-dark-bg dark:text-white
              focus:outline-none bg-inherit focus-visible:border-1 focus-visible:ring-1 focus-visible:ring-white 
              focus-visible:ring-opacity-75 focus-visible:ring-offset-0 px-2 mx-1 border rounded-md"
              name="quantity"
              type="number"
              value={quantity}
              onChange={(e) => setQuantity(e.target.value)}
              placeholder={`Quantidade atual: ${selectedProduct?.quantity}`}
              autoComplete="off"
            ></input>
          </div>
        </div>
      </Dialog>
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
    </div>
  );
};

export default ProductsList;
