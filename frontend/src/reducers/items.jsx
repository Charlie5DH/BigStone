import {
  GET_ITEMS,
  GET_ITEMS_BY_ID,
  CREATE_ITEM,
  CREATE_MANY_ITEMS,
  UPDATE_ITEM,
  UPDATE_ITEM_QUANTITY,
  SUBTRACT_ITEM_QUANTITY,
  DELETE_ITEM,
  LOADING_ITEMS,
  END_LOADING_ITEMS,
  LOADING_ITEM,
  END_LOADING_ITEM,
  LOADING_ITEM_QUANTITY,
  END_LOADING_ITEM_QUANTITY,
  DELETE_MANY_ITEMS,
} from "../constants/items";

const reducer = (
  state = { items: [], item: {}, isLoadingItems: true, isLoadingItem: true, isLoadingItemQuantity: true },
  action
) => {
  switch (action.type) {
    case GET_ITEMS:
      return { ...state, items: action.payload };
    case GET_ITEMS_BY_ID:
      return { ...state, item: action.payload };
    case CREATE_ITEM:
      return { ...state, items: [...state.items, action.payload] };
    case CREATE_MANY_ITEMS:
      return { ...state, items: [...state.items, ...action.payload] };
    case UPDATE_ITEM:
      return {
        ...state,
        items: state.items.map((item) => (item._id === action.payload._id ? action.payload : item)),
      };
    case UPDATE_ITEM_QUANTITY:
      return {
        ...state,
        items: state.items.map((item) =>
          item._id === action.payload._id ? { ...item, quantity: action.payload.quantity } : item
        ),
      };
    case SUBTRACT_ITEM_QUANTITY:
      return {
        ...state,
        items: state.items.map((item) => (item._id === action.payload._id ? action.payload : item)),
      };
    case DELETE_ITEM:
      return {
        ...state,
        items: state.items.filter((item) => item._id !== action.payload),
      };
    case DELETE_MANY_ITEMS:
      return {
        ...state,
        items: state.items.filter((item) => !action.payload.includes(item._id)),
      };
    case LOADING_ITEMS:
      return { ...state, isLoadingItems: true };
    case END_LOADING_ITEMS:
      return { ...state, isLoadingItems: false };
    case LOADING_ITEM:
      return { ...state, isLoadingItem: true };
    case END_LOADING_ITEM:
      return { ...state, isLoadingItem: false };
    case LOADING_ITEM_QUANTITY:
      return { ...state, isLoadingItemQuantity: true };
    case END_LOADING_ITEM_QUANTITY:
      return { ...state, isLoadingItemQuantity: false };
    default:
      return state;
  }
};

export default reducer;
