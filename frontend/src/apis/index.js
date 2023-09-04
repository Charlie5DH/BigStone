import axios from "axios";
import moment from "moment";
export const testing = false;

export const CLIENT_API = axios.create({
  baseURL: testing ? "http://localhost:8003/api" : "http://localhost:8003/api",
});

export const getTransactions = (
  transaction_type = "sell",
  start_timestamp = moment().subtract(2, "days").format("YYYY-MM-DD"),
  end_timestamp = moment().format("YYYY-MM-DD")
) => CLIENT_API.get(`/transactions/${transaction_type}/${start_timestamp}/${end_timestamp}`);
export const getTransactionById = (id) => CLIENT_API.get(`/transaction/${id}`);
export const createTransaction = (newTransaction) => CLIENT_API.post("/transactions", newTransaction);
export const updateTransaction = (id, updatedTransaction) =>
  CLIENT_API.patch(`/transactions/${id}`, updatedTransaction);
export const deleteTransaction = (id) => CLIENT_API.delete(`/transactions/${id}`);

export const getCategories = () => CLIENT_API.get("/categories");
export const getItems = (add_daily_mean_sales = false, period = 30) =>
  CLIENT_API.get(`/items/${add_daily_mean_sales}/${period}`);
export const getItemById = (id) => CLIENT_API.get(`/items/${id}`);
export const postItem = (newItem) => CLIENT_API.post("/items/", newItem);
export const postManyItems = (newItems) => CLIENT_API.post("/items/many", newItems);
export const updateItem = (id, updatedItem) => CLIENT_API.put(`/items/${id}`, updatedItem);
export const updateItemQuantity = (id, quantity, user) => CLIENT_API.put(`/items/${id}/quantity/${quantity}`, user);
export const subtractItemQuantity = (id, quantity) => CLIENT_API.put(`/items/${id}/subtract_quantity`, quantity);
export const deleteItem = (id) => CLIENT_API.delete(`/items/${id}`);
export const deleteManyItems = (ids) => CLIENT_API.delete(`/items/${ids}`);

export const getSummaryOfTransactions = (period) => CLIENT_API.get(`/transactions/summary/${period}`);
export const getTransactionsSummaryByClient = (client_id, period) =>
  CLIENT_API.get(`/transactions/summary/${client_id}/period/${period}`);

export const getClients = () => CLIENT_API.get("/clients");
export const getClientById = (id) => CLIENT_API.get(`/client/${id}`);
export const postClient = (newClient) => CLIENT_API.post("/create_clients", newClient);
export const updateClient = (id, updatedClient) => CLIENT_API.patch(`/client/${id}`, updatedClient);
export const clearDebtOfClients = (ids) => CLIENT_API.put(`/clients/clear_debt/${ids}`);
export const deleteClient = (id) => CLIENT_API.delete(`/client/${id}`);
export const deleteClients = (ids) => CLIENT_API.delete(`/clients/${ids}`);

export const getKGPrice = () => CLIENT_API.get("/get_kg_price");
export const updateKGPrice = (newPrice) => CLIENT_API.post(`/kg_price/${newPrice}`);
