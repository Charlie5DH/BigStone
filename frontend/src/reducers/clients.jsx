import {
  GET_CLIENTS,
  GET_CLIENT,
  CREATE_CLIENT,
  UPDATE_CLIENT,
  DELETE_CLIENT,
  LOADING_CLIENTS,
  CLIENTS_FAILED,
  END_CLIENTS_LOADING,
  DELETE_CLIENTS,
  CLEAR_DEBT_CLIENTS,
} from "../constants/clients";

const reducer = (state = { clients: [], client: {}, isLoadingClients: true, clientsFailed: false }, action) => {
  switch (action.type) {
    case GET_CLIENTS:
      return { ...state, clients: action.payload };
    case GET_CLIENT:
      return { ...state, client: action.payload };
    case CREATE_CLIENT:
      return { ...state, clients: [...state.clients, action.payload] };
    case UPDATE_CLIENT:
      return {
        ...state,
        clients: state.clients.map((client) => (client._id === action.payload._id ? action.payload : client)),
      };
    case DELETE_CLIENT:
      return {
        ...state,
        clients: state.clients.filter((client) => client._id !== action.payload),
      };
    case LOADING_CLIENTS:
      return { ...state, isLoadingClients: true };
    case END_CLIENTS_LOADING:
      return { ...state, isLoadingClients: false };
    case CLIENTS_FAILED:
      return { ...state, clientsFailed: true };
    case DELETE_CLIENTS:
      return { ...state, clients: state.clients.filter((client) => !action.payload.includes(client._id)) };
    case CLEAR_DEBT_CLIENTS:
      return {
        ...state,
        clients: state.clients.map((client) => {
          if (action.payload.map((updated) => updated._id).includes(client._id)) {
            return { ...client, balance: 0 };
          } else {
            return client;
          }
        }),
      };

    default:
      return state;
  }
};

export default reducer;
