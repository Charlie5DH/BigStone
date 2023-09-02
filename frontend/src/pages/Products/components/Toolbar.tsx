import { AiOutlineSearch } from "react-icons/ai";
import { BiSelectMultiple } from "react-icons/bi";
import { SelectButton } from "primereact/selectbutton";
import { GenericButton, Input } from "../../../components";
import { Dropdown } from "primereact/dropdown";
import React from "react";
import { Dialog } from "primereact/dialog";
import axios from "axios";
import { useDispatch } from "react-redux";
import { createItem } from "../../../actions/items";

const generateUniqueHex16 = () => {
  return Math.floor(Math.random() * 0xffffffffffffffff).toString(16);
};

const Toolbar = () => {
  const [selectedCategory, setSelectedCategory] = React.useState(null);
  const [inputTextFilter, setInputTextFilter] = React.useState("");
  const options = ["Cards", "List"];
  const [file, setFile] = React.useState();
  const dispatch = useDispatch();
  const [formData, setFormData] = React.useState({
    name: "",
    description: "Novo produto",
    category: "",
    quantity: 0,
    price: 0.99,
    barcode: generateUniqueHex16(),
    image: "",
    tags: [],
  });

  const [visibleNewProdDialog, setVisibleNewProdDialog] = React.useState(false);
  const productsCategories = [
    { name: "Todos", code: "all" },
    { name: "Bebidas", code: "Beb" },
    { name: "Carnes", code: "Car" },
    { name: "Congelados", code: "Cong" },
    { name: "Doces", code: "Dcs" },
    { name: "Higiene", code: "Hig" },
    { name: "Limpeza", code: "Limp" },
    { name: "Padaria", code: "Pad" },
    { name: "Pet", code: "Pet" },
    { name: "Verduras e Legumes", code: "Verd" },
  ];

  const selectedCategoryTemplate = (option, props) => {
    if (option) {
      return (
        <div className="flex align-items-center">
          <div>{option.name}</div>
        </div>
      );
    }

    return <span>{props.placeholder}</span>;
  };

  const categoryOptionTemplate = (option) => {
    return (
      <div className="flex align-items-center">
        <div>{option.name}</div>
      </div>
    );
  };

  const footerContent = (
    <div>
      <button
        onClick={() => setVisibleNewProdDialog(false)}
        className="bg-white hover:bg-red-400 hover:text-white text-red-400 text-14 font-normal 
        py-1.5 px-4 rounded-md duration-200 shadow-sm shadow-red-200 active:scale-95 border border-red-200"
      >
        Cancelar
      </button>
      <button
        onClick={() => handleNewProduct()}
        className="bg-emerald-500 hover:bg-emerald-400 text-white text-14 font-normal 
                  py-1.5 px-4 rounded-md duration-200 shadow-md shadow-emerald-300 active:scale-95"
      >
        Confirmar
      </button>
    </div>
  );

  const handleNewProduct = () => {
    setVisibleNewProdDialog(false);

    if (file) {
      const headers = { "Content-Type": "multipart/form-data" };
      const imageFormData = new FormData();
      imageFormData.append("file", file);
      axios.post("http://localhost:8003/api/upload_image", imageFormData, { headers: headers }).then((res) => {
        console.log(res);
      });
    }

    dispatch(
      createItem({
        name: formData.name,
        description: formData.description,
        category: formData.category,
        quantity: formData.quantity,
        price: formData.price,
        barcode: formData.barcode,
        image: file ? file.name : "",
        tags: formData.tags,
      })
    );
  };

  return (
    <div className="flex items-center bg-white h-full max-h-40 w-full rounded-b-md border p-3 shadow-sm">
      <div className="flex flex-wrap gap-2 items-center justify-between w-full">
        <div className="flex flex-wrap items-center gap-3">
          <Input
            value={inputTextFilter}
            icon={<AiOutlineSearch className="text-slate-500 text-20 mr-2" />}
            onChange={(e) => setInputTextFilter(e.target.value)}
            placeholder="Procurar por nome, código ou categoria"
          />

          <Dropdown
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.value)}
            options={productsCategories}
            optionLabel="name"
            placeholder="Selecione uma categoria"
            filter
            valueTemplate={selectedCategoryTemplate}
            itemTemplate={categoryOptionTemplate}
            className="w-full md:w-60"
          />
        </div>

        <div className="flex items-center gap-2">
          {/* <SelectButton value={value} onChange={(e) => setValue(e.value)} options={options} /> */}
          {/* <GenericButton
            text="Selecionar Produtos"
            icon={<BiSelectMultiple className="text-slate-400 text-20 mr-2" color={"slate-500"} />}
            onClick={undefined}
            bgColor={undefined}
          /> */}
          <GenericButton
            text="+ Novo Produto"
            color={"white"}
            bgColor={"bg-emerald-500"}
            onClick={() => setVisibleNewProdDialog(true)}
            icon={undefined}
          />
        </div>

        <Dialog
          header={`Criar novo produto`}
          visible={visibleNewProdDialog}
          style={{ width: "100%", maxWidth: "640px" }}
          onHide={() => setVisibleNewProdDialog(false)}
          footer={footerContent}
        >
          <div className="flex flex-col gap-y-2 font-secondary">
            <div className="flex flex-col w-full mx-1">
              <span className="text-14 text-gray-500 font-normal">Nome do produto</span>
              <input
                className="relative w-full h-10 cursor-text text-left font-normal sm:text-14 dark:bg-secondary-dark-bg dark:text-white
              focus:outline-none bg-inherit focus-visible:border-1 focus-visible:ring-1 focus-visible:ring-white 
              focus-visible:ring-opacity-75 focus-visible:ring-offset-0 px-2 border rounded-md"
                name="name"
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                placeholder={`Entre o nome do produto`}
                autoComplete="off"
              ></input>
            </div>

            <form className="flex items-center w-full">
              <label className="block w-full mx-1 rounded-md">
                <span className="text-14 text-gray-500 font-normal">Selecione uma imagem</span>
                <input
                  type="file"
                  name="image"
                  accept="image/*"
                  lang="pt-br"
                  onChange={(e) => setFile(e.target.files[0])}
                  className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 rounded-md border file:cursor-pointer file:duration-200
                  file:border-0 file:text-sm file:font-semibold file:bg-indigo-400 file:text-white hover:file:bg-blue-100"
                />
              </label>
            </form>

            <div className="flex flex-col w-full mx-1">
              <span className="text-14 text-gray-500 font-normal">Descrição</span>
              <textarea
                className="relative w-full h-32 p-2 cursor-text text-left font-light sm:text-14 dark:bg-secondary-dark-bg dark:text-white
              focus:outline-none bg-inherit focus-visible:border-1 focus-visible:ring-1 focus-visible:ring-white 
              focus-visible:ring-opacity-75 focus-visible:ring-offset-0 px-2 border rounded-md"
                name="description"
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                placeholder={`Descrição do produto`}
                autoComplete="off"
              ></textarea>
            </div>

            <div className="flex items-center gap-2 mx-1 w-full">
              <div className="flex flex-col w-full">
                <span className="text-12 text-gray-500 font-normal">Quantidade</span>
                <input
                  className="relative w-full h-10 cursor-text text-left font-light sm:text-14 dark:bg-secondary-dark-bg dark:text-white
              focus:outline-none bg-inherit focus-visible:border-1 focus-visible:ring-1 focus-visible:ring-white 
              focus-visible:ring-opacity-75 focus-visible:ring-offset-0 px-2 border rounded-md"
                  name="quantity"
                  type="number"
                  min={0}
                  value={formData.quantity}
                  onChange={(e) => setFormData({ ...formData, quantity: e.target.value })}
                  placeholder={`Quantidade`}
                  autoComplete="off"
                ></input>
              </div>

              <div className="flex flex-col w-full">
                <span className="text-12 text-gray-500 font-normal">Preço</span>
                <input
                  className="relative w-full h-10 cursor-text text-left font-light sm:text-14 dark:bg-secondary-dark-bg dark:text-white
              focus:outline-none bg-inherit focus-visible:border-1 focus-visible:ring-1 focus-visible:ring-white 
              focus-visible:ring-opacity-75 focus-visible:ring-offset-0 px-2 border rounded-md"
                  name="price"
                  type="number"
                  value={formData.price}
                  min={0}
                  onChange={(e) => setFormData({ ...formData, price: e.target.value })}
                  placeholder={`Preço do produto`}
                  autoComplete="off"
                ></input>
              </div>
            </div>

            <div className="flex flex-col w-full mx-1">
              <span className="text-12 text-gray-500 font-normal">Codigo de barras</span>
              <input
                className="relative w-full h-10 cursor-text text-left font-light sm:text-14 dark:bg-secondary-dark-bg dark:text-white
              focus:outline-none bg-inherit focus-visible:border-1 focus-visible:ring-1 focus-visible:ring-white 
              focus-visible:ring-opacity-75 focus-visible:ring-offset-0 px-2 border rounded-md"
                name="barcode"
                value={formData.barcode}
                onChange={(e) => setFormData({ ...formData, barcode: e.target.value })}
                placeholder={`Barcode`}
                autoComplete="off"
              ></input>
            </div>
          </div>
        </Dialog>
      </div>
    </div>
  );
};

export default Toolbar;
