import * as React from "react";
import { useState } from "react";

import ImageList from "@mui/material/ImageList";
import ImageListItem from "@mui/material/ImageListItem";
import BackdropPlayer from "./BackdropPlayer"

const imageServer = "https://hoangpnapi2.hungphu.org"

export default function ImageGrid({ imageData }) {
  const itemData = [
    {
      img: "https://images.unsplash.com/photo-1551963831-b3b1ca40c98e",
      title: "Breakfast",
    },
    {
      img: "https://images.unsplash.com/photo-1551782450-a2132b4ba21d",
      title: "Burger",
    },
    {
      img: "https://images.unsplash.com/photo-1522770179533-24471fcdba45",
      title: "Camera",
    },
    {
      img: "https://images.unsplash.com/photo-1444418776041-9c7e33cc5a9c",
      title: "Coffee",
    },
    {
      img: "https://images.unsplash.com/photo-1533827432537-70133748f5c8",
      title: "Hats",
    },
    {
      img: "https://images.unsplash.com/photo-1558642452-9d2a7deb7f62",
      title: "Honey",
    },
    {
      img: "https://images.unsplash.com/photo-1516802273409-68526ee1bdd6",
      title: "Basketball",
    },
    {
      img: "https://images.unsplash.com/photo-1518756131217-31eb79b20e8f",
      title: "Fern",
    },
    {
      img: "https://images.unsplash.com/photo-1597645587822-e99fa5d45d25",
      title: "Mushrooms",
    },
    {
      img: "https://images.unsplash.com/photo-1567306301408-9b74779a11af",
      title: "Tomato basil",
    },
    {
      img: "https://images.unsplash.com/photo-1471357674240-e1a485acb3e1",
      title: "Sea star",
    },
    {
      img: "https://images.unsplash.com/photo-1589118949245-7d38baf380d6",
      title: "Bike",
    },
  ];
  const handleClick = (item) => {
    setDataSideBar(item)
  }
  const [dataSideBar, setDataSideBar] = useState(null)
  const handleCloseSidebar = () => {
    // console.log('clicked')
    setDataSideBar(null)
  }
  console.log(dataSideBar)

  return (
    <ImageList sx={{}} cols={5} >
      {imageData.map((item) => (
        <ImageListItem key={item.image_path}>
        {/* <ImageListItem key={item.img}> */}
          <img
            src={`${imageServer}${item.image_path}`}
            // src={item.img}
            // src={'http://localhost:5003/3Batch_KeyFrames/KeyFramesC02_V00/C02_V0021/013729.jpg'}
            // srcSet={`${item.img}?w=164&h=164&fit=crop&auto=format&dpr=2 2x`}
            // alt={item.title}
            loading="lazy"
            onClick={() => handleClick(item)}
          />
        </ImageListItem>
      ))}
      {dataSideBar && (<BackdropPlayer dataSideBar={dataSideBar} handleCloseSidebar={handleCloseSidebar}/>)}
    </ImageList>
  );
  // return (
  //   <ImageList sx={{}} cols={5} >
  //     {itemData.map((item) => (
  //       <ImageListItem key={item.title}>
  //       {/* <ImageListItem key={item.img}> */}
  //         <img
  //           src={`${item.img}`}
  //           // src={item.img}
  //           // src={'http://localhost:5003/3Batch_KeyFrames/KeyFramesC02_V00/C02_V0021/013729.jpg'}
  //           // srcSet={`${item.img}?w=164&h=164&fit=crop&auto=format&dpr=2 2x`}
  //           // alt={item.title}
  //           loading="lazy"
  //           onClick={() => handleClick(item)}
  //         />
  //       </ImageListItem>
  //     ))}
  //     {dataSideBar && (<BackdropPlayer dataSideBar={dataSideBar} handleCloseSidebar={handleCloseSidebar}/>)}
  //   </ImageList>
  // );
}
// ở đây thì tự chỉnh lại theo api động nha