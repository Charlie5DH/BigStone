/* eslint-disable react/prop-types */
import React from "react";
import { GenericButton, Input } from "../../../components";
import { AiOutlineSearch } from "react-icons/ai";
import { Dropdown } from "primereact/dropdown";
import { createClient } from "../../../actions/clients";
import { Dialog } from "primereact/dialog";
import { useDispatch } from "react-redux";

const createRandomCPF = () => {
  let cpf = "";
  for (let i = 0; i < 11; i++) {
    cpf += Math.floor(Math.random() * 10);
  }
  return cpf;
};

const Toolbar = () => {
  const [selectedClientOption, setSelectedClientOption] = React.useState(null);
  const [inputTextFilter, setInputTextFilter] = React.useState("");
  const [visibleClientDialog, setVisibleClientDialog] = React.useState(false);
  const dispatch = useDispatch();
  const [formData, setFormData] = React.useState({
    name: "",
    email: "",
    cpf: createRandomCPF(),
    phone: "(48)99-987-1234",
    address: "Rua XXX, 123",
    group: "regular",
    cep: "",
    balance: 0,
    rfid: "",
  });

  // React.useEffect(() => {
  //   setFormData({ ...formData, cpf: createRandomCPF() });
  // }, [visibleClientDialog]);

  const clientesOptions = [
    { name: "Todos", code: "all" },
    { name: "Com Dividas", code: "div" },
    { name: "Sem dividas", code: "sdiv" },
  ];

  const selectedClientOptionTemplate = (option, props) => {
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
        onClick={() => setVisibleClientDialog(false)}
        className="bg-white hover:bg-red-400 hover:text-white text-red-400 text-14 font-normal 
        py-1.5 px-4 rounded-md duration-200 shadow-sm shadow-red-200 active:scale-95 border border-red-200"
      >
        Cancelar
      </button>
      <button
        disabled={formData.name === "" || formData.email === "" || !formData.email.includes("@")}
        onClick={() => handleNewClient()}
        className="bg-emerald-500 hover:bg-emerald-400 text-white text-14 font-normal disabled:opacity-50
        disabled:cursor-not-allowed py-1.5 px-4 rounded-md duration-200 shadow-md shadow-emerald-300 active:scale-95"
      >
        Confirmar
      </button>
    </div>
  );

  const handleNewClient = () => {
    setVisibleClientDialog(false);

    dispatch(createClient(formData));
    setFormData({
      name: "Novo Cliente",
      email: "nomedocliente@exemplo.com",
      cpf: createRandomCPF(),
      phone: "(48)99-987-1234",
      address: "Rua XXX, 123",
      group: "regular",
      cep: "79311-571",
      balance: 0,
      rfid: "",
    });
  };

  return (
    <div className="flex items-center bg-white h-full max-h-40 w-full rounded-b-md border p-3 shadow-sm">
      <div className="flex flex-wrap gap-2 items-center justify-between w-full">
        <div className="flex flex-wrap items-center gap-3">
          <Input
            value={inputTextFilter}
            icon={<AiOutlineSearch className="text-slate-500 text-20 mr-2" />}
            onChange={(e) => setInputTextFilter(e.target.value)}
            placeholder="Procurar cliente por nome ou email"
          />

          <Dropdown
            value={selectedClientOption}
            onChange={(e) => setSelectedClientOption(e.value)}
            options={clientesOptions}
            optionLabel="name"
            placeholder="Filtrar por dividas"
            filter
            valueTemplate={selectedClientOptionTemplate}
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
            text="+ Novo Cliente"
            color={"white"}
            bgColor={"bg-emerald-500"}
            onClick={() => setVisibleClientDialog(true)}
            icon={undefined}
          />
        </div>

        <Dialog
          header={`Criar novo produto`}
          visible={visibleClientDialog}
          style={{ width: "100%", maxWidth: "640px" }}
          onHide={() => setVisibleClientDialog(false)}
          footer={footerContent}
        >
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
        </Dialog>
      </div>
    </div>
  );
};

export default Toolbar;
