import { AiOutlineClear } from "react-icons/ai";
import { BsArrowsFullscreen, BsFullscreenExit, BsLayoutThreeColumns, BsSortDownAlt } from "react-icons/bs";
import { MdDragIndicator } from "react-icons/md";
import { TbFilter, TbFilterOff } from "react-icons/tb";

export const tableIcons = {
  ClearAllIcon: () => (
    <AiOutlineClear className="text-16 text-gray-500 hover:text-gray-700 cursor-pointer transition-all duration-300" />
  ),
  DragHandleIcon: () => (
    <MdDragIndicator className="text-20 text-gray-500 hover:text-gray-700 cursor-pointer transition-all duration-300" />
  ),
  FilterListIcon: (props) => (
    <TbFilter
      {...props}
      className="text-24 text-gray-500 hover:text-gray-700 cursor-pointer transition-all duration-300"
    />
  ),
  SortIcon: (props) => (
    <BsSortDownAlt {...props} /> //props so that style rotation transforms are applied
  ),
  FilterListOffIcon: () => (
    <TbFilterOff className="text-24 text-gray-500 hover:text-gray-700 cursor-pointer transition-all duration-300" />
  ),
  FullscreenExitIcon: () => (
    <BsFullscreenExit className="text-20 text-gray-500 hover:text-gray-700 cursor-pointer transition-all duration-300" />
  ),
  FullscreenIcon: () => (
    <BsArrowsFullscreen className="text-20 text-gray-500 hover:text-gray-700 cursor-pointer transition-all duration-300" />
  ),
  ViewColumnIcon: () => (
    <BsLayoutThreeColumns className="text-20 text-gray-500 hover:text-gray-700 cursor-pointer transition-all duration-300" />
  ),
};
