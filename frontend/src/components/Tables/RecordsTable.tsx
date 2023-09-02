import React from "react";
import MaterialReactTable from "material-react-table";
import { columns } from "../../constants/tablerows";
import { tableIcons } from "../../constants/table_icons";

const RecordsTable = ({ rows }) => {
  return (
    <MaterialReactTable
      columns={columns(rows)}
      data={rows || []}
      icons={tableIcons}
      enableColumnFilterModes
      enableColumnOrdering
      enableGrouping
      enablePinning
      enableRowSelection
      enableRowActions
      //enableColumnResizing
      //columnResizeMode="onChange"
      muiTablePaperProps={{ elevation: 0 }}
      muiTopToolbarProps={{ sx: { backgroundColor: "#FFFFFF" } }}
      muiTableFooterProps={{ sx: { backgroundColor: "#FFFFFF" } }}
      muiTableProps={{ sx: { backgroundColor: "#FFFFFF" } }}
      muiTableHeadProps={{ sx: { backgroundColor: "#FFFFFF" } }}
      muiToolbarAlertBannerProps={{
        sx: { backgroundColor: "#FAFBFF", borderRadius: "10px" },
      }}
      muiTableBodyCellProps={{
        sx: { backgroundColor: "#FFFFFF" },
      }}
      muiBottomToolbarProps={{ sx: { backgroundColor: "#FFFFFF" } }}
      // muiTableBodyRowProps={{ sx: { height: "10px" } }}
      initialState={{
        showColumnFilters: false,
        density: "compact",
        expanded: {
          0: false,
        },
        pagination: { pageIndex: 0, pageSize: 10 },
      }}
      muiSelectCheckboxProps={{ color: "secondary" }}
      positionToolbarAlertBanner="top"
      enableExpanding
      renderDetailPanel={({ row }) => <div className="w-full">items</div>}
      muiTableHeadCellProps={{
        style: {
          border: "0",
          backgroundColor: "#FFFFFF",
        },
      }}
    />
  );
};

export default RecordsTable;
