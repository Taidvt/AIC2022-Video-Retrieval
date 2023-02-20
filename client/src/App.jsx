import "./App.css";

import { useState } from "react";
import Box from "@mui/material/Box";

import Header from "./components/Header";
import QueryForm from "./components/QueryForm";
import ImageGrid from "./components/ImageGrid";
import SideBar from "./components/Sidebar";

function App() {
  const [imageData, setImageData] = useState();

  const setData = (data) => {
    setImageData(data);
  };

  return (
    <Box sx={{ width: "100%" }}>
      <Header />
      <QueryForm setData={setData} />
      {/* <ImageGrid imageData={imageData} /> */}
      {imageData && (<ImageGrid imageData={imageData}/>)}
      {/* {(<ImageGrid imageData={imageData} setDataSideBar={setDataSideBar} />)} */}
      {/* {dataSideBar && (<SideBar dataFromClick={dataSideBar} widthDynamic={'600px'} />)} */}
      {/* dòng 25 thì dùng fake data chỉnh lại dùng 24 để lấy dữ liệu từ api */}
    </Box>
  );
}

export default App;
