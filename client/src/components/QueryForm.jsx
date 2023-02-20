import * as React from "react";
import { useState } from "react";
import Box from "@mui/material/Box";
import InputAdornment from "@mui/material/InputAdornment";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import Grid from '@mui/material/Grid';

import SearchIcon from "@mui/icons-material/Search";

const BACKEND_URL = ""
const url = "http://hoangpnapi.hungphu.org/process"
export default function QueryForm({ setData }) {
  const [query, setQuery] = useState("");

  const handleChange = (e) => {
    setQuery(e.target.value)
  }

  const handleSubmit = (event) => {
    event.preventDefault();

    console.log("submited")
    let data = {"query": query,
                "mode": "caption"}
    fetch(url,{
    method: 'POST', // *GET, POST, PUT, DELETE, etc.
    // mode: '*cors', // no-cors, *cors, same-origin
    body: JSON.stringify(data)
    })
      .then((response) => response.json())
      .then((data) => setData(data))
      .catch(err => console.log('Error: ', err))
  }

  const handleSubmitOCR = (event) => {
    event.preventDefault();

    console.log("submited")
    let data = {"query": query,
                "mode": "ocr"}
    fetch(url,{
    method: 'POST', // *GET, POST, PUT, DELETE, etc.
    // mode: '*cors', // no-cors, *cors, same-origin
    body: JSON.stringify(data)
    })
      .then((response) => response.json())
      .then((data) => setData(data))
      .catch(err => console.log('Error: ', err))
  }

  return (
    <Box>
      <form onSubmit={handleSubmit}>
        <Grid
          container
          spacing={1}
          justifyContent="center"
          alignItems="center"
        >
          <Grid item xs={8}>
            <TextField
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon />
                  </InputAdornment>
                ),
              }}
              fullWidth
              variant="outlined"
              value={query}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={8}>
            <Box display="flex" justifyContent="center">
              <Button
                variant="outlined"
                type="submit"
                onClick={handleSubmit}
              >
                via CLIP
              </Button>

              <Button
                variant="outlined"
                type="submit"
                onClick={handleSubmitOCR}
              >
                via OCR
              </Button>
            
            
            </Box>
            
          </Grid>
        </Grid>
      </form>
    </Box>
  );
}