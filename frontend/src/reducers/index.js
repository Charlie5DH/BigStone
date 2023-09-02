import { combineReducers } from "redux";
import transactions from "./transactions";
import items from "./items";
import clients from "./clients";
import weight from "./weight";

export default combineReducers({
  transactions,
  items,
  clients,
  weight,
});
