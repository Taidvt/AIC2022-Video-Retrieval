import * as React from 'react';
import Backdrop from '@mui/material/Backdrop';
import Sidebar from "./Sidebar"


export default function BackdropPlayer({dataSideBar, handleCloseSidebar}) {
  return (
      <Backdrop onClick={handleCloseSidebar}
        sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}
        open={dataSideBar !== null}
      >
        {dataSideBar && (<Sidebar dataFromClick={dataSideBar} widthDynamic={'600px'} />)}
      </Backdrop>
  );
}