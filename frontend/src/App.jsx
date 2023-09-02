import React from "react";
import PageRoutes from "./routes/Routes";
import { styles } from "./styles";
import { Navbar } from "./components";

function App() {
  return (
    <React.Fragment>
      <div className={`bg-slate-100 ${styles.body}`}>
        <Navbar />
        <PageRoutes />
      </div>
    </React.Fragment>
  );
}

export default App;
